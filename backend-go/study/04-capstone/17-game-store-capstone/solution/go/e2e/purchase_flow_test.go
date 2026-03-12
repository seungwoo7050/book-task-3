package e2e

import (
	"bytes"
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"io"
	"log/slog"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"sync"
	"testing"
	"time"

	_ "github.com/jackc/pgx/v5/stdlib"

	"github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/domain"
	"github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/httpapi"
	"github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/relay"
	"github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/repository"
	"github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/service"
)

const (
	playerAlice = "11111111-1111-1111-1111-111111111111"
	playerBob   = "22222222-2222-2222-2222-222222222222"

	itemSword  = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
	itemShield = "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
)

type purchaseResponse struct {
	PurchaseID string    `json:"purchase_id"`
	PlayerID   string    `json:"player_id"`
	ItemID     string    `json:"item_id"`
	Price      int64     `json:"price"`
	NewBalance int64     `json:"new_balance"`
	Status     string    `json:"status"`
	CreatedAt  time.Time `json:"created_at"`
}

type errorResponse struct {
	Error string `json:"error"`
}

type inventoryEnvelope struct {
	PlayerID string                 `json:"player_id"`
	Items    []domain.InventoryItem `json:"items"`
}

type capturePublisher struct {
	events []string
}

func (p *capturePublisher) Publish(_ context.Context, event domain.OutboxEvent) error {
	p.events = append(p.events, event.ID)
	return nil
}

func TestPurchaseFlowReplayReadAndRelay(t *testing.T) {
	db := openTestDB(t)
	store := repository.NewStore(db)
	server := newTestServer(t, db)
	defer server.Close()

	resetAndSeed(t, db)

	firstStatus, firstBody := doJSONRequest(t, http.MethodPost, server.URL+"/v1/purchases", "idem-e2e-001", map[string]string{
		"player_id": playerAlice,
		"item_id":   itemSword,
	})
	if firstStatus != http.StatusOK {
		t.Fatalf("first purchase status=%d body=%s", firstStatus, string(firstBody))
	}

	var first purchaseResponse
	mustUnmarshal(t, firstBody, &first)
	if first.PurchaseID == "" || first.NewBalance != 4000 {
		t.Fatalf("unexpected first purchase response: %+v", first)
	}

	replayStatus, replayBody := doJSONRequest(t, http.MethodPost, server.URL+"/v1/purchases", "idem-e2e-001", map[string]string{
		"player_id": playerAlice,
		"item_id":   itemSword,
	})
	if replayStatus != http.StatusOK {
		t.Fatalf("replay purchase status=%d body=%s", replayStatus, string(replayBody))
	}

	var replay purchaseResponse
	mustUnmarshal(t, replayBody, &replay)
	if replay.PurchaseID != first.PurchaseID || replay.NewBalance != first.NewBalance {
		t.Fatalf("replay mismatch first=%+v replay=%+v", first, replay)
	}

	getStatus, getBody := doJSONRequest(t, http.MethodGet, server.URL+"/v1/purchases/"+first.PurchaseID, "", nil)
	if getStatus != http.StatusOK {
		t.Fatalf("get purchase status=%d body=%s", getStatus, string(getBody))
	}

	var gotPurchase domain.Purchase
	mustUnmarshal(t, getBody, &gotPurchase)
	if gotPurchase.ID != first.PurchaseID {
		t.Fatalf("purchase id mismatch got=%s want=%s", gotPurchase.ID, first.PurchaseID)
	}

	invStatus, invBody := doJSONRequest(t, http.MethodGet, server.URL+"/v1/players/"+playerAlice+"/inventory", "", nil)
	if invStatus != http.StatusOK {
		t.Fatalf("get inventory status=%d body=%s", invStatus, string(invBody))
	}

	var inventory inventoryEnvelope
	mustUnmarshal(t, invBody, &inventory)
	if len(inventory.Items) != 1 || inventory.Items[0].ItemID != itemSword || inventory.Items[0].Qty != 1 {
		t.Fatalf("unexpected inventory response: %+v", inventory)
	}

	var unpublishedBefore int
	if err := db.QueryRow(`SELECT count(*) FROM outbox WHERE published_at IS NULL`).Scan(&unpublishedBefore); err != nil {
		t.Fatalf("query unpublished before relay: %v", err)
	}
	if unpublishedBefore != 1 {
		t.Fatalf("unexpected unpublished before relay: %d", unpublishedBefore)
	}

	pub := &capturePublisher{}
	relayRunner := relay.New(
		store,
		pub,
		slog.New(slog.NewTextHandler(io.Discard, nil)),
		time.Second,
		10,
	)
	if err := relayRunner.PollOnce(context.Background()); err != nil {
		t.Fatalf("relay poll once: %v", err)
	}
	if len(pub.events) != 1 {
		t.Fatalf("publisher event count=%d want=1", len(pub.events))
	}

	var publishedCount int
	if err := db.QueryRow(`SELECT count(*) FROM outbox WHERE published_at IS NOT NULL`).Scan(&publishedCount); err != nil {
		t.Fatalf("query published count: %v", err)
	}
	if publishedCount != 1 {
		t.Fatalf("unexpected published count: %d", publishedCount)
	}
}

