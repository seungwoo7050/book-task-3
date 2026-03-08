package consumer

import (
	"testing"

	"github.com/segmentio/kafka-go"
)

func TestGetHeader(t *testing.T) {
	tests := []struct {
		name    string
		headers []kafka.Header
		key     string
		want    string
	}{
		{
			name: "found",
			headers: []kafka.Header{
				{Key: "event_type", Value: []byte("PurchaseCompleted")},
				{Key: "event_id", Value: []byte("abc-123")},
			},
			key:  "event_id",
			want: "abc-123",
		},
		{
			name: "not found",
			headers: []kafka.Header{
				{Key: "event_type", Value: []byte("PurchaseCompleted")},
			},
			key:  "event_id",
			want: "",
		},
		{
			name:    "empty headers",
			headers: nil,
			key:     "event_id",
			want:    "",
		},
		{
			name: "first match wins",
			headers: []kafka.Header{
				{Key: "x", Value: []byte("first")},
				{Key: "x", Value: []byte("second")},
			},
			key:  "x",
			want: "first",
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			got := getHeader(tc.headers, tc.key)
			if got != tc.want {
				t.Errorf("getHeader(%q) = %q, want %q", tc.key, got, tc.want)
			}
		})
	}
}

func TestConsumerIdempotency(t *testing.T) {
	c := &Consumer{
		processed: make(map[string]struct{}),
	}

	// Initially not processed.
	if c.isProcessed("evt-1") {
		t.Error("evt-1 should not be processed initially")
	}

	// Mark as processed.
	c.markProcessed("evt-1")

	// Now it should be processed.
	if !c.isProcessed("evt-1") {
		t.Error("evt-1 should be processed after markProcessed")
	}

	// Other events still not processed.
	if c.isProcessed("evt-2") {
		t.Error("evt-2 should not be processed")
	}
}
