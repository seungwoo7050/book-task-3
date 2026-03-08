package outbox

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
)

// Repository provides data-access methods for the outbox table.
type Repository struct {
	DB *sql.DB
}

// NewRepository creates a new outbox repository.
func NewRepository(db *sql.DB) *Repository {
	return &Repository{DB: db}
}

// InsertTx inserts an outbox event within an existing transaction.
// This is used inside the purchase transaction to ensure atomicity.
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

// GetUnpublished returns up to limit unpublished events ordered by creation time.
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

// MarkPublished sets the published_at timestamp for the given event ID.
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

// Cleanup deletes published events older than the given interval.
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
