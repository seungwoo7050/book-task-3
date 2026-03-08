package service

import "testing"

func TestValidatePurchaseRequest(t *testing.T) {
	tests := []struct {
		name    string
		req     PurchaseRequest
		wantErr bool
	}{
		{
			name: "valid request",
			req: PurchaseRequest{
				PlayerID:       "player-1",
				ItemID:         "item-1",
				IdempotencyKey: "idem-1",
			},
		},
		{
			name: "missing idempotency key",
			req: PurchaseRequest{
				PlayerID: "player-1",
				ItemID:   "item-1",
			},
			wantErr: true,
		},
		{
			name: "missing player id",
			req: PurchaseRequest{
				ItemID:         "item-1",
				IdempotencyKey: "idem-1",
			},
			wantErr: true,
		},
		{
			name: "missing item id",
			req: PurchaseRequest{
				PlayerID:       "player-1",
				IdempotencyKey: "idem-1",
			},
			wantErr: true,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			err := ValidatePurchaseRequest(tc.req)
			if (err != nil) != tc.wantErr {
				t.Fatalf("ValidatePurchaseRequest(%+v) err=%v, wantErr=%v", tc.req, err, tc.wantErr)
			}
		})
	}
}