func TestPurchaseInsufficientBalanceAndIdempotencyConflict(t *testing.T) {
	db := openTestDB(t)
	server := newTestServer(t, db)
	defer server.Close()

	resetAndSeed(t, db)

	okStatus, okBody := doJSONRequest(t, http.MethodPost, server.URL+"/v1/purchases", "idem-e2e-101", map[string]string{
		"player_id": playerBob,
		"item_id":   itemShield,
	})
	if okStatus != http.StatusOK {
		t.Fatalf("first purchase status=%d body=%s", okStatus, string(okBody))
	}

	insufficientStatus, insufficientBody := doJSONRequest(t, http.MethodPost, server.URL+"/v1/purchases", "idem-e2e-102", map[string]string{
		"player_id": playerBob,
		"item_id":   itemSword,
	})
	if insufficientStatus != http.StatusConflict {
		t.Fatalf("insufficient purchase status=%d body=%s", insufficientStatus, string(insufficientBody))
	}

	var insufficientErr errorResponse
	mustUnmarshal(t, insufficientBody, &insufficientErr)
	if insufficientErr.Error != "insufficient balance" {
		t.Fatalf("unexpected insufficient error: %q", insufficientErr.Error)
	}

	conflictStatus, conflictBody := doJSONRequest(t, http.MethodPost, server.URL+"/v1/purchases", "idem-e2e-101", map[string]string{
		"player_id": playerBob,
		"item_id":   itemSword,
	})
	if conflictStatus != http.StatusConflict {
		t.Fatalf("idempotency conflict status=%d body=%s", conflictStatus, string(conflictBody))
	}

	var idemErr errorResponse
	mustUnmarshal(t, conflictBody, &idemErr)
	if idemErr.Error != "idempotency key conflict" {
		t.Fatalf("unexpected idempotency conflict error: %q", idemErr.Error)
	}
}

func TestConcurrentSameIdempotencyKeyCreatesSinglePurchase(t *testing.T) {
	db := openTestDB(t)
	server := newTestServer(t, db)
	defer server.Close()

	resetAndSeed(t, db)

	const idemKey = "idem-e2e-concurrent-001"
	payload := map[string]string{
		"player_id": playerAlice,
		"item_id":   itemSword,
	}

	type result struct {
		status int
		body   []byte
		err    error
	}

	start := make(chan struct{})
	results := make(chan result, 2)
	var wg sync.WaitGroup

	worker := func(idx int) {
		defer wg.Done()
		<-start
		status, body := doJSONRequestNoFail(http.MethodPost, server.URL+"/v1/purchases", idemKey, payload)
		results <- result{status: status, body: body}
		_ = idx
	}

	wg.Add(2)
	go worker(1)
	go worker(2)
	close(start)
	wg.Wait()
	close(results)

	collected := make([]result, 0, 2)
	for r := range results {
		collected = append(collected, r)
	}
	if len(collected) != 2 {
		t.Fatalf("unexpected result count: %d", len(collected))
	}

	for i, r := range collected {
		if r.status != http.StatusOK {
			t.Fatalf("request %d status=%d body=%s", i, r.status, string(r.body))
		}
	}

	var first, second purchaseResponse
	mustUnmarshal(t, collected[0].body, &first)
	mustUnmarshal(t, collected[1].body, &second)

	if first.PurchaseID == "" || second.PurchaseID == "" {
		t.Fatalf("empty purchase id first=%q second=%q", first.PurchaseID, second.PurchaseID)
	}
	if first.PurchaseID != second.PurchaseID {
		t.Fatalf("purchase ids differ first=%s second=%s", first.PurchaseID, second.PurchaseID)
	}

	var purchaseCount int
	if err := db.QueryRow(`SELECT count(*) FROM purchases WHERE player_id = $1 AND item_id = $2`, playerAlice, itemSword).Scan(&purchaseCount); err != nil {
		t.Fatalf("count purchases: %v", err)
	}
	if purchaseCount != 1 {
		t.Fatalf("expected 1 purchase row, got %d", purchaseCount)
	}
}

