// Package outbox defines the outbox event model and repository.
package outbox

import (
	"encoding/json"
	"time"
)

// Event represents a row in the outbox table.
type Event struct {
	ID            string          `json:"id"`
	AggregateType string          `json:"aggregate_type"`
	AggregateID   string          `json:"aggregate_id"`
	EventType     string          `json:"event_type"`
	Payload       json.RawMessage `json:"payload"`
	CreatedAt     time.Time       `json:"created_at"`
	PublishedAt   *time.Time      `json:"published_at,omitempty"`
}

// PurchasePayload is the event payload for a PurchaseCompleted event.
type PurchasePayload struct {
	PlayerID   string    `json:"player_id"`
	ItemName   string    `json:"item_name"`
	Price      int64     `json:"price"`
	NewBalance int64     `json:"new_balance"`
	Timestamp  time.Time `json:"timestamp"`
}
