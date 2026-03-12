package service

import (
	"testing"

	"github.com/woopinbell/go-backend/study/03-platform-engineering/14-cockroach-tx/repository"
)

func TestErrConflictSentinel(t *testing.T) {
	if repository.ErrConflict == nil {
		t.Fatal("ErrConflict should not be nil")
	}
	if repository.ErrConflict.Error() != "optimistic locking conflict" {
		t.Errorf("ErrConflict message = %q", repository.ErrConflict.Error())
	}
}
func TestPurchaseRequestValidation(t *testing.T) {
	tests := []struct {
		name    string
		req     PurchaseRequest
		wantErr bool
	}{
		{
			name: "valid request",
			req: PurchaseRequest{
				IdempotencyKey: "key-1",
				PlayerID:       "player-1",
				ItemName:       "sword",
				Price:          100,
			},
			wantErr: false,
		},
		{
			name: "missing idempotency key",
			req: PurchaseRequest{
				PlayerID: "player-1",
				ItemName: "sword",
				Price:    100,
			},
			wantErr: true,
		},
		{
			name: "missing player id",
			req: PurchaseRequest{
				IdempotencyKey: "key-1",
				ItemName:       "sword",
				Price:          100,
			},
			wantErr: true,
		},
		{
			name: "zero price",
			req: PurchaseRequest{
				IdempotencyKey: "key-1",
				PlayerID:       "player-1",
				ItemName:       "sword",
				Price:          0,
			},
			wantErr: true,
		},
		{
			name: "negative price",
			req: PurchaseRequest{
				IdempotencyKey: "key-1",
				PlayerID:       "player-1",
				ItemName:       "sword",
				Price:          -50,
			},
			wantErr: true,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			err := validatePurchaseRequest(tc.req)
			if (err != nil) != tc.wantErr {
				t.Errorf("validatePurchaseRequest(%+v) err=%v, wantErr=%v", tc.req, err, tc.wantErr)
			}
		})
	}
}
func validatePurchaseRequest(req PurchaseRequest) error {
	if req.IdempotencyKey == "" {
		return &ValidationError{Field: "idempotency_key", Message: "required"}
	}
	if req.PlayerID == "" {
		return &ValidationError{Field: "player_id", Message: "required"}
	}
	if req.ItemName == "" {
		return &ValidationError{Field: "item_name", Message: "required"}
	}
	if req.Price <= 0 {
		return &ValidationError{Field: "price", Message: "must be positive"}
	}
	return nil
}

type ValidationError struct {
	Field   string
	Message string
}

func (e *ValidationError) Error() string {
	return e.Field + ": " + e.Message
}
