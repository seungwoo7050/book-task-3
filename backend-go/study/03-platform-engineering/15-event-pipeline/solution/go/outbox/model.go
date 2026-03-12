// Package outbox는 outbox 이벤트 모델과 저장소를 정의한다.
package outbox

import (
	"encoding/json"
	"time"
)

// Event는 outbox 테이블의 한 행을 나타낸다.
type Event struct {
	ID            string          `json:"id"`
	AggregateType string          `json:"aggregate_type"`
	AggregateID   string          `json:"aggregate_id"`
	EventType     string          `json:"event_type"`
	Payload       json.RawMessage `json:"payload"`
	CreatedAt     time.Time       `json:"created_at"`
	PublishedAt   *time.Time      `json:"published_at,omitempty"`
}

// PurchasePayload는 구매 완료 이벤트에 담기는 페이로드다.
type PurchasePayload struct {
	PlayerID   string    `json:"player_id"`
	ItemName   string    `json:"item_name"`
	Price      int64     `json:"price"`
	NewBalance int64     `json:"new_balance"`
	Timestamp  time.Time `json:"timestamp"`
}
