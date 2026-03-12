package worker

import (
	"context"
	"encoding/json"
	"testing"

	"github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/repository"
)

type fakeStore struct {
	events         []repository.OutboxEvent
	recipients     []repository.Recipient
	notifications  []repository.Notification
	publishedEvent []string
}

func (f *fakeStore) ListUnpublishedOutbox(context.Context, int) ([]repository.OutboxEvent, error) {
	return f.events, nil
}

func (f *fakeStore) ListRecipients(context.Context, string, string) ([]repository.Recipient, error) {
	return f.recipients, nil
}

func (f *fakeStore) CreateNotification(_ context.Context, notification repository.Notification) error {
	f.notifications = append(f.notifications, notification)
	return nil
}

func (f *fakeStore) MarkOutboxPublished(_ context.Context, eventID string) error {
	f.publishedEvent = append(f.publishedEvent, eventID)
	return nil
}

type fakeCache struct {
	deleted []string
}

func (f *fakeCache) DeleteDashboardSummary(_ context.Context, organizationID string) error {
	f.deleted = append(f.deleted, organizationID)
	return nil
}

func TestRunOncePublishesNotifications(t *testing.T) {
	t.Parallel()

	payload, err := json.Marshal(map[string]any{
		"issue_id": "issue-1",
		"title":    "Add pagination",
	})
	if err != nil {
		t.Fatalf("marshal payload: %v", err)
	}

	store := &fakeStore{
		events: []repository.OutboxEvent{{
			ID:             "event-1",
			OrganizationID: "org-1",
			EventType:      "issue.created",
			ActorUserID:    "user-1",
			PayloadJSON:    payload,
		}},
		recipients: []repository.Recipient{
			{UserID: "user-2", DisplayName: "Alice"},
			{UserID: "user-3", DisplayName: "Bob"},
		},
	}
	cache := &fakeCache{}
	processor := New(store, cache, nil, nil)

	processed, err := processor.RunOnce(context.Background())
	if err != nil {
		t.Fatalf("RunOnce() error = %v", err)
	}
	if processed != 1 {
		t.Fatalf("RunOnce() processed = %d, want 1", processed)
	}
	if len(store.notifications) != 2 {
		t.Fatalf("notifications = %d, want 2", len(store.notifications))
	}
	if got := store.notifications[0].Title; got != "New issue created" {
		t.Fatalf("title = %q, want %q", got, "New issue created")
	}
	if len(store.publishedEvent) != 1 || store.publishedEvent[0] != "event-1" {
		t.Fatalf("published events = %#v", store.publishedEvent)
	}
	if len(cache.deleted) != 1 || cache.deleted[0] != "org-1" {
		t.Fatalf("cache deleted = %#v", cache.deleted)
	}
}
