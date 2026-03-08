package repository

import (
	"database/sql"
	"encoding/json"
	"time"
)

// User represents an application user without password data.
type User struct {
	ID          string    `json:"id"`
	Email       string    `json:"email"`
	DisplayName string    `json:"display_name"`
	CreatedAt   time.Time `json:"created_at"`
}

// AuthUser contains password hash required for login.
type AuthUser struct {
	User
	PasswordHash string
}

// Membership represents a user role inside an organization.
type Membership struct {
	OrganizationID   string    `json:"organization_id"`
	OrganizationName string    `json:"organization_name"`
	OrganizationSlug string    `json:"organization_slug"`
	UserID           string    `json:"user_id"`
	Role             string    `json:"role"`
	CreatedAt        time.Time `json:"created_at"`
}

// Invitation represents a pending or accepted organization invite.
type Invitation struct {
	ID                    string     `json:"id"`
	OrganizationID        string     `json:"organization_id"`
	Email                 string     `json:"email"`
	Role                  string     `json:"role"`
	Status                string     `json:"status"`
	InvitedByUserID       string     `json:"invited_by_user_id"`
	AcceptedByUserID      *string    `json:"accepted_by_user_id,omitempty"`
	RequestIDempotencyKey *string    `json:"request_idempotency_key,omitempty"`
	RequestHash           *string    `json:"-"`
	CreatedAt             time.Time  `json:"created_at"`
	AcceptedAt            *time.Time `json:"accepted_at,omitempty"`
}

// Project represents an organization project.
type Project struct {
	ID              string    `json:"id"`
	OrganizationID  string    `json:"organization_id"`
	Name            string    `json:"name"`
	ProjectKey      string    `json:"project_key"`
	CreatedByUserID string    `json:"created_by_user_id"`
	CreatedAt       time.Time `json:"created_at"`
}

// Issue represents a tracked issue inside a project.
type Issue struct {
	ID                 string    `json:"id"`
	OrganizationID     string    `json:"organization_id"`
	ProjectID          string    `json:"project_id"`
	Title              string    `json:"title"`
	Description        string    `json:"description"`
	Status             string    `json:"status"`
	AssigneeUserID     *string   `json:"assignee_user_id,omitempty"`
	CreatedByUserID    string    `json:"created_by_user_id"`
	Version            int64     `json:"version"`
	RequestIDempotency *string   `json:"-"`
	RequestHash        *string   `json:"-"`
	CreatedAt          time.Time `json:"created_at"`
	UpdatedAt          time.Time `json:"updated_at"`
}

// Comment represents a comment attached to an issue.
type Comment struct {
	ID             string    `json:"id"`
	OrganizationID string    `json:"organization_id"`
	IssueID        string    `json:"issue_id"`
	AuthorUserID   string    `json:"author_user_id"`
	Body           string    `json:"body"`
	CreatedAt      time.Time `json:"created_at"`
}

// RefreshSession stores refresh-token audit data in Postgres.
type RefreshSession struct {
	ID         string     `json:"id"`
	UserID     string     `json:"user_id"`
	TokenHash  string     `json:"-"`
	ExpiresAt  time.Time  `json:"expires_at"`
	ReplacedBy *string    `json:"replaced_by,omitempty"`
	RevokedAt  *time.Time `json:"revoked_at,omitempty"`
	CreatedAt  time.Time  `json:"created_at"`
}

// OutboxEvent is consumed by the worker process.
type OutboxEvent struct {
	ID             string          `json:"id"`
	OrganizationID string          `json:"organization_id"`
	AggregateType  string          `json:"aggregate_type"`
	AggregateID    string          `json:"aggregate_id"`
	EventType      string          `json:"event_type"`
	ActorUserID    string          `json:"actor_user_id"`
	PayloadJSON    json.RawMessage `json:"payload_json"`
	CreatedAt      time.Time       `json:"created_at"`
	PublishedAt    *time.Time      `json:"published_at,omitempty"`
}

// Recipient identifies a notification target.
type Recipient struct {
	UserID      string
	DisplayName string
}

// Notification is delivered asynchronously from outbox events.
type Notification struct {
	ID             string     `json:"id"`
	OrganizationID string     `json:"organization_id"`
	UserID         string     `json:"user_id"`
	IssueID        *string    `json:"issue_id,omitempty"`
	EventType      string     `json:"event_type"`
	Title          string     `json:"title"`
	Body           string     `json:"body"`
	SourceEventID  string     `json:"source_event_id"`
	CreatedAt      time.Time  `json:"created_at"`
	ReadAt         *time.Time `json:"read_at,omitempty"`
}

// DashboardSummary is the cached org-wide dashboard aggregate.
type DashboardSummary struct {
	OrganizationID      string `json:"organization_id"`
	ProjectsTotal       int    `json:"projects_total"`
	IssuesTodo          int    `json:"issues_todo"`
	IssuesInProgress    int    `json:"issues_in_progress"`
	IssuesDone          int    `json:"issues_done"`
	UnreadNotifications int    `json:"unread_notifications"`
}

func stringPtr(value string) *string {
	if value == "" {
		return nil
	}
	return &value
}

func nullStringPtr(value sql.NullString) *string {
	if value.Valid {
		return &value.String
	}
	return nil
}

func nullTimePtr(value sql.NullTime) *time.Time {
	if value.Valid {
		return &value.Time
	}
	return nil
}
