package service

import (
	"context"
	"errors"
	"strings"

	"github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/domain"
	"github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/repository"
)

var (
	// ErrPurchaseIDRequired는 구매 ID가 비어 있을 때 반환된다.
	ErrPurchaseIDRequired = errors.New("purchase_id is required")
	// ErrPlayerIDRequired는 플레이어 ID가 비어 있을 때 반환된다.
	ErrPlayerIDRequired = errors.New("player_id is required")
)

// QueryService는 구매 조회와 인벤토리 조회를 담당한다.
type QueryService struct {
	store *repository.Store
}

// NewQueryService는 QueryService를 생성한다.
func NewQueryService(store *repository.Store) *QueryService {
	return &QueryService{store: store}
}

// GetPurchase는 구매 ID로 구매 정보를 조회한다.
func (s *QueryService) GetPurchase(ctx context.Context, purchaseID string) (domain.Purchase, error) {
	if strings.TrimSpace(purchaseID) == "" {
		return domain.Purchase{}, ErrPurchaseIDRequired
	}
	return s.store.GetPurchase(ctx, purchaseID)
}

// GetInventory는 플레이어 인벤토리 목록을 조회한다.
func (s *QueryService) GetInventory(ctx context.Context, playerID string) ([]domain.InventoryItem, error) {
	if strings.TrimSpace(playerID) == "" {
		return nil, ErrPlayerIDRequired
	}
	return s.store.ListInventory(ctx, playerID)
}