func openTestDB(t *testing.T) *sql.DB {
	t.Helper()

	dsn := os.Getenv("DATABASE_URL")
	if dsn == "" {
		t.Skip("DATABASE_URL is required for e2e tests")
	}

	db, err := sql.Open("pgx", dsn)
	if err != nil {
		t.Fatalf("open db: %v", err)
	}
	t.Cleanup(func() {
		_ = db.Close()
	})

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if err := db.PingContext(ctx); err != nil {
		t.Fatalf("ping db: %v", err)
	}

	applySchema(t, db)
	return db
}

func applySchema(t *testing.T, db *sql.DB) {
	t.Helper()

	schemaPath := filepath.Join("..", "schema.sql")
	sqlBytes, err := os.ReadFile(schemaPath)
	if err != nil {
		t.Fatalf("read schema.sql: %v", err)
	}

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if _, err := db.ExecContext(ctx, string(sqlBytes)); err != nil {
		t.Fatalf("apply schema: %v", err)
	}
}

func resetAndSeed(t *testing.T, db *sql.DB) {
	t.Helper()

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	cleanup := []string{
		`DELETE FROM outbox`,
		`DELETE FROM idempotency_keys`,
		`DELETE FROM purchases`,
		`DELETE FROM inventories`,
		`DELETE FROM catalog_items`,
		`DELETE FROM players`,
	}
	for _, q := range cleanup {
		if _, err := db.ExecContext(ctx, q); err != nil {
			t.Fatalf("cleanup query failed (%s): %v", q, err)
		}
	}

	seed := []string{
		`INSERT INTO players (id, name, balance, version) VALUES
		  ('11111111-1111-1111-1111-111111111111', 'alice', 5000, 0),
		  ('22222222-2222-2222-2222-222222222222', 'bob', 2000, 0)`,
		`INSERT INTO catalog_items (id, sku, name, price) VALUES
		  ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'sword-basic', 'Bronze Sword', 1000),
		  ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'shield-basic', 'Wood Shield', 1500),
		  ('cccccccc-cccc-cccc-cccc-cccccccccccc', 'potion-hp', 'HP Potion', 300)`,
	}
	for _, q := range seed {
		if _, err := db.ExecContext(ctx, q); err != nil {
			t.Fatalf("seed query failed (%s): %v", q, err)
		}
	}
}

func newTestServer(t *testing.T, db *sql.DB) *httptest.Server {
	t.Helper()

	store := repository.NewStore(db)
	purchaseSvc := service.NewPurchaseService(db, store)
	querySvc := service.NewQueryService(store)
	logger := slog.New(slog.NewTextHandler(io.Discard, nil))

	api := httpapi.NewAPI(purchaseSvc, querySvc, logger, 10_000)
	return httptest.NewServer(api.Routes())
}

func doJSONRequest(t *testing.T, method, url, idempotencyKey string, payload any) (int, []byte) {
	t.Helper()

	status, body := doJSONRequestNoFail(method, url, idempotencyKey, payload)
	if status == 0 {
		t.Fatalf("request failed without status")
	}
	return status, body
}

func doJSONRequestNoFail(method, url, idempotencyKey string, payload any) (int, []byte) {

	var body io.Reader
	if payload != nil {
		b, err := json.Marshal(payload)
		if err != nil {
			return 0, []byte(fmt.Sprintf(`{"error":"marshal payload: %v"}`, err))
		}
		body = bytes.NewReader(b)
	}

	req, err := http.NewRequest(method, url, body)
	if err != nil {
		return 0, []byte(fmt.Sprintf(`{"error":"new request: %v"}`, err))
	}
	if payload != nil {
		req.Header.Set("Content-Type", "application/json")
	}
	if idempotencyKey != "" {
		req.Header.Set("Idempotency-Key", idempotencyKey)
	}

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return 0, []byte(fmt.Sprintf(`{"error":"http request: %v"}`, err))
	}
	defer resp.Body.Close()

	respBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		return resp.StatusCode, []byte(fmt.Sprintf(`{"error":"read response: %v"}`, err))
	}
	return resp.StatusCode, respBytes
}

func mustUnmarshal(t *testing.T, b []byte, target any) {
	t.Helper()
	if err := json.Unmarshal(b, target); err != nil {
		t.Fatalf("unmarshal failed body=%s err=%v", string(b), err)
	}
}
