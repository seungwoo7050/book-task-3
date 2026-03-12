package outbox

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
)

// Repository는 outbox 테이블에 접근하는 데이터 계층이다.
type Repository struct {
	DB *sql.DB
}

// NewRepository는 outbox 저장소를 생성한다.
func NewRepository(db *sql.DB) *Repository {
	return &Repository{DB: db}
}

// InsertTx는 기존 트랜잭션 안에서 outbox 이벤트를 기록한다.
func InsertTx(ctx context.Context, tx *sql.Tx, aggregateType, aggregateID, eventType string, payload interface{}) error {
	payloadJSON, err := json.Marshal(payload)
	if err != nil {
		return fmt.Errorf("marshal payload: %w", err)
	}

	_, err = tx.ExecContext(ctx,
		`INSERT INTO outbox (aggregate_type, aggregate_id, event_type, payload)
		 VALUES ($1, $2, $3, $4)`,
		aggregateType, aggregateID, eventType, payloadJSON,
	)
	if err != nil {
		return fmt.Errorf("insert outbox: %w", err)
	}
	return nil
}

// GetUnpublished는 아직 발행되지 않은 이벤트를 생성 시각 순으로 조회한다.
func (r *Repository) GetUnpublished(ctx context.Context, limit int) ([]Event, error) {
	rows, err := r.DB.QueryContext(ctx,
		`SELECT id, aggregate_type, aggregate_id, event_type, payload, created_at
		 FROM outbox
		 WHERE published_at IS NULL
		 ORDER BY created_at ASC
		 LIMIT $1`,
		limit,
	)
	if err != nil {
		return nil, fmt.Errorf("query unpublished: %w", err)
	}
	defer rows.Close()

	var events []Event
	for rows.Next() {
		var e Event
		if err := rows.Scan(
			&e.ID, &e.AggregateType, &e.AggregateID,
			&e.EventType, &e.Payload, &e.CreatedAt,
		); err != nil {
			return nil, fmt.Errorf("scan event: %w", err)
		}
		events = append(events, e)
	}
	return events, rows.Err()
}

// MarkPublished는 지정 이벤트를 발행 완료 상태로 표시한다.
func (r *Repository) MarkPublished(ctx context.Context, eventID string) error {
	_, err := r.DB.ExecContext(ctx,
		`UPDATE outbox SET published_at = now() WHERE id = $1`,
		eventID,
	)
	if err != nil {
		return fmt.Errorf("mark published: %w", err)
	}
	return nil
}

// Cleanup은 지정한 보관 기간보다 오래된 발행 완료 이벤트를 삭제한다.
func (r *Repository) Cleanup(ctx context.Context, olderThan string) (int64, error) {
	result, err := r.DB.ExecContext(ctx,
		`DELETE FROM outbox
		 WHERE published_at IS NOT NULL
		   AND published_at < now() - $1::INTERVAL`,
		olderThan,
	)
	if err != nil {
		return 0, fmt.Errorf("cleanup: %w", err)
	}
	return result.RowsAffected()
}
