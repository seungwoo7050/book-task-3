package repository

import (
	"database/sql"
	"encoding/json"
	"time"
)

// User는 비밀번호 해시를 제외한 애플리케이션 사용자 모델이다.
type User struct {
	ID          string    `json:"id"`
	Email       string    `json:"email"`
	DisplayName string    `json:"display_name"`
	CreatedAt   time.Time `json:"created_at"`
}

// AuthUser는 로그인 검증에 필요한 비밀번호 해시를 포함한다.
type AuthUser struct {
	User
	PasswordHash string
}

// Membership은 조직 안에서의 사용자 역할을 나타낸다.
type Membership struct {
	OrganizationID   string    `json:"organization_id"`
	OrganizationName string    `json:"organization_name"`
	OrganizationSlug string    `json:"organization_slug"`
	UserID           string    `json:"user_id"`
	Role             string    `json:"role"`
	CreatedAt        time.Time `json:"created_at"`
}

// Invitation은 조직 초대의 현재 상태를 나타낸다.
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

// Project는 조직 아래의 프로젝트를 나타낸다.
type Project struct {
	ID              string    `json:"id"`
	OrganizationID  string    `json:"organization_id"`
	Name            string    `json:"name"`
	ProjectKey      string    `json:"project_key"`
	CreatedByUserID string    `json:"created_by_user_id"`
	CreatedAt       time.Time `json:"created_at"`
}

// Issue는 프로젝트 안에서 추적하는 작업 항목이다.
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

// Comment는 이슈에 달린 댓글이다.
type Comment struct {
	ID             string    `json:"id"`
	OrganizationID string    `json:"organization_id"`
	IssueID        string    `json:"issue_id"`
	AuthorUserID   string    `json:"author_user_id"`
	Body           string    `json:"body"`
	CreatedAt      time.Time `json:"created_at"`
}

// RefreshSession은 Postgres에 저장하는 refresh token 세션 상태다.
type RefreshSession struct {
	ID         string     `json:"id"`
	UserID     string     `json:"user_id"`
	TokenHash  string     `json:"-"`
	ExpiresAt  time.Time  `json:"expires_at"`
	ReplacedBy *string    `json:"replaced_by,omitempty"`
	RevokedAt  *time.Time `json:"revoked_at,omitempty"`
	CreatedAt  time.Time  `json:"created_at"`
}

// OutboxEvent는 비동기 통지를 위해 저장하는 outbox 이벤트다.
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

// Recipient는 알림을 받을 사용자를 식별한다.
type Recipient struct {
	UserID      string
	DisplayName string
}

// Notification은 outbox 이벤트를 바탕으로 생성된 사용자 알림이다.
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

// DashboardSummary는 조직 전체 대시보드 집계 결과다.
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
