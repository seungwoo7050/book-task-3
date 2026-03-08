package repository

import (
	"context"
	"database/sql"
	"encoding/json"
	"errors"
	"fmt"
	"time"

	"github.com/google/uuid"

	"github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/domain"
)

// ErrConflict indicates optimistic locking conflict on balance update.
var ErrConflict = errors.New("optimistic locking conflict")

// ErrIdempotencyKeyExists indicates duplicate key insertion race.
var ErrIdempotencyKeyExists = errors.New("idempotency key already exists")

// Store provides DB access for purchase, inventory, idempotency, and outbox.
type Store struct {
	db *sql.DB
}

// NewStore creates a new Store.
func NewStore(db *sql.DB) *Store {
	return &Store{db: db}
}

// GetPlayer fetches player state in transaction context.
func (s *Store) GetPlayer(ctx context.Context, tx *sql.Tx, playerID string) (domain.Player, error) {
	var p domain.Player
	err := tx.QueryRowContext(ctx,
		`SELECT id, name, balance, version, created_at
		 FROM players WHERE id = $1`,
		playerID,
	).Scan(&p.ID, &p.Name, &p.Balance, &p.Version, &p.CreatedAt)
	if err != nil {
		return domain.Player{}, err
	}
	return p, nil
}

// GetCatalogItem fetches catalog metadata and price.
func (s *Store) GetCatalogItem(ctx context.Context, tx *sql.Tx, itemID string) (domain.CatalogItem, error) {
	var item domain.CatalogItem
	err := tx.QueryRowContext(ctx,
		`SELECT id, sku, name, price, created_at
		 FROM catalog_items WHERE id = $1`,
		itemID,
	).Scan(&item.ID, &item.SKU, &item.Name, &item.Price, &item.CreatedAt)
	if err != nil {
		return domain.CatalogItem{}, err
	}
	return item, nil
}

// DeductBalance updates player balance with version check.
func (s *Store) DeductBalance(ctx context.Context, tx *sql.Tx, playerID string, amount int64, expectedVersion int64) (int64, int64, error) {
	var newBalance int64
	var newVersion int64
	err := tx.QueryRowContext(ctx,
		`UPDATE players
		 SET balance = balance - $1, version = version + 1
		 WHERE id = $2
		   AND version = $3
		   AND balance >= $1
		 RETURNING balance, version`,
		amount, playerID, expectedVersion,
	).Scan(&newBalance, &newVersion)
	if errors.Is(err, sql.ErrNoRows) {
		return 0, 0, ErrConflict
	}
	if err != nil {
		return 0, 0, err
	}
	return newBalance, newVersion, nil
}

// UpsertInventory increments owned item quantity.
func (s *Store) UpsertInventory(ctx context.Context, tx *sql.Tx, playerID, itemID string, qty int) error {
	_, err := tx.ExecContext(ctx,
		`INSERT INTO inventories (id, player_id, item_id, qty, updated_at)
		 VALUES ($1, $2, $3, $4, now())
		 ON CONFLICT (player_id, item_id)
		 DO UPDATE
		 SET qty = inventories.qty + EXCLUDED.qty,
		     updated_at = now()`,
		uuid.NewString(), playerID, itemID, qty,
	)
	return err
}

// CreatePurchase inserts a purchase row and returns stored record.
func (s *Store) CreatePurchase(ctx context.Context, tx *sql.Tx, purchaseID, playerID, itemID string, price int64) (domain.Purchase, error) {
	var p domain.Purchase
	err := tx.QueryRowContext(ctx,
		`INSERT INTO purchases (id, player_id, item_id, price)
		 VALUES ($1, $2, $3, $4)
		 RETURNING id, player_id, item_id, price, created_at`,
		purchaseID, playerID, itemID, price,
	).Scan(&p.ID, &p.PlayerID, &p.ItemID, &p.Price, &p.CreatedAt)
	if err != nil {
		return domain.Purchase{}, err
	}
	return p, nil
}

// GetIdempotencyKey fetches a cached response by key.
func (s *Store) GetIdempotencyKey(ctx context.Context, tx *sql.Tx, key string) (domain.IdempotencyRecord, error) {
	var rec domain.IdempotencyRecord
	err := tx.QueryRowContext(ctx,
		`SELECT key, request_hash, response_json, created_at
		 FROM idempotency_keys
		 WHERE key = $1`,
		key,
	).Scan(&rec.Key, &rec.RequestHash, &rec.Response, &rec.CreatedAt)
	if err != nil {
		return domain.IdempotencyRecord{}, err
	}
	return rec, nil
}

