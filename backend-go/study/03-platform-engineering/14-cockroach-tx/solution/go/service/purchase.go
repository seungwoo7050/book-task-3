package service

import (
	"context"
	"database/sql"
	"encoding/json"
	"errors"
	"fmt"

	"github.com/woopinbell/go-backend/study/03-platform-engineering/14-cockroach-tx/repository"
	"github.com/woopinbell/go-backend/study/03-platform-engineering/14-cockroach-tx/txn"
)

type PurchaseRequest struct {
	IdempotencyKey string `json:"idempotency_key"`
	PlayerID       string `json:"player_id"`
	ItemName       string `json:"item_name"`
	Price          int64  `json:"price"`
}
type PurchaseResponse struct {
	Status     string `json:"status"`
	NewBalance int64  `json:"new_balance"`
	Item       string `json:"item"`
}
type PurchaseService struct {
	DB         *sql.DB
	MaxRetries int
}

func NewPurchaseService(db *sql.DB) *PurchaseService {
	return &PurchaseService{
		DB:         db,
		MaxRetries: 3,
	}
}
func (s *PurchaseService) Purchase(ctx context.Context, req PurchaseRequest) (*PurchaseResponse, error) {
	var resp *PurchaseResponse

	err := txn.RunInTx(ctx, s.DB, s.MaxRetries, func(tx *sql.Tx) error {
		cached, err := repository.GetIdempotencyKey(ctx, tx, req.IdempotencyKey)
		if err == nil {
			var cachedResp PurchaseResponse
			if err := json.Unmarshal(cached, &cachedResp); err != nil {
				return fmt.Errorf("unmarshal cached response: %w", err)
			}
			resp = &cachedResp
			return nil
		}
		if !errors.Is(err, sql.ErrNoRows) {
			return fmt.Errorf("check idempotency key: %w", err)
		}
		player, err := repository.GetPlayer(ctx, tx, req.PlayerID)
		if err != nil {
			return fmt.Errorf("get player: %w", err)
		}

		if player.Balance < req.Price {
			return fmt.Errorf("insufficient balance: have %d, need %d", player.Balance, req.Price)
		}
		newBalance, _, err := repository.DeductBalance(ctx, tx, req.PlayerID, req.Price, player.Version)
		if err != nil {
			if errors.Is(err, repository.ErrConflict) {
				return repository.ErrConflict
			}
			return fmt.Errorf("deduct balance: %w", err)
		}
		if err := repository.UpsertInventory(ctx, tx, req.PlayerID, req.ItemName, 1); err != nil {
			return fmt.Errorf("upsert inventory: %w", err)
		}
		auditDetail := map[string]interface{}{
			"item":    req.ItemName,
			"price":   req.Price,
			"balance": newBalance,
		}
		if err := repository.InsertAuditLog(ctx, tx, req.PlayerID, "purchase", auditDetail); err != nil {
			return fmt.Errorf("insert audit log: %w", err)
		}
		resp = &PurchaseResponse{
			Status:     "ok",
			NewBalance: newBalance,
			Item:       req.ItemName,
		}

		respJSON, err := json.Marshal(resp)
		if err != nil {
			return fmt.Errorf("marshal response: %w", err)
		}

		if err := repository.InsertIdempotencyKey(ctx, tx, req.IdempotencyKey, req.PlayerID, respJSON); err != nil {
			return fmt.Errorf("insert idempotency key: %w", err)
		}

		return nil
	})

	if err != nil {
		return nil, err
	}
	return resp, nil
}
