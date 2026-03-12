package relay

import (
	"context"
	"log/slog"
	"time"

	"github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/domain"
)

type OutboxStore interface {
	ListUnpublishedOutbox(ctx context.Context, limit int) ([]domain.OutboxEvent, error)
	MarkOutboxPublished(ctx context.Context, eventID string) error
}
type Publisher interface {
	Publish(ctx context.Context, event domain.OutboxEvent) error
}
type Relay struct {
	store     OutboxStore
	publisher Publisher
	logger    *slog.Logger
	interval  time.Duration
	batchSize int
}

func New(store OutboxStore, publisher Publisher, logger *slog.Logger, interval time.Duration, batchSize int) *Relay {
	if interval <= 0 {
		interval = time.Second
	}
	if batchSize <= 0 {
		batchSize = 50
	}
	return &Relay{
		store:     store,
		publisher: publisher,
		logger:    logger,
		interval:  interval,
		batchSize: batchSize,
	}
}
func (r *Relay) Run(ctx context.Context) error {
	ticker := time.NewTicker(r.interval)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			return ctx.Err()
		case <-ticker.C:
			if err := r.PollOnce(ctx); err != nil {
				r.logger.Error("relay poll failed", "err", err)
			}
		}
	}
}
func (r *Relay) PollOnce(ctx context.Context) error {
	events, err := r.store.ListUnpublishedOutbox(ctx, r.batchSize)
	if err != nil {
		return err
	}
	if len(events) == 0 {
		return nil
	}

	for _, event := range events {
		if err := r.publisher.Publish(ctx, event); err != nil {
			return err
		}
		if err := r.store.MarkOutboxPublished(ctx, event.ID); err != nil {
			return err
		}
	}
	return nil
}

type LogPublisher struct {
	logger *slog.Logger
}

func NewLogPublisher(logger *slog.Logger) *LogPublisher {
	return &LogPublisher{logger: logger}
}
func (p *LogPublisher) Publish(_ context.Context, event domain.OutboxEvent) error {
	p.logger.Info(
		"outbox event published",
		"event_id", event.ID,
		"aggregate_id", event.AggregateID,
		"event_type", event.EventType,
		"payload", string(event.PayloadJSON),
	)
	return nil
}
