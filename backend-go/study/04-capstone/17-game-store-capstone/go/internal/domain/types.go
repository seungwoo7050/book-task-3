package domain

import (
	"encoding/json"
	"time"
)

// Player is the account owner for purchases.
type Player struct {
	ID        string
	Name      string
	Balance   int64
	Version   int64
	CreatedAt time.Time
}

// CatalogItem is a sellable item.
type CatalogItem struct {
	ID        string
	SKU       string
	Name      string
	Price     int64
	CreatedAt time.Time
}

// Purchase is the immutable purchase history row.
type Purchase struct {
	ID        string    `json:"id"`
	PlayerID  string    `json:"player_id"`
	ItemID    string    `json:"item_id"`
	Price     int64     `json:"price"`
	CreatedAt time.Time `json:"created_at"`
}

// InventoryItem is the player's owned catalog item summary.
type InventoryItem struct {
	ItemID    string    `json:"item_id"`
	SKU       string    `json:"sku"`
	Name      string    `json:"name"`
	Qty       int       `json:"qty"`
	UpdatedAt time.Time `json:"updated_at"`
}

// IdempotencyRecord stores a request hash and cached response.
type IdempotencyRecord struct {
	Key         string
	RequestHash string
	Response    json.RawMessage
	CreatedAt   time.Time
}

// OutboxEvent is a relay target row.
type OutboxEvent struct {
	ID          string          `json:"id"`
	AggregateID string          `json:"aggregate_id"`
	EventType   string          `json:"event_type"`
	PayloadJSON json.RawMessage `json:"payload_json"`
	CreatedAt   time.Time       `json:"created_at"`
	PublishedAt *time.Time      `json:"published_at,omitempty"`
}
