package repository

import (
	"context"
	"database/sql"
	"encoding/json"
	"errors"
	"fmt"
	"time"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5/pgconn"
	_ "github.com/jackc/pgx/v5/stdlib"
)

var (
	ErrNotFound               = errors.New("not found")
	ErrEmailExists            = errors.New("email already exists")
	ErrOrganizationSlugExists = errors.New("organization slug already exists")
	ErrAlreadyMember          = errors.New("user is already a member")
	ErrPendingInvitation      = errors.New("pending invitation already exists")
	ErrProjectKeyExists       = errors.New("project key already exists")
	ErrVersionConflict        = errors.New("version conflict")
	ErrIdempotencyConflict    = errors.New("idempotency key conflict")
)

// Store provides Postgres-backed persistence for the portfolio project.
type Store struct {
	db *sql.DB
}

// Open connects to Postgres and returns a repository store.
func Open(ctx context.Context, databaseURL string) (*Store, error) {
	db, err := sql.Open("pgx", databaseURL)
	if err != nil {
		return nil, err
	}
	db.SetMaxOpenConns(10)
	db.SetMaxIdleConns(10)
	db.SetConnMaxLifetime(5 * time.Minute)
	if err := db.PingContext(ctx); err != nil {
		return nil, err
	}
	return &Store{db: db}, nil
}

// DB exposes the underlying database handle.
func (s *Store) DB() *sql.DB {
	return s.db
}

// Close closes the underlying database handle.
func (s *Store) Close() error {
	return s.db.Close()
}

// Ping checks if Postgres is reachable.
func (s *Store) Ping(ctx context.Context) error {
	return s.db.PingContext(ctx)
}

// CreateOwner creates the initial owner user, organization, and membership.
func (s *Store) CreateOwner(ctx context.Context, email, passwordHash, displayName, orgName, orgSlug string) (User, Membership, error) {
	tx, err := s.db.BeginTx(ctx, nil)
	if err != nil {
		return User{}, Membership{}, err
	}
	defer tx.Rollback()

	userID := uuid.NewString()
	var user User
	err = tx.QueryRowContext(ctx, `
INSERT INTO users (id, email, password_hash, display_name)
VALUES ($1, $2, $3, $4)
RETURNING id, email, display_name, created_at
`, userID, email, passwordHash, displayName).
		Scan(&user.ID, &user.Email, &user.DisplayName, &user.CreatedAt)
	if err != nil {
		return User{}, Membership{}, mapInsertError(err)
	}

	orgID := uuid.NewString()
	_, err = tx.ExecContext(ctx, `
INSERT INTO organizations (id, slug, name)
VALUES ($1, $2, $3)
`, orgID, orgSlug, orgName)
	if err != nil {
		return User{}, Membership{}, mapInsertError(err)
	}

	membershipID := uuid.NewString()
	var membership Membership
	err = tx.QueryRowContext(ctx, `
INSERT INTO organization_memberships (id, organization_id, user_id, role)
VALUES ($1, $2, $3, 'owner')
RETURNING organization_id, user_id, role, created_at
`, membershipID, orgID, user.ID).
		Scan(&membership.OrganizationID, &membership.UserID, &membership.Role, &membership.CreatedAt)
	if err != nil {
		return User{}, Membership{}, mapInsertError(err)
	}
	membership.OrganizationName = orgName
	membership.OrganizationSlug = orgSlug

	if err := tx.Commit(); err != nil {
		return User{}, Membership{}, err
	}
	return user, membership, nil
}

// GetAuthUserByEmail loads a user and password hash for login.
func (s *Store) GetAuthUserByEmail(ctx context.Context, email string) (AuthUser, error) {
	var user AuthUser
	err := s.db.QueryRowContext(ctx, `
SELECT id, email, display_name, password_hash, created_at
FROM users
WHERE email = $1
`, email).Scan(&user.ID, &user.Email, &user.DisplayName, &user.PasswordHash, &user.CreatedAt)
	if errors.Is(err, sql.ErrNoRows) {
		return AuthUser{}, ErrNotFound
	}
	return user, err
}

