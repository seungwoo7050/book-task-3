package outbox

import (
	"encoding/json"
	"testing"
	"time"
)

func TestPurchasePayloadMarshal(t *testing.T) {
	tests := []struct {
		name    string
		payload PurchasePayload
		wantKey string // a key that must appear in JSON
	}{
		{
			name: "basic purchase",
			payload: PurchasePayload{
				PlayerID:   "player-1",
				ItemName:   "sword",
				Price:      100,
				NewBalance: 900,
				Timestamp:  time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC),
			},
			wantKey: "player_id",
		},
		{
			name: "zero balance",
			payload: PurchasePayload{
				PlayerID:   "player-2",
				ItemName:   "shield",
				Price:      500,
				NewBalance: 0,
				Timestamp:  time.Date(2024, 6, 15, 12, 0, 0, 0, time.UTC),
			},
			wantKey: "new_balance",
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			data, err := json.Marshal(tc.payload)
			if err != nil {
				t.Fatalf("Marshal: %v", err)
			}

			var m map[string]interface{}
			if err := json.Unmarshal(data, &m); err != nil {
				t.Fatalf("Unmarshal: %v", err)
			}

			if _, ok := m[tc.wantKey]; !ok {
				t.Errorf("JSON missing key %q: %s", tc.wantKey, data)
			}
		})
	}
}

func TestEventModel(t *testing.T) {
	now := time.Now()
	e := Event{
		ID:            "evt-1",
		AggregateType: "player",
		AggregateID:   "p-1",
		EventType:     "PurchaseCompleted",
		Payload:       json.RawMessage(`{"item":"sword"}`),
		CreatedAt:     now,
	}

	if e.PublishedAt != nil {
		t.Error("new event should have nil PublishedAt")
	}

	pubTime := now.Add(time.Second)
	e.PublishedAt = &pubTime
	if e.PublishedAt == nil {
		t.Error("PublishedAt should be set")
	}
}
