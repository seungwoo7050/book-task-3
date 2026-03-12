package e2e

import (
	"bytes"
	"context"
	"database/sql"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"os"
	"testing"
	"time"

	_ "github.com/jackc/pgx/v5/stdlib"

	"github.com/woopinbell/go-backend/study/03-platform-engineering/14-cockroach-tx/handler"
	"github.com/woopinbell/go-backend/study/03-platform-engineering/14-cockroach-tx/service"
)

const (
	defaultDatabaseURL = "postgresql://root@localhost:26257/defaultdb?sslmode=disable"
	playerID           = "11111111-1111-1111-1111-111111111111"
)

type purchaseResponse struct {
	Status     string `json:"status"`
	NewBalance int64  `json:"new_balance"`
	Item       string `json:"item"`
}

func TestPurchaseFlowReplayAndPersistence(t *testing.T) {
	requireRuntime(t)

	db := openDB(t)
	t.Cleanup(func() { _ = db.Close() })

	resetState(t, db)
	seedPlayer(t, db, 1_000)

	server := httptest.NewServer(&handler.PurchaseHandler{
		Service: service.NewPurchaseService(db),
	})
	t.Cleanup(server.Close)

	first := doPurchase(t, server.URL, "idem-e2e-1", map[string]any{
		"player_id": playerID,
		"item_name": "sword_of_fire",
		"price":     100,
	})
	if first.Status != "ok" {
		t.Fatalf("status = %q, want ok", first.Status)
	}
	if first.NewBalance != 900 {
		t.Fatalf("new_balance = %d, want 900", first.NewBalance)
	}

	replay := doPurchase(t, server.URL, "idem-e2e-1", map[string]any{
		"player_id": playerID,
		"item_name": "sword_of_fire",
		"price":     100,
	})
	if replay != first {
		t.Fatalf("replay = %+v, want %+v", replay, first)
	}

	var (
		balance   int64
		version   int
		quantity  int
		auditRows int
		idemRows  int
	)
	mustQueryRow(t, db, `SELECT balance, version FROM players WHERE id = $1`, playerID).Scan(&balance, &version)
	mustQueryRow(t, db, `SELECT quantity FROM inventory WHERE player_id = $1 AND item_name = $2`, playerID, "sword_of_fire").Scan(&quantity)
	mustQueryRow(t, db, `SELECT count(*) FROM audit_log WHERE player_id = $1`, playerID).Scan(&auditRows)
	mustQueryRow(t, db, `SELECT count(*) FROM idempotency_keys WHERE key = $1`, "idem-e2e-1").Scan(&idemRows)

	if balance != 900 {
		t.Fatalf("balance = %d, want 900", balance)
	}
	if version != 2 {
		t.Fatalf("version = %d, want 2", version)
	}
	if quantity != 1 {
		t.Fatalf("quantity = %d, want 1", quantity)
	}
	if auditRows != 1 {
		t.Fatalf("audit rows = %d, want 1", auditRows)
	}
	if idemRows != 1 {
		t.Fatalf("idempotency rows = %d, want 1", idemRows)
	}
}

func TestHealthz(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte("ok\n"))
	}))
	t.Cleanup(server.Close)

	resp, err := http.Get(server.URL)
	if err != nil {
		t.Fatalf("healthz request: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		t.Fatalf("status = %d, want %d", resp.StatusCode, http.StatusOK)
	}
}

func requireRuntime(t *testing.T) {
	t.Helper()
	if os.Getenv("RUN_E2E") != "1" {
		t.Skip("set RUN_E2E=1 to execute runtime integration tests")
	}
}

func doPurchase(t *testing.T, baseURL, idempotencyKey string, payload map[string]any) purchaseResponse {
	t.Helper()

	body, err := json.Marshal(payload)
	if err != nil {
		t.Fatalf("marshal payload: %v", err)
	}

	req, err := http.NewRequest(http.MethodPost, baseURL+"/api/purchase", bytes.NewReader(body))
	if err != nil {
		t.Fatalf("new request: %v", err)
	}
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Idempotency-Key", idempotencyKey)

	client := &http.Client{Timeout: 5 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		t.Fatalf("purchase request: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		t.Fatalf("status = %d, want %d", resp.StatusCode, http.StatusOK)
	}

	var out purchaseResponse
	if err := json.NewDecoder(resp.Body).Decode(&out); err != nil {
		t.Fatalf("decode response: %v", err)
	}
	return out
}

func openDB(t *testing.T) *sql.DB {
	t.Helper()

	dsn := os.Getenv("DATABASE_URL")
	if dsn == "" {
		dsn = defaultDatabaseURL
	}

	db, err := sql.Open("pgx", dsn)
	if err != nil {
		t.Fatalf("open db: %v", err)
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if err := db.PingContext(ctx); err != nil {
		t.Fatalf("ping db: %v", err)
	}
	return db
}

func resetState(t *testing.T, db *sql.DB) {
	t.Helper()

	statements := []string{
		`DELETE FROM audit_log`,
		`DELETE FROM idempotency_keys`,
		`DELETE FROM inventory`,
		`DELETE FROM players`,
	}
	for _, stmt := range statements {
		if _, err := db.Exec(stmt); err != nil {
			t.Fatalf("exec %q: %v", stmt, err)
		}
	}
}

func seedPlayer(t *testing.T, db *sql.DB, balance int64) {
	t.Helper()

	if _, err := db.Exec(
		`INSERT INTO players (id, name, balance, version) VALUES ($1, $2, $3, 1)`,
		playerID,
		"e2e-player",
		balance,
	); err != nil {
		t.Fatalf("insert player: %v", err)
	}
}

func mustQueryRow(t *testing.T, db *sql.DB, query string, args ...any) *sql.Row {
	t.Helper()
	return db.QueryRow(query, args...)
}