// InsertIdempotencyKey stores request hash and response payload.
func (s *Store) InsertIdempotencyKey(ctx context.Context, tx *sql.Tx, key, requestHash string, response json.RawMessage) error {
	_, err := tx.ExecContext(ctx,
		`INSERT INTO idempotency_keys (key, request_hash, response_json)
		 VALUES ($1, $2, $3)`,
		key, requestHash, response,
	)
	if isUniqueViolation(err) {
		return ErrIdempotencyKeyExists
	}
	return err
}

// InsertOutboxEvent appends a domain event in the same transaction.
func (s *Store) InsertOutboxEvent(ctx context.Context, tx *sql.Tx, eventID, aggregateID, eventType string, payload json.RawMessage) error {
	_, err := tx.ExecContext(ctx,
		`INSERT INTO outbox (id, aggregate_id, event_type, payload_json)
		 VALUES ($1, $2, $3, $4)`,
		eventID, aggregateID, eventType, payload,
	)
	return err
}

// GetPurchase returns purchase by id.
func (s *Store) GetPurchase(ctx context.Context, purchaseID string) (domain.Purchase, error) {
	var p domain.Purchase
	err := s.db.QueryRowContext(ctx,
		`SELECT id, player_id, item_id, price, created_at
		 FROM purchases
		 WHERE id = $1`,
		purchaseID,
	).Scan(&p.ID, &p.PlayerID, &p.ItemID, &p.Price, &p.CreatedAt)
	if err != nil {
		return domain.Purchase{}, err
	}
	return p, nil
}

// ListInventory returns player's inventory with catalog metadata.
func (s *Store) ListInventory(ctx context.Context, playerID string) ([]domain.InventoryItem, error) {
	rows, err := s.db.QueryContext(ctx,
		`SELECT i.item_id, c.sku, c.name, i.qty, i.updated_at
		 FROM inventories i
		 INNER JOIN catalog_items c ON c.id = i.item_id
		 WHERE i.player_id = $1
		 ORDER BY i.updated_at DESC`,
		playerID,
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	items := make([]domain.InventoryItem, 0)
	for rows.Next() {
		var item domain.InventoryItem
		if err := rows.Scan(&item.ItemID, &item.SKU, &item.Name, &item.Qty, &item.UpdatedAt); err != nil {
			return nil, err
		}
		items = append(items, item)
	}
	if err := rows.Err(); err != nil {
		return nil, err
	}
	return items, nil
}

// ListUnpublishedOutbox loads unpublished events ordered by created_at.
func (s *Store) ListUnpublishedOutbox(ctx context.Context, limit int) ([]domain.OutboxEvent, error) {
	rows, err := s.db.QueryContext(ctx,
		`SELECT id, aggregate_id, event_type, payload_json, created_at, published_at
		 FROM outbox
		 WHERE published_at IS NULL
		 ORDER BY created_at ASC
		 LIMIT $1`,
		limit,
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	events := make([]domain.OutboxEvent, 0)
	for rows.Next() {
		var e domain.OutboxEvent
		if err := rows.Scan(&e.ID, &e.AggregateID, &e.EventType, &e.PayloadJSON, &e.CreatedAt, &e.PublishedAt); err != nil {
			return nil, err
		}
		events = append(events, e)
	}
	if err := rows.Err(); err != nil {
		return nil, err
	}
	return events, nil
}

// MarkOutboxPublished sets published_at for a delivered event.
func (s *Store) MarkOutboxPublished(ctx context.Context, eventID string) error {
	result, err := s.db.ExecContext(ctx,
		`UPDATE outbox SET published_at = now() WHERE id = $1`,
		eventID,
	)
	if err != nil {
		return err
	}
	n, err := result.RowsAffected()
	if err != nil {
		return err
	}
	if n == 0 {
		return fmt.Errorf("outbox event not found: %s", eventID)
	}
	return nil
}

// LastPublishedAt returns latest published timestamp for debugging.
func (s *Store) LastPublishedAt(ctx context.Context) (*time.Time, error) {
	var ts sql.NullTime
	err := s.db.QueryRowContext(ctx, `SELECT max(published_at) FROM outbox`).Scan(&ts)
	if err != nil {
		return nil, err
	}
	if !ts.Valid {
		return nil, nil
	}
	t := ts.Time
	return &t, nil
}

func isUniqueViolation(err error) bool {
	type sqlStateError interface {
		error
		SQLState() string
	}
	var se sqlStateError
	return errors.As(err, &se) && se.SQLState() == "23505"
}
