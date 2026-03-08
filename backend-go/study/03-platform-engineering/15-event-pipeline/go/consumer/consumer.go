// Package consumer implements a Kafka consumer with at-least-once
// semantics and idempotent event processing.
package consumer

import (
	"context"
	"database/sql"
	"encoding/json"
	"errors"
	"log/slog"
	"sync"

	"github.com/segmentio/kafka-go"
)

// Handler processes a single event. Implementations must be idempotent.
type Handler func(ctx context.Context, eventType string, payload json.RawMessage) error

// Consumer reads messages from Kafka and processes them idempotently.
type Consumer struct {
	reader  *kafka.Reader
	db      *sql.DB
	handler Handler
	logger  *slog.Logger

	// In-memory dedup cache for fast duplicate detection.
	// For production, use the processed_events DB table.
	mu        sync.RWMutex
	processed map[string]struct{}
}

// New creates a new Consumer.
func New(reader *kafka.Reader, db *sql.DB, handler Handler, logger *slog.Logger) *Consumer {
	return &Consumer{
		reader:    reader,
		db:        db,
		handler:   handler,
		logger:    logger,
		processed: make(map[string]struct{}),
	}
}

// Run starts consuming messages. It blocks until ctx is cancelled.
func (c *Consumer) Run(ctx context.Context) error {
	c.logger.Info("consumer started")

	for {
		msg, err := c.reader.FetchMessage(ctx)
		if err != nil {
			if ctx.Err() != nil {
				c.logger.Info("consumer stopping")
				return ctx.Err()
			}
			c.logger.Error("fetch message failed", "err", err)
			continue
		}

		eventID := getHeader(msg.Headers, "event_id")
		eventType := getHeader(msg.Headers, "event_type")

		// Idempotency check.
		if c.isProcessed(eventID) {
			c.logger.Info("skipping duplicate",
				"event_id", eventID,
				"offset", msg.Offset,
			)
			c.commitMessage(ctx, msg)
			continue
		}
		if c.isPersisted(ctx, eventID) {
			c.markProcessed(eventID)
			c.logger.Info("skipping persisted duplicate",
				"event_id", eventID,
				"offset", msg.Offset,
			)
			c.commitMessage(ctx, msg)
			continue
		}

		c.logger.Info("processing event",
			"event_id", eventID,
			"type", eventType,
			"partition", msg.Partition,
			"offset", msg.Offset,
		)

		if err := c.handler(ctx, eventType, msg.Value); err != nil {
			c.logger.Error("handler failed",
				"event_id", eventID,
				"err", err,
			)
			// Don't commit — message will be re-delivered.
			continue
		}

		// Mark as processed.
		c.markProcessed(eventID)
		c.persistProcessed(ctx, eventID)

		// Commit offset.
		c.commitMessage(ctx, msg)
	}
}

// isProcessed checks the in-memory cache.
func (c *Consumer) isProcessed(eventID string) bool {
	c.mu.RLock()
	defer c.mu.RUnlock()
	_, ok := c.processed[eventID]
	return ok
}

// markProcessed adds the event ID to the in-memory cache.
func (c *Consumer) markProcessed(eventID string) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.processed[eventID] = struct{}{}
}

// isPersisted checks the durable processed_events table.
func (c *Consumer) isPersisted(ctx context.Context, eventID string) bool {
	if c.db == nil || eventID == "" {
		return false
	}

	var existing string
	err := c.db.QueryRowContext(ctx,
		`SELECT event_id FROM processed_events WHERE event_id = $1`,
		eventID,
	).Scan(&existing)
	if errors.Is(err, sql.ErrNoRows) {
		return false
	}
	if err != nil {
		c.logger.Error("check persisted processed failed",
			"event_id", eventID,
			"err", err,
		)
		return false
	}
	return existing != ""
}

// persistProcessed writes the event ID to the processed_events table.
func (c *Consumer) persistProcessed(ctx context.Context, eventID string) {
	if c.db == nil {
		return
	}
	_, err := c.db.ExecContext(ctx,
		`INSERT INTO processed_events (event_id) VALUES ($1) ON CONFLICT DO NOTHING`,
		eventID,
	)
	if err != nil {
		c.logger.Error("persist processed failed",
			"event_id", eventID,
			"err", err,
		)
	}
}

// commitMessage commits the given message's offset.
func (c *Consumer) commitMessage(ctx context.Context, msg kafka.Message) {
	if err := c.reader.CommitMessages(ctx, msg); err != nil {
		c.logger.Error("commit failed",
			"offset", msg.Offset,
			"err", err,
		)
	}
}

// getHeader extracts a header value by key from Kafka message headers.
func getHeader(headers []kafka.Header, key string) string {
	for _, h := range headers {
		if h.Key == key {
			return string(h.Value)
		}
	}
	return ""
}
