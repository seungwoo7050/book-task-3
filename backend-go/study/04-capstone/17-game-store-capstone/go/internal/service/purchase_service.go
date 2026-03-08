package service

import (
	"context"
	"crypto/sha256"
	"database/sql"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"strings"
	"time"

	"github.com/google/uuid"

	"github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/repository"
	"github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/txn"
)

var (
	// ErrPlayerNotFound means the requested player id does not exist.
	ErrPlayerNotFound = errors.New("player not found")
	// ErrItemNotFound means the requested catalog item id does not exist.
	ErrItemNotFound = errors.New("catalog item not found")
	// ErrInsufficientBalance means player balance is not enough for item price.
	ErrInsufficientBalance = errors.New("insufficient balance")
	// ErrIdempotencyKeyConflict means same key was reused with different payload.
	ErrIdempotencyKeyConflict = errors.New("idempotency key conflict")
)

// ValidationError is a bad client input error.
type ValidationError struct {
	Field   string
	Message string
}

func (e *ValidationError) Error() string {
	return fmt.Sprintf("%s: %s", e.Field, e.Message)
}

type retryableTxError struct {
	msg string
}

func (e *retryableTxError) Error() string {
	return e.msg
}

func (e *retryableTxError) SQLState() string {
	return txn.RetryableErrorCode
}

// PurchaseRequest is the input to purchase use-case.
type PurchaseRequest struct {
	PlayerID       string
	ItemID         string
	IdempotencyKey string
}

// PurchaseResponse is returned by the purchase API.
type PurchaseResponse struct {
	PurchaseID string    `json:"purchase_id"`
	PlayerID   string    `json:"player_id"`
	ItemID     string    `json:"item_id"`
	Price      int64     `json:"price"`
	NewBalance int64     `json:"new_balance"`
	Status     string    `json:"status"`
	CreatedAt  time.Time `json:"created_at"`
}

// PurchaseService orchestrates an idempotent purchase transaction.
type PurchaseService struct {
	db         *sql.DB
	store      *repository.Store
	maxRetries int
}

// NewPurchaseService creates purchase service with defaults.
func NewPurchaseService(db *sql.DB, store *repository.Store) *PurchaseService {
	return &PurchaseService{
		db:         db,
		store:      store,
		maxRetries: 3,
	}
}

// Purchase executes one purchase operation.
func (s *PurchaseService) Purchase(ctx context.Context, req PurchaseRequest) (*PurchaseResponse, error) {
	if err := ValidatePurchaseRequest(req); err != nil {
		return nil, err
	}

	requestHash := buildRequestHash(req.PlayerID, req.ItemID)
	var response *PurchaseResponse

	err := txn.RunInTx(ctx, s.db, s.maxRetries, func(tx *sql.Tx) error {
		cached, err := s.store.GetIdempotencyKey(ctx, tx, req.IdempotencyKey)
		if err == nil {
			if cached.RequestHash != requestHash {
				return ErrIdempotencyKeyConflict
			}
			var cachedResp PurchaseResponse
			if err := json.Unmarshal(cached.Response, &cachedResp); err != nil {
				return fmt.Errorf("unmarshal cached response: %w", err)
			}
			response = &cachedResp
			return nil
		}
		if !errors.Is(err, sql.ErrNoRows) {
			return fmt.Errorf("get idempotency key: %w", err)
		}

		player, err := s.store.GetPlayer(ctx, tx, req.PlayerID)
		if errors.Is(err, sql.ErrNoRows) {
			return ErrPlayerNotFound
		}
		if err != nil {
			return fmt.Errorf("get player: %w", err)
		}

		item, err := s.store.GetCatalogItem(ctx, tx, req.ItemID)
		if errors.Is(err, sql.ErrNoRows) {
			return ErrItemNotFound
		}
		if err != nil {
			return fmt.Errorf("get catalog item: %w", err)
		}

		if player.Balance < item.Price {
			return ErrInsufficientBalance
		}

		newBalance, _, err := s.store.DeductBalance(ctx, tx, player.ID, item.Price, player.Version)
		if err != nil {
			if errors.Is(err, repository.ErrConflict) {
				return repository.ErrConflict
			}
			return fmt.Errorf("deduct balance: %w", err)
		}

		purchaseID := uuid.NewString()
		purchase, err := s.store.CreatePurchase(ctx, tx, purchaseID, player.ID, item.ID, item.Price)
		if err != nil {
			return fmt.Errorf("create purchase: %w", err)
		}

		if err := s.store.UpsertInventory(ctx, tx, player.ID, item.ID, 1); err != nil {
			return fmt.Errorf("upsert inventory: %w", err)
		}

		eventPayload, err := json.Marshal(map[string]any{
			"purchase_id": purchase.ID,
			"player_id":   purchase.PlayerID,
			"item_id":     purchase.ItemID,
			"price":       purchase.Price,
			"created_at":  purchase.CreatedAt.UTC(),
		})
		if err != nil {
			return fmt.Errorf("marshal outbox payload: %w", err)
		}

		if err := s.store.InsertOutboxEvent(
			ctx,
			tx,
			uuid.NewString(),
			purchase.ID,
			"purchase.completed",
			eventPayload,
		); err != nil {
			return fmt.Errorf("insert outbox event: %w", err)
		}

		response = &PurchaseResponse{
			PurchaseID: purchase.ID,
			PlayerID:   purchase.PlayerID,
			ItemID:     purchase.ItemID,
			Price:      purchase.Price,
			NewBalance: newBalance,
			Status:     "ok",
			CreatedAt:  purchase.CreatedAt,
		}

		responseJSON, err := json.Marshal(response)
		if err != nil {
			return fmt.Errorf("marshal purchase response: %w", err)
		}

		if err := s.store.InsertIdempotencyKey(ctx, tx, req.IdempotencyKey, requestHash, responseJSON); err != nil {
			if errors.Is(err, repository.ErrIdempotencyKeyExists) {
				// Another in-flight request inserted the same key first.
				// Retry the transaction so the next attempt can read cached response.
				return &retryableTxError{msg: "idempotency key collision, retry"}
			}
			return fmt.Errorf("insert idempotency key: %w", err)
		}

		return nil
	})
	if err != nil {
		return nil, err
	}

	return response, nil
}

// ValidatePurchaseRequest validates purchase payload.
func ValidatePurchaseRequest(req PurchaseRequest) error {
	if strings.TrimSpace(req.IdempotencyKey) == "" {
		return &ValidationError{Field: "idempotency_key", Message: "required"}
	}
	if strings.TrimSpace(req.PlayerID) == "" {
		return &ValidationError{Field: "player_id", Message: "required"}
	}
	if strings.TrimSpace(req.ItemID) == "" {
		return &ValidationError{Field: "item_id", Message: "required"}
	}
	return nil
}

func buildRequestHash(playerID, itemID string) string {
	sum := sha256.Sum256([]byte(playerID + ":" + itemID))
	return hex.EncodeToString(sum[:])
}
