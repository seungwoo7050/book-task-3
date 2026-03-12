package main

import (
	"context"
	"database/sql"
	"encoding/json"
	"log/slog"
	"os"
	"os/signal"
	"syscall"
	"time"

	_ "github.com/jackc/pgx/v5/stdlib"
	"github.com/segmentio/kafka-go"

	"github.com/woopinbell/go-backend/study/03-platform-engineering/15-event-pipeline/consumer"
)

func main() {
	logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
		Level: slog.LevelInfo,
	}))

	dsn := os.Getenv("DATABASE_URL")
	if dsn == "" {
		dsn = "postgresql://root@localhost:26257/defaultdb?sslmode=disable"
	}

	kafkaBroker := os.Getenv("KAFKA_BROKER")
	if kafkaBroker == "" {
		kafkaBroker = "localhost:9092"
	}

	kafkaTopic := os.Getenv("KAFKA_TOPIC")
	if kafkaTopic == "" {
		kafkaTopic = "game.purchases"
	}

	groupID := os.Getenv("CONSUMER_GROUP")
	if groupID == "" {
		groupID = "purchase-analytics"
	}

	db, err := sql.Open("pgx", dsn)
	if err != nil {
		logger.Error("open database", "err", err)
		os.Exit(1)
	}
	defer db.Close()

	db.SetMaxOpenConns(5)
	db.SetMaxIdleConns(2)
	db.SetConnMaxLifetime(5 * time.Minute)

	reader := kafka.NewReader(kafka.ReaderConfig{
		Brokers:        []string{kafkaBroker},
		GroupID:        groupID,
		Topic:          kafkaTopic,
		MinBytes:       1,
		MaxBytes:       10e6,
		CommitInterval: 0, // manual commit for at-least-once
		StartOffset:    kafka.FirstOffset,
	})
	defer reader.Close()
	handler := func(ctx context.Context, eventType string, payload json.RawMessage) error {
		logger.Info("event received",
			"type", eventType,
			"payload", string(payload),
		)
		return nil
	}

	c := consumer.New(reader, db, handler, logger)

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)

	go func() {
		sig := <-sigCh
		logger.Info("received signal", "signal", sig)
		cancel()
	}()

	if err := c.Run(ctx); err != nil && err != context.Canceled {
		logger.Error("consumer error", "err", err)
		os.Exit(1)
	}
}
