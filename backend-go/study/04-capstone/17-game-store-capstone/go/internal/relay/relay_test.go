package relay

import (
	"context"
	"log/slog"
	"slices"
	"testing"
	"time"

	"github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/domain"
)

type fakeStore struct {
	events  []domain.OutboxEvent
	marked  []string
	listErr error
	markErr error
}

func (f *fakeStore) ListUnpublishedOutbox(_ context.Context, limit int) ([]domain.OutboxEvent, error) {
	if f.listErr != nil {
		return nil, f.listErr
	}
	if len(f.events) > limit {
		return f.events[:limit], nil
	}
	return f.events, nil
}

func (f *fakeStore) MarkOutboxPublished(_ context.Context, eventID string) error {
	if f.markErr != nil {
		return f.markErr
	}
	f.marked = append(f.marked, eventID)
	return nil
}

type fakePublisher struct {
	published []string
	err       error
}

func (p *fakePublisher) Publish(_ context.Context, e domain.OutboxEvent) error {
	if p.err != nil {
		return p.err
	}
	p.published = append(p.published, e.ID)
	return nil
}

func TestRelayPollOnce(t *testing.T) {
	store := &fakeStore{
		events: []domain.OutboxEvent{
			{ID: "evt-1", EventType: "purchase.completed", CreatedAt: time.Now()},
			{ID: "evt-2", EventType: "purchase.completed", CreatedAt: time.Now()},
		},
	}
	pub := &fakePublisher{}

	r := New(store, pub, slog.Default(), time.Second, 10)
	if err := r.PollOnce(context.Background()); err != nil {
		t.Fatalf("PollOnce() error = %v", err)
	}

	if !slices.Equal(pub.published, []string{"evt-1", "evt-2"}) {
		t.Fatalf("published = %v, want [evt-1 evt-2]", pub.published)
	}
	if !slices.Equal(store.marked, []string{"evt-1", "evt-2"}) {
		t.Fatalf("marked = %v, want [evt-1 evt-2]", store.marked)
	}
}
