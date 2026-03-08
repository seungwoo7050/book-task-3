package e2e

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"io"
	"log/slog"
	"os"
	"sync/atomic"
	"testing"
	"time"

	_ "github.com/jackc/pgx/v5/stdlib"
	"github.com/segmentio/kafka-go"

	"github.com/woopinbell/go-backend/study/03-platform-engineering/15-event-pipeline/consumer"
	"github.com/woopinbell/go-backend/study/03-platform-engineering/15-event-pipeline/outbox"
	"github.com/woopinbell/go-backend/study/03-platform-engineering/15-event-pipeline/relay"
)

const (
	defaultDatabaseURL = "postgresql://root@localhost:26258/defaultdb?sslmode=disable"
	defaultKafkaBroker = "localhost:9093"
)

func TestRelayPublishesAndConsumerDedupesAcrossRestart(t *testing.T) {
	requireRuntime(t)

	db := openDB(t)
	t.Cleanup(func() { _ = db.Close() })
	resetState(t, db)

	broker := os.Getenv("KAFKA_BROKER")
	if broker == "" {
		broker = defaultKafkaBroker
	}
	topic := fmt.Sprintf("game.purchases.e2e.%d", time.Now().UnixNano())

	eventID := "22222222-2222-2222-2222-222222222222"
	aggregateID := "33333333-3333-3333-3333-333333333333"
	payload := outbox.PurchasePayload{
		PlayerID:   aggregateID,
		ItemName:   "sword_of_fire",
		Price:      100,
		NewBalance: 900,
		Timestamp:  time.Now().UTC().Round(time.Second),
	}
	payloadJSON, err := json.Marshal(payload)
	if err != nil {
		t.Fatalf("marshal payload: %v", err)
	}
	insertEvent(t, db, eventID, aggregateID, payloadJSON)

	logger := slog.New(slog.NewTextHandler(io.Discard, nil))
	repo := outbox.NewRepository(db)
	writer := &kafka.Writer{
		Addr:                   kafka.TCP(broker),
		Topic:                  topic,
		Balancer:               &kafka.Hash{},
		AllowAutoTopicCreation: true,
		BatchTimeout:           10 * time.Millisecond,
		RequiredAcks:           kafka.RequireAll,
	}
	t.Cleanup(func() { _ = writer.Close() })

	var processedCount atomic.Int32
	consumerGroup1 := fmt.Sprintf("purchase-analytics-e2e-%d-a", time.Now().UnixNano())
	reader1 := kafka.NewReader(kafka.ReaderConfig{
		Brokers:        []string{broker},
		GroupID:        consumerGroup1,
		Topic:          topic,
		MinBytes:       1,
		MaxBytes:       10e6,
		CommitInterval: 0,
		StartOffset:    kafka.FirstOffset,
	})
	t.Cleanup(func() { _ = reader1.Close() })

	relayCtx, relayCancel := context.WithCancel(context.Background())
	defer relayCancel()
	consumerCtx1, consumerCancel1 := context.WithCancel(context.Background())

	relayProc := relay.New(repo, writer, logger, relay.Config{
		PollInterval: 100 * time.Millisecond,
		BatchSize:    10,
	})
	consumerProc1 := consumer.New(reader1, db, func(ctx context.Context, eventType string, payload json.RawMessage) error {
		processedCount.Add(1)
		if eventType != "PurchaseCompleted" {
			return fmt.Errorf("unexpected event type %q", eventType)
		}
		return nil
	}, logger)

	go func() {
		_ = relayProc.Run(relayCtx)
	}()
	go func() {
		_ = consumerProc1.Run(consumerCtx1)
	}()

	waitFor(t, 10*time.Second, func() bool {
		return processedCount.Load() == 1 &&
			isPublished(t, db, eventID) &&
			processedRowCount(t, db, eventID) == 1
	})

	consumerCancel1()
	_ = reader1.Close()
	time.Sleep(250 * time.Millisecond)

	var replayCount atomic.Int32
	consumerGroup2 := fmt.Sprintf("purchase-analytics-e2e-%d-b", time.Now().UnixNano())
	reader2 := kafka.NewReader(kafka.ReaderConfig{
		Brokers:        []string{broker},
		GroupID:        consumerGroup2,
		Topic:          topic,
		MinBytes:       1,
		MaxBytes:       10e6,
		CommitInterval: 0,
		StartOffset:    kafka.LastOffset,
	})
	t.Cleanup(func() { _ = reader2.Close() })

	consumerCtx2, consumerCancel2 := context.WithCancel(context.Background())
	defer consumerCancel2()
	consumerProc2 := consumer.New(reader2, db, func(ctx context.Context, eventType string, payload json.RawMessage) error {
		replayCount.Add(1)
		return nil
	}, logger)
	go func() {
		_ = consumerProc2.Run(consumerCtx2)
	}()

	duplicate := kafka.Message{
		Key:   []byte(aggregateID),
		Value: payloadJSON,
		Headers: []kafka.Header{
			{Key: "event_type", Value: []byte("PurchaseCompleted")},
			{Key: "event_id", Value: []byte(eventID)},
			{Key: "aggregate_type", Value: []byte("player")},
		},
	}
	if err := writer.WriteMessages(context.Background(), duplicate); err != nil {
		t.Fatalf("write duplicate message: %v", err)
	}

	time.Sleep(750 * time.Millisecond)
	if replayCount.Load() != 0 {
		t.Fatalf("replay handler count = %d, want 0", replayCount.Load())
	}
	if processedRowCount(t, db, eventID) != 1 {
		t.Fatalf("processed row count changed, want 1")
	}
}

func requireRuntime(t *testing.T) {
	t.Helper()
	if os.Getenv("RUN_E2E") != "1" {
		t.Skip("set RUN_E2E=1 to execute runtime integration tests")
	}
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
		`DELETE FROM processed_events`,
		`DELETE FROM outbox`,
	}
	for _, stmt := range statements {
		if _, err := db.Exec(stmt); err != nil {
			t.Fatalf("exec %q: %v", stmt, err)
		}
	}
}

func insertEvent(t *testing.T, db *sql.DB, eventID, aggregateID string, payload []byte) {
	t.Helper()
	if _, err := db.Exec(
		`INSERT INTO outbox (id, aggregate_type, aggregate_id, event_type, payload) VALUES ($1, $2, $3, $4, $5)`,
		eventID,
		"player",
		aggregateID,
		"PurchaseCompleted",
		payload,
	); err != nil {
		t.Fatalf("insert outbox event: %v", err)
	}
}

func isPublished(t *testing.T, db *sql.DB, eventID string) bool {
	t.Helper()
	var publishedAt sql.NullTime
	if err := db.QueryRow(`SELECT published_at FROM outbox WHERE id = $1`, eventID).Scan(&publishedAt); err != nil {
		t.Fatalf("query published_at: %v", err)
	}
	return publishedAt.Valid
}

func processedRowCount(t *testing.T, db *sql.DB, eventID string) int {
	t.Helper()
	var count int
	if err := db.QueryRow(`SELECT count(*) FROM processed_events WHERE event_id = $1`, eventID).Scan(&count); err != nil {
		t.Fatalf("query processed_events: %v", err)
	}
	return count
}

func waitFor(t *testing.T, timeout time.Duration, condition func() bool) {
	t.Helper()
	deadline := time.Now().Add(timeout)
	for time.Now().Before(deadline) {
		if condition() {
			return
		}
		time.Sleep(100 * time.Millisecond)
	}
	t.Fatal("condition was not met before timeout")
}
