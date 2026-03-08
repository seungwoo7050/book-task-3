package service

import (
	"context"
	"errors"
	"strings"

	"github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/domain"
	"github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/repository"
)

var (
	// ErrPurchaseIDRequired indicates missing purchase id input.
	ErrPurchaseIDRequired = errors.New("purchase_id is required")
	// ErrPlayerIDRequired indicates missing player id input.
	ErrPlayerIDRequired = errors.New("player_id is required")
)

// QueryService handles read APIs.
type QueryService struct {
	store *repository.Store
}

// NewQueryService creates QueryService.
func NewQueryService(store *repository.Store) *QueryService {
	return &QueryService{store: store}
}

// GetPurchase returns one purchase.
func (s *QueryService) GetPurchase(ctx context.Context, purchaseID string) (domain.Purchase, error) {
	if strings.TrimSpace(purchaseID) == "" {
		return domain.Purchase{}, ErrPurchaseIDRequired
	}
	return s.store.GetPurchase(ctx, purchaseID)
}

// GetInventory returns player inventory list.
func (s *QueryService) GetInventory(ctx context.Context, playerID string) ([]domain.InventoryItem, error) {
	if strings.TrimSpace(playerID) == "" {
		return nil, ErrPlayerIDRequired
	}
	return s.store.ListInventory(ctx, playerID)
}
