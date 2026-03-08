// Package relay implements the outbox relay process that publishes
// events from the outbox table to Kafka.
package relay

import (
	"context"
	"log/slog"
	"time"

	"github.com/segmentio/kafka-go"

	"github.com/woopinbell/go-backend/study/03-platform-engineering/15-event-pipeline/outbox"
)

// Relay polls the outbox table and publishes events to Kafka.
type Relay struct {
	repo     *outbox.Repository
	writer   *kafka.Writer
	logger   *slog.Logger
	interval time.Duration
	batch    int
}

// Config holds relay configuration.
type Config struct {
	PollInterval time.Duration
	BatchSize    int
}

// New creates a new Relay.
func New(repo *outbox.Repository, writer *kafka.Writer, logger *slog.Logger, cfg Config) *Relay {
	if cfg.PollInterval == 0 {
		cfg.PollInterval = time.Second
	}
	if cfg.BatchSize == 0 {
		cfg.BatchSize = 100
	}
	return &Relay{
		repo:     repo,
		writer:   writer,
		logger:   logger,
		interval: cfg.PollInterval,
		batch:    cfg.BatchSize,
	}
}

// Run starts the polling loop. It blocks until ctx is cancelled.
func (r *Relay) Run(ctx context.Context) error {
	r.logger.Info("relay started", "interval", r.interval, "batch", r.batch)

	ticker := time.NewTicker(r.interval)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			r.logger.Info("relay stopping")
			return ctx.Err()
		case <-ticker.C:
			if err := r.poll(ctx); err != nil {
				r.logger.Error("poll failed", "err", err)
			}
		}
	}
}

// poll fetches unpublished events and publishes them to Kafka.
func (r *Relay) poll(ctx context.Context) error {
	events, err := r.repo.GetUnpublished(ctx, r.batch)
	if err != nil {
		return err
	}
	if len(events) == 0 {
		return nil
	}

	r.logger.Info("publishing events", "count", len(events))

	for _, event := range events {
		msg := kafka.Message{
			Key:   []byte(event.AggregateID),
			Value: event.Payload,
			Headers: []kafka.Header{
				{Key: "event_type", Value: []byte(event.EventType)},
				{Key: "event_id", Value: []byte(event.ID)},
				{Key: "aggregate_type", Value: []byte(event.AggregateType)},
			},
		}

		if err := r.writer.WriteMessages(ctx, msg); err != nil {
			r.logger.Error("publish failed",
				"event_id", event.ID,
				"err", err,
			)
			return err // stop batch; will retry on next poll
		}

		if err := r.repo.MarkPublished(ctx, event.ID); err != nil {
			r.logger.Error("mark published failed",
				"event_id", event.ID,
				"err", err,
			)
			// Event may be re-published next poll — at-least-once is fine.
		}

		r.logger.Info("event published",
			"event_id", event.ID,
			"type", event.EventType,
			"aggregate", event.AggregateID,
		)
	}

	return nil
}
