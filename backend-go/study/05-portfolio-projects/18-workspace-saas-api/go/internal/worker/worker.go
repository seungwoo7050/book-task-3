package worker

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"log/slog"
	"time"

	"github.com/google/uuid"

	"github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/platform"
	"github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/repository"
)

// Store describes the persistence operations required by the worker.
type Store interface {
	ListUnpublishedOutbox(ctx context.Context, limit int) ([]repository.OutboxEvent, error)
	ListRecipients(ctx context.Context, organizationID, excludeUserID string) ([]repository.Recipient, error)
	CreateNotification(ctx context.Context, notification repository.Notification) error
	MarkOutboxPublished(ctx context.Context, eventID string) error
}

// SummaryCache describes the cache invalidation operation needed by the worker.
type SummaryCache interface {
	DeleteDashboardSummary(ctx context.Context, organizationID string) error
}

// Processor polls the outbox table and creates notifications.
type Processor struct {
	store   Store
	cache   SummaryCache
	logger  *slog.Logger
	metrics *platform.Metrics
}

// New creates a worker processor.
func New(store Store, cache SummaryCache, logger *slog.Logger, metrics *platform.Metrics) *Processor {
	if logger == nil {
		logger = slog.Default()
	}
	if metrics == nil {
		metrics = &platform.Metrics{}
	}
	return &Processor{
		store:   store,
		cache:   cache,
		logger:  logger,
		metrics: metrics,
	}
}

// Run polls continuously until the context is cancelled.
func (p *Processor) Run(ctx context.Context, interval time.Duration) error {
	if interval <= 0 {
		interval = 300 * time.Millisecond
	}

	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			return ctx.Err()
		case <-ticker.C:
			if _, err := p.RunOnce(ctx); err != nil && !errors.Is(err, context.Canceled) {
				p.logger.Error("worker batch failed", "err", err)
			}
		}
	}
}

// RunOnce processes one batch of unpublished outbox events.
func (p *Processor) RunOnce(ctx context.Context) (int, error) {
	events, err := p.store.ListUnpublishedOutbox(ctx, 50)
	if err != nil {
		return 0, err
	}

	processed := 0
	for _, event := range events {
		recipients, err := p.store.ListRecipients(ctx, event.OrganizationID, event.ActorUserID)
		if err != nil {
			return processed, err
		}

		title, body, issueID := buildNotification(event)
		for _, recipient := range recipients {
			notification := repository.Notification{
				ID:             uuid.NewString(),
				OrganizationID: event.OrganizationID,
				UserID:         recipient.UserID,
				IssueID:        issueID,
				EventType:      event.EventType,
				Title:          title,
				Body:           body,
				SourceEventID:  event.ID,
			}
			if err := p.store.CreateNotification(ctx, notification); err != nil {
				return processed, err
			}
		}

		if err := p.store.MarkOutboxPublished(ctx, event.ID); err != nil {
			return processed, err
		}
		if p.cache != nil {
			_ = p.cache.DeleteDashboardSummary(ctx, event.OrganizationID)
		}
		processed++
	}

	if processed > 0 {
		p.metrics.AddWorkerProcessed(processed)
	}
	return processed, nil
}

func buildNotification(event repository.OutboxEvent) (title, body string, issueID *string) {
	payload := map[string]any{}
	_ = json.Unmarshal(event.PayloadJSON, &payload)

	if rawIssueID, ok := payload["issue_id"].(string); ok && rawIssueID != "" {
		issueID = &rawIssueID
	}

	switch event.EventType {
	case "issue.created":
		if titleValue, ok := payload["title"].(string); ok && titleValue != "" {
			return "New issue created", fmt.Sprintf("Issue %q was created.", titleValue), issueID
		}
		return "New issue created", "An issue was created.", issueID
	case "issue.updated":
		status, _ := payload["status"].(string)
		if status == "" {
			status = "updated"
		}
		return "Issue updated", fmt.Sprintf("Issue status changed to %s.", status), issueID
	case "comment.created":
		commentBody, _ := payload["body"].(string)
		if len(commentBody) > 80 {
			commentBody = commentBody[:80] + "..."
		}
		return "New comment", fmt.Sprintf("A comment was added: %s", commentBody), issueID
	default:
		return "Workspace event", "A workspace event was processed.", issueID
	}
}