// GetUserByID returns a user without password data.
func (s *Store) GetUserByID(ctx context.Context, userID string) (User, error) {
	var user User
	err := s.db.QueryRowContext(ctx, `
SELECT id, email, display_name, created_at
FROM users
WHERE id = $1
`, userID).Scan(&user.ID, &user.Email, &user.DisplayName, &user.CreatedAt)
	if errors.Is(err, sql.ErrNoRows) {
		return User{}, ErrNotFound
	}
	return user, err
}

// ListMembershipsForUser returns all organization memberships for a user.
func (s *Store) ListMembershipsForUser(ctx context.Context, userID string) ([]Membership, error) {
	rows, err := s.db.QueryContext(ctx, `
SELECT m.organization_id, o.name, o.slug, m.user_id, m.role, m.created_at
FROM organization_memberships m
INNER JOIN organizations o ON o.id = m.organization_id
WHERE m.user_id = $1
ORDER BY o.name ASC
`, userID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var memberships []Membership
	for rows.Next() {
		var membership Membership
		if err := rows.Scan(
			&membership.OrganizationID,
			&membership.OrganizationName,
			&membership.OrganizationSlug,
			&membership.UserID,
			&membership.Role,
			&membership.CreatedAt,
		); err != nil {
			return nil, err
		}
		memberships = append(memberships, membership)
	}
	return memberships, rows.Err()
}

// GetMembership returns a user's membership inside an organization.
func (s *Store) GetMembership(ctx context.Context, organizationID, userID string) (Membership, error) {
	var membership Membership
	err := s.db.QueryRowContext(ctx, `
SELECT m.organization_id, o.name, o.slug, m.user_id, m.role, m.created_at
FROM organization_memberships m
INNER JOIN organizations o ON o.id = m.organization_id
WHERE m.organization_id = $1 AND m.user_id = $2
`, organizationID, userID).Scan(
		&membership.OrganizationID,
		&membership.OrganizationName,
		&membership.OrganizationSlug,
		&membership.UserID,
		&membership.Role,
		&membership.CreatedAt,
	)
	if errors.Is(err, sql.ErrNoRows) {
		return Membership{}, ErrNotFound
	}
	return membership, err
}

// InsertRefreshSession stores a refresh session audit row.
func (s *Store) InsertRefreshSession(ctx context.Context, session RefreshSession) error {
	_, err := s.db.ExecContext(ctx, `
INSERT INTO refresh_sessions (id, user_id, token_hash, expires_at)
VALUES ($1, $2, $3, $4)
`, session.ID, session.UserID, session.TokenHash, session.ExpiresAt)
	return err
}

// GetRefreshSession loads one refresh session row.
func (s *Store) GetRefreshSession(ctx context.Context, sessionID string) (RefreshSession, error) {
	var session RefreshSession
	var replacedBy sql.NullString
	var revokedAt sql.NullTime
	err := s.db.QueryRowContext(ctx, `
SELECT id, user_id, token_hash, expires_at, replaced_by, revoked_at, created_at
FROM refresh_sessions
WHERE id = $1
`, sessionID).Scan(&session.ID, &session.UserID, &session.TokenHash, &session.ExpiresAt, &replacedBy, &revokedAt, &session.CreatedAt)
	if errors.Is(err, sql.ErrNoRows) {
		return RefreshSession{}, ErrNotFound
	}
	session.ReplacedBy = nullStringPtr(replacedBy)
	session.RevokedAt = nullTimePtr(revokedAt)
	return session, err
}

// RotateRefreshSession revokes one session and inserts its replacement in a transaction.
func (s *Store) RotateRefreshSession(ctx context.Context, oldSessionID string, newSession RefreshSession) error {
	tx, err := s.db.BeginTx(ctx, nil)
	if err != nil {
		return err
	}
	defer tx.Rollback()

	result, err := tx.ExecContext(ctx, `
UPDATE refresh_sessions
SET revoked_at = now(), replaced_by = $2
WHERE id = $1 AND revoked_at IS NULL
`, oldSessionID, newSession.ID)
	if err != nil {
		return err
	}
	rows, err := result.RowsAffected()
	if err != nil {
		return err
	}
	if rows == 0 {
		return ErrNotFound
	}

	_, err = tx.ExecContext(ctx, `
INSERT INTO refresh_sessions (id, user_id, token_hash, expires_at)
VALUES ($1, $2, $3, $4)
`, newSession.ID, newSession.UserID, newSession.TokenHash, newSession.ExpiresAt)
	if err != nil {
		return err
	}

	return tx.Commit()
}

// RevokeRefreshSession revokes one refresh session.
func (s *Store) RevokeRefreshSession(ctx context.Context, sessionID string) error {
	_, err := s.db.ExecContext(ctx, `
UPDATE refresh_sessions
SET revoked_at = now()
WHERE id = $1 AND revoked_at IS NULL
`, sessionID)
	return err
}

// GetInvitationByIdempotency returns the invitation created for a request key.
func (s *Store) GetInvitationByIdempotency(ctx context.Context, organizationID, key string) (Invitation, error) {
	var invitation Invitation
	var acceptedBy sql.NullString
	var requestKey sql.NullString
	var requestHash sql.NullString
	var acceptedAt sql.NullTime
	err := s.db.QueryRowContext(ctx, `
SELECT id, organization_id, email, role, status, invited_by_user_id, accepted_by_user_id,
       request_idempotency_key, request_hash, created_at, accepted_at
FROM invitations
WHERE organization_id = $1 AND request_idempotency_key = $2
`, organizationID, key).Scan(
		&invitation.ID,
		&invitation.OrganizationID,
		&invitation.Email,
		&invitation.Role,
		&invitation.Status,
		&invitation.InvitedByUserID,
		&acceptedBy,
		&requestKey,
		&requestHash,
		&invitation.CreatedAt,
		&acceptedAt,
	)
	if errors.Is(err, sql.ErrNoRows) {
		return Invitation{}, ErrNotFound
	}
	invitation.AcceptedByUserID = nullStringPtr(acceptedBy)
	invitation.RequestIDempotencyKey = nullStringPtr(requestKey)
	invitation.RequestHash = nullStringPtr(requestHash)
	invitation.AcceptedAt = nullTimePtr(acceptedAt)
	return invitation, err
}

// CreateInvitation inserts a new invitation row.
func (s *Store) CreateInvitation(ctx context.Context, invitation Invitation, tokenHash string) (Invitation, error) {
	var requestKey sql.NullString
	var requestHash sql.NullString
	if invitation.RequestIDempotencyKey != nil {
		requestKey = sql.NullString{String: *invitation.RequestIDempotencyKey, Valid: true}
	}
	if invitation.RequestHash != nil {
		requestHash = sql.NullString{String: *invitation.RequestHash, Valid: true}
	}

	err := s.db.QueryRowContext(ctx, `
INSERT INTO invitations (
    id, organization_id, email, role, status, invited_by_user_id, token_hash,
    request_idempotency_key, request_hash
)
VALUES ($1, $2, $3, $4, 'pending', $5, $6, $7, $8)
RETURNING created_at
`, invitation.ID, invitation.OrganizationID, invitation.Email, invitation.Role, invitation.InvitedByUserID, tokenHash, requestKey, requestHash).
		Scan(&invitation.CreatedAt)
	if err != nil {
		return Invitation{}, mapInsertError(err)
	}
	invitation.Status = "pending"
	return invitation, nil
}

// AcceptInvitation accepts a pending invitation and creates membership.
func (s *Store) AcceptInvitation(ctx context.Context, tokenHash, displayName, passwordHash string) (User, Membership, error) {
	tx, err := s.db.BeginTx(ctx, nil)
	if err != nil {
		return User{}, Membership{}, err
	}
	defer tx.Rollback()

	var invitation Invitation
	err = tx.QueryRowContext(ctx, `
SELECT id, organization_id, email, role, invited_by_user_id, created_at
FROM invitations
WHERE token_hash = $1 AND status = 'pending'
FOR UPDATE
`, tokenHash).Scan(
		&invitation.ID,
		&invitation.OrganizationID,
		&invitation.Email,
		&invitation.Role,
		&invitation.InvitedByUserID,
		&invitation.CreatedAt,
	)
	if errors.Is(err, sql.ErrNoRows) {
		return User{}, Membership{}, ErrNotFound
	}
	if err != nil {
		return User{}, Membership{}, err
	}

	var user User
	var authUser AuthUser
	authUser, err = s.getAuthUserByEmailTx(ctx, tx, invitation.Email)
	switch {
	case errors.Is(err, ErrNotFound):
		userID := uuid.NewString()
		err = tx.QueryRowContext(ctx, `
INSERT INTO users (id, email, password_hash, display_name)
VALUES ($1, $2, $3, $4)
RETURNING id, email, display_name, created_at
`, userID, invitation.Email, passwordHash, displayName).
			Scan(&user.ID, &user.Email, &user.DisplayName, &user.CreatedAt)
		if err != nil {
			return User{}, Membership{}, mapInsertError(err)
		}
	case err != nil:
		return User{}, Membership{}, err
	default:
		user = authUser.User
	}

	membershipID := uuid.NewString()
	var membership Membership
	err = tx.QueryRowContext(ctx, `
INSERT INTO organization_memberships (id, organization_id, user_id, role)
VALUES ($1, $2, $3, $4)
RETURNING organization_id, user_id, role, created_at
`, membershipID, invitation.OrganizationID, user.ID, invitation.Role).
		Scan(&membership.OrganizationID, &membership.UserID, &membership.Role, &membership.CreatedAt)
	if err != nil {
		return User{}, Membership{}, mapInsertError(err)
	}

	var acceptedAt time.Time
	err = tx.QueryRowContext(ctx, `
UPDATE invitations
SET status = 'accepted', accepted_by_user_id = $2, accepted_at = now()
WHERE id = $1
RETURNING accepted_at
`, invitation.ID, user.ID).Scan(&acceptedAt)
	if err != nil {
		return User{}, Membership{}, err
	}

	err = tx.QueryRowContext(ctx, `
SELECT name, slug
FROM organizations
WHERE id = $1
`, invitation.OrganizationID).Scan(&membership.OrganizationName, &membership.OrganizationSlug)
	if err != nil {
		return User{}, Membership{}, err
	}

	if err := tx.Commit(); err != nil {
		return User{}, Membership{}, err
	}
	return user, membership, nil
}

// CreateProject inserts a project row.
func (s *Store) CreateProject(ctx context.Context, organizationID, createdByUserID, name, projectKey string) (Project, error) {
	project := Project{
		ID:              uuid.NewString(),
		OrganizationID:  organizationID,
		Name:            name,
		ProjectKey:      projectKey,
		CreatedByUserID: createdByUserID,
	}
	err := s.db.QueryRowContext(ctx, `
INSERT INTO projects (id, organization_id, name, project_key, created_by_user_id)
VALUES ($1, $2, $3, $4, $5)
RETURNING created_at
`, project.ID, project.OrganizationID, project.Name, project.ProjectKey, project.CreatedByUserID).
		Scan(&project.CreatedAt)
	if err != nil {
		return Project{}, mapInsertError(err)
	}
	return project, nil
}

// GetProject returns one project scoped by organization.
func (s *Store) GetProject(ctx context.Context, organizationID, projectID string) (Project, error) {
	var project Project
	err := s.db.QueryRowContext(ctx, `
SELECT id, organization_id, name, project_key, created_by_user_id, created_at
FROM projects
WHERE organization_id = $1 AND id = $2
`, organizationID, projectID).Scan(
		&project.ID,
		&project.OrganizationID,
		&project.Name,
		&project.ProjectKey,
		&project.CreatedByUserID,
		&project.CreatedAt,
	)
	if errors.Is(err, sql.ErrNoRows) {
		return Project{}, ErrNotFound
	}
	return project, err
}

// GetProjectByID returns one project without requiring organization id.
func (s *Store) GetProjectByID(ctx context.Context, projectID string) (Project, error) {
	var project Project
	err := s.db.QueryRowContext(ctx, `
SELECT id, organization_id, name, project_key, created_by_user_id, created_at
FROM projects
WHERE id = $1
`, projectID).Scan(
		&project.ID,
		&project.OrganizationID,
		&project.Name,
		&project.ProjectKey,
		&project.CreatedByUserID,
		&project.CreatedAt,
	)
	if errors.Is(err, sql.ErrNoRows) {
		return Project{}, ErrNotFound
	}
	return project, err
}

// UserBelongsToOrganization returns true when a membership exists.
func (s *Store) UserBelongsToOrganization(ctx context.Context, organizationID, userID string) (bool, error) {
	var exists bool
	err := s.db.QueryRowContext(ctx, `
SELECT EXISTS(
    SELECT 1
    FROM organization_memberships
    WHERE organization_id = $1 AND user_id = $2
)
`, organizationID, userID).Scan(&exists)
	return exists, err
}

// GetIssueByID returns one issue by its primary key.
func (s *Store) GetIssueByID(ctx context.Context, issueID string) (Issue, error) {
	var issue Issue
	var assignee sql.NullString
	err := s.db.QueryRowContext(ctx, `
SELECT id, organization_id, project_id, title, description, status, assignee_user_id,
       created_by_user_id, version, created_at, updated_at
FROM issues
WHERE id = $1
`, issueID).Scan(
		&issue.ID,
		&issue.OrganizationID,
		&issue.ProjectID,
		&issue.Title,
		&issue.Description,
		&issue.Status,
		&assignee,
		&issue.CreatedByUserID,
		&issue.Version,
		&issue.CreatedAt,
		&issue.UpdatedAt,
	)
	if errors.Is(err, sql.ErrNoRows) {
		return Issue{}, ErrNotFound
	}
	issue.AssigneeUserID = nullStringPtr(assignee)
	return issue, err
}

// ListProjects returns all projects for one organization.
func (s *Store) ListProjects(ctx context.Context, organizationID string) ([]Project, error) {
	rows, err := s.db.QueryContext(ctx, `
SELECT id, organization_id, name, project_key, created_by_user_id, created_at
FROM projects
WHERE organization_id = $1
ORDER BY created_at ASC
`, organizationID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var projects []Project
	for rows.Next() {
		var project Project
		if err := rows.Scan(
			&project.ID,
			&project.OrganizationID,
			&project.Name,
			&project.ProjectKey,
			&project.CreatedByUserID,
			&project.CreatedAt,
		); err != nil {
			return nil, err
		}
		projects = append(projects, project)
	}
	return projects, rows.Err()
}

// GetIssueByIdempotency returns issue created for a request key.
func (s *Store) GetIssueByIdempotency(ctx context.Context, projectID, key string) (Issue, error) {
	var issue Issue
	var assignee sql.NullString
	var requestKey sql.NullString
	var requestHash sql.NullString
	err := s.db.QueryRowContext(ctx, `
SELECT id, organization_id, project_id, title, description, status, assignee_user_id,
       created_by_user_id, version, request_idempotency_key, request_hash, created_at, updated_at
FROM issues
WHERE project_id = $1 AND request_idempotency_key = $2
`, projectID, key).Scan(
		&issue.ID,
		&issue.OrganizationID,
		&issue.ProjectID,
		&issue.Title,
		&issue.Description,
		&issue.Status,
		&assignee,
		&issue.CreatedByUserID,
		&issue.Version,
		&requestKey,
		&requestHash,
		&issue.CreatedAt,
		&issue.UpdatedAt,
	)
	if errors.Is(err, sql.ErrNoRows) {
		return Issue{}, ErrNotFound
	}
	issue.AssigneeUserID = nullStringPtr(assignee)
	issue.RequestIDempotency = nullStringPtr(requestKey)
	issue.RequestHash = nullStringPtr(requestHash)
	return issue, err
}

// CreateIssue inserts a new issue and matching outbox event in one transaction.
func (s *Store) CreateIssue(ctx context.Context, issue Issue, actorUserID string, payload json.RawMessage) (Issue, error) {
	tx, err := s.db.BeginTx(ctx, nil)
	if err != nil {
		return Issue{}, err
	}
	defer tx.Rollback()

	err = tx.QueryRowContext(ctx, `
INSERT INTO issues (
    id, organization_id, project_id, title, description, status, assignee_user_id,
    created_by_user_id, request_idempotency_key, request_hash
)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
RETURNING version, created_at, updated_at
`, issue.ID, issue.OrganizationID, issue.ProjectID, issue.Title, issue.Description, issue.Status,
		issue.AssigneeUserID, issue.CreatedByUserID, issue.RequestIDempotency, issue.RequestHash).
		Scan(&issue.Version, &issue.CreatedAt, &issue.UpdatedAt)
	if err != nil {
		return Issue{}, mapInsertError(err)
	}

	if err := insertOutboxTx(ctx, tx, issue.OrganizationID, "issue", issue.ID, "issue.created", actorUserID, payload); err != nil {
		return Issue{}, err
	}

	if err := tx.Commit(); err != nil {
		return Issue{}, err
	}
	return issue, nil
}

// ListIssues returns issues for a project inside one organization.
func (s *Store) ListIssues(ctx context.Context, organizationID, projectID string) ([]Issue, error) {
	rows, err := s.db.QueryContext(ctx, `
SELECT id, organization_id, project_id, title, description, status, assignee_user_id,
       created_by_user_id, version, created_at, updated_at
FROM issues
WHERE organization_id = $1 AND project_id = $2
ORDER BY created_at ASC
`, organizationID, projectID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var issues []Issue
	for rows.Next() {
		var issue Issue
		var assignee sql.NullString
		if err := rows.Scan(
			&issue.ID,
			&issue.OrganizationID,
			&issue.ProjectID,
			&issue.Title,
			&issue.Description,
			&issue.Status,
			&assignee,
			&issue.CreatedByUserID,
			&issue.Version,
			&issue.CreatedAt,
			&issue.UpdatedAt,
		); err != nil {
			return nil, err
		}
		issue.AssigneeUserID = nullStringPtr(assignee)
		issues = append(issues, issue)
	}
	return issues, rows.Err()
}

// UpdateIssue updates issue state with optimistic locking and emits an outbox event.
func (s *Store) UpdateIssue(ctx context.Context, organizationID, issueID, actorUserID string, version int64, status string, assigneeUserID *string, payload json.RawMessage) (Issue, error) {
	tx, err := s.db.BeginTx(ctx, nil)
	if err != nil {
		return Issue{}, err
	}
	defer tx.Rollback()

	var issue Issue
	var assignee sql.NullString
	updateAssignee := sql.NullString{}
	if assigneeUserID != nil {
		updateAssignee = sql.NullString{String: *assigneeUserID, Valid: true}
	}

	err = tx.QueryRowContext(ctx, `
UPDATE issues
SET status = $1,
    assignee_user_id = COALESCE($2, assignee_user_id),
    version = version + 1,
    updated_at = now()
WHERE id = $3 AND organization_id = $4 AND version = $5
RETURNING id, organization_id, project_id, title, description, status, assignee_user_id,
          created_by_user_id, version, created_at, updated_at
`, status, updateAssignee, issueID, organizationID, version).Scan(
		&issue.ID,
		&issue.OrganizationID,
		&issue.ProjectID,
		&issue.Title,
		&issue.Description,
		&issue.Status,
		&assignee,
		&issue.CreatedByUserID,
		&issue.Version,
		&issue.CreatedAt,
		&issue.UpdatedAt,
	)
	if errors.Is(err, sql.ErrNoRows) {
		return Issue{}, ErrVersionConflict
	}
	if err != nil {
		return Issue{}, err
	}
	issue.AssigneeUserID = nullStringPtr(assignee)

	if err := insertOutboxTx(ctx, tx, issue.OrganizationID, "issue", issue.ID, "issue.updated", actorUserID, payload); err != nil {
		return Issue{}, err
	}

	if err := tx.Commit(); err != nil {
		return Issue{}, err
	}
	return issue, nil
}

// AddComment inserts a comment and corresponding outbox event.
func (s *Store) AddComment(ctx context.Context, organizationID, issueID, authorUserID, body string, payload json.RawMessage) (Comment, error) {
	tx, err := s.db.BeginTx(ctx, nil)
	if err != nil {
		return Comment{}, err
	}
	defer tx.Rollback()

	var exists bool
	if err := tx.QueryRowContext(ctx, `
SELECT EXISTS(
    SELECT 1
    FROM issues
    WHERE id = $1 AND organization_id = $2
)
`, issueID, organizationID).Scan(&exists); err != nil {
		return Comment{}, err
	}
	if !exists {
		return Comment{}, ErrNotFound
	}

	comment := Comment{
		ID:             uuid.NewString(),
		OrganizationID: organizationID,
		IssueID:        issueID,
		AuthorUserID:   authorUserID,
		Body:           body,
	}
	err = tx.QueryRowContext(ctx, `
INSERT INTO comments (id, organization_id, issue_id, author_user_id, body)
VALUES ($1, $2, $3, $4, $5)
RETURNING created_at
`, comment.ID, comment.OrganizationID, comment.IssueID, comment.AuthorUserID, comment.Body).
		Scan(&comment.CreatedAt)
	if err != nil {
		return Comment{}, err
	}

	if err := insertOutboxTx(ctx, tx, organizationID, "comment", comment.ID, "comment.created", authorUserID, payload); err != nil {
		return Comment{}, err
	}

	if err := tx.Commit(); err != nil {
		return Comment{}, err
	}
	return comment, nil
}

// ListNotifications returns notifications for one user inside an organization.
func (s *Store) ListNotifications(ctx context.Context, organizationID, userID string, limit int) ([]Notification, error) {
	rows, err := s.db.QueryContext(ctx, `
SELECT id, organization_id, user_id, issue_id, event_type, title, body, source_event_id, created_at, read_at
FROM notifications
WHERE organization_id = $1 AND user_id = $2
ORDER BY created_at DESC
LIMIT $3
`, organizationID, userID, limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var notifications []Notification
	for rows.Next() {
		var notification Notification
		var issueID sql.NullString
		var readAt sql.NullTime
		if err := rows.Scan(
			&notification.ID,
			&notification.OrganizationID,
			&notification.UserID,
			&issueID,
			&notification.EventType,
			&notification.Title,
			&notification.Body,
			&notification.SourceEventID,
			&notification.CreatedAt,
			&readAt,
		); err != nil {
			return nil, err
		}
		notification.IssueID = nullStringPtr(issueID)
		notification.ReadAt = nullTimePtr(readAt)
		notifications = append(notifications, notification)
	}
	return notifications, rows.Err()
}

// BuildDashboardSummary calculates org-wide dashboard counters.
func (s *Store) BuildDashboardSummary(ctx context.Context, organizationID string) (DashboardSummary, error) {
	summary := DashboardSummary{OrganizationID: organizationID}

	if err := s.db.QueryRowContext(ctx, `
SELECT count(*) FROM projects WHERE organization_id = $1
`, organizationID).Scan(&summary.ProjectsTotal); err != nil {
		return DashboardSummary{}, err
	}

	rows, err := s.db.QueryContext(ctx, `
SELECT status, count(*) FROM issues
WHERE organization_id = $1
GROUP BY status
`, organizationID)
	if err != nil {
		return DashboardSummary{}, err
	}
	for rows.Next() {
		var status string
		var count int
		if err := rows.Scan(&status, &count); err != nil {
			rows.Close()
			return DashboardSummary{}, err
		}
		switch status {
		case "todo":
			summary.IssuesTodo = count
		case "in_progress":
			summary.IssuesInProgress = count
		case "done":
			summary.IssuesDone = count
		}
	}
	rows.Close()

	if err := s.db.QueryRowContext(ctx, `
SELECT count(*)
FROM notifications
WHERE organization_id = $1 AND read_at IS NULL
`, organizationID).Scan(&summary.UnreadNotifications); err != nil {
		return DashboardSummary{}, err
	}
	return summary, nil
}

// ListUnpublishedOutbox returns unpublished outbox events ordered by created_at.
func (s *Store) ListUnpublishedOutbox(ctx context.Context, limit int) ([]OutboxEvent, error) {
	rows, err := s.db.QueryContext(ctx, `
SELECT id, organization_id, aggregate_type, aggregate_id, event_type, actor_user_id, payload_json, created_at, published_at
FROM outbox_events
WHERE published_at IS NULL
ORDER BY created_at ASC
LIMIT $1
`, limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var events []OutboxEvent
	for rows.Next() {
		var event OutboxEvent
		var publishedAt sql.NullTime
		if err := rows.Scan(
			&event.ID,
			&event.OrganizationID,
			&event.AggregateType,
			&event.AggregateID,
			&event.EventType,
			&event.ActorUserID,
			&event.PayloadJSON,
			&event.CreatedAt,
			&publishedAt,
		); err != nil {
			return nil, err
		}
		event.PublishedAt = nullTimePtr(publishedAt)
		events = append(events, event)
	}
	return events, rows.Err()
}

// ListRecipients returns organization members excluding one actor id.
func (s *Store) ListRecipients(ctx context.Context, organizationID, excludeUserID string) ([]Recipient, error) {
	rows, err := s.db.QueryContext(ctx, `
SELECT u.id, u.display_name
FROM organization_memberships m
INNER JOIN users u ON u.id = m.user_id
WHERE m.organization_id = $1 AND m.user_id <> $2
ORDER BY u.display_name ASC
`, organizationID, excludeUserID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var recipients []Recipient
	for rows.Next() {
		var recipient Recipient
		if err := rows.Scan(&recipient.UserID, &recipient.DisplayName); err != nil {
			return nil, err
		}
		recipients = append(recipients, recipient)
	}
	return recipients, rows.Err()
}

// CreateNotification inserts one notification row with duplicate protection.
func (s *Store) CreateNotification(ctx context.Context, notification Notification) error {
	_, err := s.db.ExecContext(ctx, `
INSERT INTO notifications (id, organization_id, user_id, issue_id, event_type, title, body, source_event_id)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
ON CONFLICT (user_id, source_event_id) DO NOTHING
`, notification.ID, notification.OrganizationID, notification.UserID, notification.IssueID, notification.EventType, notification.Title, notification.Body, notification.SourceEventID)
	return err
}

// MarkOutboxPublished marks an outbox event as published.
func (s *Store) MarkOutboxPublished(ctx context.Context, eventID string) error {
	_, err := s.db.ExecContext(ctx, `
UPDATE outbox_events
SET published_at = now()
WHERE id = $1
`, eventID)
	return err
}

func (s *Store) getAuthUserByEmailTx(ctx context.Context, tx *sql.Tx, email string) (AuthUser, error) {
	var user AuthUser
	err := tx.QueryRowContext(ctx, `
SELECT id, email, display_name, password_hash, created_at
FROM users
WHERE email = $1
`, email).Scan(&user.ID, &user.Email, &user.DisplayName, &user.PasswordHash, &user.CreatedAt)
	if errors.Is(err, sql.ErrNoRows) {
		return AuthUser{}, ErrNotFound
	}
	return user, err
}

func insertOutboxTx(ctx context.Context, tx *sql.Tx, organizationID, aggregateType, aggregateID, eventType, actorUserID string, payload json.RawMessage) error {
	_, err := tx.ExecContext(ctx, `
INSERT INTO outbox_events (id, organization_id, aggregate_type, aggregate_id, event_type, actor_user_id, payload_json)
VALUES ($1, $2, $3, $4, $5, $6, $7)
`, uuid.NewString(), organizationID, aggregateType, aggregateID, eventType, actorUserID, payload)
	return err
}

func mapInsertError(err error) error {
	var pgErr *pgconn.PgError
	if !errors.As(err, &pgErr) {
		return err
	}
	switch pgErr.ConstraintName {
	case "users_email_key":
		return ErrEmailExists
	case "organizations_slug_key":
		return ErrOrganizationSlugExists
	case "organization_memberships_organization_id_user_id_key":
		return ErrAlreadyMember
	case "invitations_pending_org_email_key":
		return ErrPendingInvitation
	case "invitations_org_idempotency_key":
		return ErrIdempotencyConflict
	case "projects_organization_id_project_key_key":
		return ErrProjectKeyExists
	case "issues_project_idempotency_key":
		return ErrIdempotencyConflict
	default:
		return fmt.Errorf("%w (%s)", err, pgErr.ConstraintName)
	}
}
