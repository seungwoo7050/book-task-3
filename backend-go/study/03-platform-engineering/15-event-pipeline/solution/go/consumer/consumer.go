// Package consumer는 at-least-once 전달을 전제로 동작하는 Kafka 소비자를 구현한다.
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

// Handler는 단일 이벤트를 처리한다.
// 중복 전달 가능성이 있으므로 구현은 멱등적이어야 한다.
type Handler func(ctx context.Context, eventType string, payload json.RawMessage) error

// Consumer는 Kafka 메시지를 읽고 중복 여부를 확인한 뒤 처리한다.
type Consumer struct {
	reader  *kafka.Reader
	db      *sql.DB
	handler Handler
	logger  *slog.Logger

	// 최근 처리 이력을 메모리에 유지해 같은 프로세스 안에서 빠르게 중복을 걸러낸다.
	mu        sync.RWMutex
	processed map[string]struct{}
}

// New는 Kafka consumer 인스턴스를 생성한다.
func New(reader *kafka.Reader, db *sql.DB, handler Handler, logger *slog.Logger) *Consumer {
	return &Consumer{
		reader:    reader,
		db:        db,
		handler:   handler,
		logger:    logger,
		processed: make(map[string]struct{}),
	}
}

// Run은 메시지 처리 루프를 시작하고 ctx가 취소될 때까지 계속 실행한다.
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

		// 먼저 메모리와 DB를 확인해 중복 메시지를 건너뛴다.
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
			// 커밋하지 않으면 Kafka가 같은 메시지를 다시 전달한다.
			continue
		}

		// 처리 완료 후 메모리/DB에 반영한다.
		c.markProcessed(eventID)
		c.persistProcessed(ctx, eventID)

		// 마지막으로 오프셋을 커밋해 재전달을 막는다.
		c.commitMessage(ctx, msg)
	}
}

// isProcessed는 메모리 캐시에 이벤트 ID가 있는지 확인한다.
func (c *Consumer) isProcessed(eventID string) bool {
	c.mu.RLock()
	defer c.mu.RUnlock()
	_, ok := c.processed[eventID]
	return ok
}

// markProcessed는 이벤트 ID를 메모리 캐시에 추가한다.
func (c *Consumer) markProcessed(eventID string) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.processed[eventID] = struct{}{}
}

// isPersisted는 DB에 이미 처리 이력이 저장됐는지 확인한다.
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

// persistProcessed는 이벤트 ID를 processed_events 테이블에 저장한다.
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

// commitMessage는 메시지 오프셋을 Kafka에 커밋한다.
func (c *Consumer) commitMessage(ctx context.Context, msg kafka.Message) {
	if err := c.reader.CommitMessages(ctx, msg); err != nil {
		c.logger.Error("commit failed",
			"offset", msg.Offset,
			"err", err,
		)
	}
}

// getHeader는 Kafka 헤더 목록에서 지정 키의 값을 찾는다.
func getHeader(headers []kafka.Header, key string) string {
	for _, h := range headers {
		if h.Key == key {
			return string(h.Value)
		}
	}
	return ""
}
