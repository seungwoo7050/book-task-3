package main

import (
	"context"
	"database/sql"
	"log/slog"
	"os"
	"os/signal"
	"syscall"
	"time"

	_ "github.com/jackc/pgx/v5/stdlib"
	"github.com/segmentio/kafka-go"

	"github.com/woopinbell/go-backend/study/03-platform-engineering/15-event-pipeline/outbox"
	"github.com/woopinbell/go-backend/study/03-platform-engineering/15-event-pipeline/relay"
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

	db, err := sql.Open("pgx", dsn)
	if err != nil {
		logger.Error("open database", "err", err)
		os.Exit(1)
	}
	defer db.Close()

	db.SetMaxOpenConns(5)
	db.SetMaxIdleConns(2)
	db.SetConnMaxLifetime(5 * time.Minute)

	writer := &kafka.Writer{
		Addr:         kafka.TCP(kafkaBroker),
		Topic:        kafkaTopic,
		Balancer:     &kafka.Hash{},
		RequiredAcks: kafka.RequireAll,
		BatchTimeout: 10 * time.Millisecond,
	}
	defer writer.Close()

	repo := outbox.NewRepository(db)

	r := relay.New(repo, writer, logger, relay.Config{
		PollInterval: time.Second,
		BatchSize:    100,
	})

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)

	go func() {
		sig := <-sigCh
		logger.Info("received signal", "signal", sig)
		cancel()
	}()

	if err := r.Run(ctx); err != nil && err != context.Canceled {
		logger.Error("relay error", "err", err)
		os.Exit(1)
	}
}
