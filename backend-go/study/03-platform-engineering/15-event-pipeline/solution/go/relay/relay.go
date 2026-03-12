// Package relay는 outbox 테이블의 이벤트를 Kafka로 전달하는 릴레이를 구현한다.
package relay

import (
	"context"
	"log/slog"
	"time"

	"github.com/segmentio/kafka-go"

	"github.com/woopinbell/go-backend/study/03-platform-engineering/15-event-pipeline/outbox"
)

// Relay는 outbox 테이블을 주기적으로 조회해 Kafka에 이벤트를 발행한다.
type Relay struct {
	repo     *outbox.Repository
	writer   *kafka.Writer
	logger   *slog.Logger
	interval time.Duration
	batch    int
}

// Config는 릴레이의 폴링 간격과 배치 크기를 정의한다.
type Config struct {
	PollInterval time.Duration
	BatchSize    int
}

// New는 outbox 릴레이를 생성한다.
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

// Run은 ctx가 취소될 때까지 폴링 루프를 실행한다.
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

// poll은 미발행 outbox 이벤트를 읽어 Kafka로 전달한다.
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
			// mark 단계가 실패하면 다음 poll에서 다시 발행될 수 있다.
			// 이 프로젝트는 at-least-once 전달을 전제로 한다.
		}

		r.logger.Info("event published",
			"event_id", event.ID,
			"type", event.EventType,
			"aggregate", event.AggregateID,
		)
	}

	return nil
}
