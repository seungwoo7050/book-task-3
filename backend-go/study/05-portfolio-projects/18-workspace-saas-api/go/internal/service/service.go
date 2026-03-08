package service

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"log/slog"
	"net/http"
	"strings"
	"time"

	"github.com/google/uuid"
	"golang.org/x/crypto/bcrypt"

	"github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/auth"
	"github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/cache"
	"github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/platform"
	"github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/repository"
)

// Service orchestrates the B2B SaaS use-cases for the portfolio API.
type Service struct {
	store             *repository.Store
	cache             *cache.Client
	logger            *slog.Logger
	metrics           *platform.Metrics
	jwtSecret         []byte
	accessTokenTTL    time.Duration
	refreshTokenTTL   time.Duration
	dashboardCacheTTL time.Duration
	now               func() time.Time
}

// New creates a new portfolio service.
func New(
	store *repository.Store,
	cacheClient *cache.Client,
	logger *slog.Logger,
	metrics *platform.Metrics,
	cfg platform.Config,
) *Service {
	if logger == nil {
		logger = slog.Default()
	}
	if metrics == nil {
		metrics = &platform.Metrics{}
	}
	return &Service{
		store:             store,
		cache:             cacheClient,
		logger:            logger,
		metrics:           metrics,
		jwtSecret:         cfg.JWTSecret,
		accessTokenTTL:    cfg.AccessTokenTTL,
		refreshTokenTTL:   cfg.RefreshTokenTTL,
		dashboardCacheTTL: cfg.DashboardCacheTTL,
		now:               time.Now,
	}
}

// AuthResponse is returned by register/login/refresh/accept invitation.
type AuthResponse struct {
	AccessToken  string                  `json:"access_token"`
	RefreshToken string                  `json:"refresh_token"`
	User         repository.User         `json:"user"`
	Memberships  []repository.Membership `json:"memberships"`
}

// MeResponse returns user state for GET /v1/me.
type MeResponse struct {
	User        repository.User         `json:"user"`
	Memberships []repository.Membership `json:"memberships"`
}

// InviteResponse is returned by POST /invitations.
type InviteResponse struct {
	Invitation         repository.Invitation `json:"invitation"`
	AcceptTokenPreview string                `json:"accept_token_preview,omitempty"`
	Replayed           bool                  `json:"replayed"`
}

// IssueResponse wraps issue create/update responses.
type IssueResponse struct {
	Issue    repository.Issue `json:"issue"`
	Replayed bool             `json:"replayed,omitempty"`
}

// RegisterOwnerInput is the request body for owner registration.
type RegisterOwnerInput struct {
	Email       string `json:"email"`
	Password    string `json:"password"`
	DisplayName string `json:"display_name"`
	OrgName     string `json:"org_name"`
	OrgSlug     string `json:"org_slug"`
}

// LoginInput is the request body for login.
type LoginInput struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

// RefreshInput rotates refresh tokens.
type RefreshInput struct {
	RefreshToken string `json:"refresh_token"`
}

// LogoutInput revokes a refresh token session.
type LogoutInput struct {
	RefreshToken string `json:"refresh_token"`
}

// InviteInput creates an organization invitation.
type InviteInput struct {
	Email string `json:"email"`
	Role  string `json:"role"`
}

// AcceptInvitationInput accepts an invitation token.
type AcceptInvitationInput struct {
	Token       string `json:"token"`
	DisplayName string `json:"display_name"`
	Password    string `json:"password"`
}

// CreateProjectInput creates a project under one organization.
type CreateProjectInput struct {
	Name       string `json:"name"`
	ProjectKey string `json:"project_key"`
}

// CreateIssueInput creates a project issue.
type CreateIssueInput struct {
	Title          string  `json:"title"`
	Description    string  `json:"description"`
	AssigneeUserID *string `json:"assignee_user_id,omitempty"`
}

// UpdateIssueInput updates issue status/assignee with optimistic locking.
type UpdateIssueInput struct {
	Status         string  `json:"status"`
	AssigneeUserID *string `json:"assignee_user_id,omitempty"`
	Version        int64   `json:"version"`
}

// AddCommentInput adds a comment to an issue.
type AddCommentInput struct {
	Body string `json:"body"`
}

// Ready checks whether required dependencies are available.
func (s *Service) Ready(ctx context.Context) error {
	if err := s.store.Ping(ctx); err != nil {
		return platform.Errorf(http.StatusServiceUnavailable, "database_unavailable", "database is unavailable")
	}
	if err := s.cache.Ping(ctx); err != nil {
		return platform.Errorf(http.StatusServiceUnavailable, "redis_unavailable", "redis is unavailable")
	}
	return nil
}

// RegisterOwner creates the first user/org membership and immediately issues tokens.
func (s *Service) RegisterOwner(ctx context.Context, input RegisterOwnerInput) (*AuthResponse, error) {
	if err := validateRegisterOwner(input); err != nil {
		return nil, err
	}

	passwordHash, err := bcrypt.GenerateFromPassword([]byte(input.Password), bcrypt.DefaultCost)
	if err != nil {
		return nil, err
	}

	user, membership, err := s.store.CreateOwner(
		ctx,
		strings.ToLower(strings.TrimSpace(input.Email)),
		string(passwordHash),
		strings.TrimSpace(input.DisplayName),
		strings.TrimSpace(input.OrgName),
		strings.TrimSpace(input.OrgSlug),
	)
	if err != nil {
		return nil, mapRepositoryError(err)
	}

	memberships := []repository.Membership{membership}
	authResponse, err := s.issueAuthResponse(ctx, user, memberships)
	if err != nil {
		return nil, err
	}
	s.metrics.IncAuthLogins()
	return authResponse, nil
}

// Login validates credentials and issues new access/refresh tokens.
func (s *Service) Login(ctx context.Context, input LoginInput) (*AuthResponse, error) {
	if strings.TrimSpace(input.Email) == "" || strings.TrimSpace(input.Password) == "" {
		return nil, platform.Errorf(http.StatusUnprocessableEntity, "validation_error", "email and password are required")
	}

	authUser, err := s.store.GetAuthUserByEmail(ctx, strings.ToLower(strings.TrimSpace(input.Email)))
	if err != nil {
		if errors.Is(err, repository.ErrNotFound) {
			return nil, platform.Errorf(http.StatusUnauthorized, "invalid_credentials", "email or password is invalid")
		}
		return nil, err
	}
	if err := bcrypt.CompareHashAndPassword([]byte(authUser.PasswordHash), []byte(input.Password)); err != nil {
		return nil, platform.Errorf(http.StatusUnauthorized, "invalid_credentials", "email or password is invalid")
	}

	memberships, err := s.store.ListMembershipsForUser(ctx, authUser.ID)
	if err != nil {
		return nil, err
	}
	authResponse, err := s.issueAuthResponse(ctx, authUser.User, memberships)
	if err != nil {
		return nil, err
	}
	s.metrics.IncAuthLogins()
	return authResponse, nil
}

// Refresh rotates a refresh session and returns a new token pair.
func (s *Service) Refresh(ctx context.Context, input RefreshInput) (*AuthResponse, error) {
	sessionID, tokenHash, err := auth.ParseRefreshToken(strings.TrimSpace(input.RefreshToken))
	if err != nil {
		return nil, platform.Errorf(http.StatusUnauthorized, "invalid_refresh_token", "refresh token is invalid")
	}

	storedHash, err := s.cache.GetRefreshSessionHash(ctx, sessionID)
	switch {
	case errors.Is(err, cache.ErrUnavailable):
		return nil, platform.Errorf(http.StatusServiceUnavailable, "redis_unavailable", "refresh token store is unavailable")
	case errors.Is(err, cache.ErrNotFound):
		return nil, platform.Errorf(http.StatusUnauthorized, "invalid_refresh_token", "refresh token is invalid")
	case err != nil:
		return nil, err
	case storedHash != tokenHash:
		return nil, platform.Errorf(http.StatusUnauthorized, "invalid_refresh_token", "refresh token is invalid")
	}

	session, err := s.store.GetRefreshSession(ctx, sessionID)
	if err != nil {
		return nil, mapRepositoryError(err)
	}
	if session.RevokedAt != nil || session.ExpiresAt.Before(s.now()) {
		return nil, platform.Errorf(http.StatusUnauthorized, "invalid_refresh_token", "refresh token is expired or revoked")
	}

	user, err := s.store.GetUserByID(ctx, session.UserID)
	if err != nil {
		return nil, mapRepositoryError(err)
	}
	memberships, err := s.store.ListMembershipsForUser(ctx, user.ID)
	if err != nil {
		return nil, err
	}

	newSessionID := uuid.NewString()
	rawToken, newTokenHash, err := auth.GenerateRefreshToken(newSessionID)
	if err != nil {
		return nil, err
	}
	newSession := repository.RefreshSession{
		ID:        newSessionID,
		UserID:    user.ID,
		TokenHash: newTokenHash,
		ExpiresAt: s.now().Add(s.refreshTokenTTL),
	}
	if err := s.store.RotateRefreshSession(ctx, session.ID, newSession); err != nil {
		return nil, mapRepositoryError(err)
	}

	if err := s.cache.SetRefreshSession(ctx, newSession.ID, newTokenHash, s.refreshTokenTTL); err != nil {
		_ = s.store.RevokeRefreshSession(ctx, newSession.ID)
		return nil, platform.Errorf(http.StatusServiceUnavailable, "redis_unavailable", "refresh token store is unavailable")
	}
	if err := s.cache.DeleteRefreshSession(ctx, session.ID); err != nil && !errors.Is(err, cache.ErrNotFound) {
		s.logger.Warn("failed to delete old refresh session", "session_id", session.ID, "err", err)
	}

	accessToken, err := auth.SignAccessToken(s.jwtSecret, auth.Claims{
		Sub:   user.ID,
		Email: user.Email,
		Exp:   s.now().Add(s.accessTokenTTL).Unix(),
	})
	if err != nil {
		return nil, err
	}
	return &AuthResponse{
		AccessToken:  accessToken,
		RefreshToken: rawToken,
		User:         user,
		Memberships:  memberships,
	}, nil
}

// Logout revokes a refresh session and removes it from Redis.
func (s *Service) Logout(ctx context.Context, input LogoutInput) error {
	sessionID, _, err := auth.ParseRefreshToken(strings.TrimSpace(input.RefreshToken))
	if err != nil {
		return platform.Errorf(http.StatusUnauthorized, "invalid_refresh_token", "refresh token is invalid")
	}
	if _, err := s.cache.GetRefreshSessionHash(ctx, sessionID); errors.Is(err, cache.ErrUnavailable) {
		return platform.Errorf(http.StatusServiceUnavailable, "redis_unavailable", "refresh token store is unavailable")
	} else if errors.Is(err, cache.ErrNotFound) {
		return platform.Errorf(http.StatusUnauthorized, "invalid_refresh_token", "refresh token is invalid")
	} else if err != nil {
		return err
	}

	if err := s.store.RevokeRefreshSession(ctx, sessionID); err != nil {
		return err
	}
	if err := s.cache.DeleteRefreshSession(ctx, sessionID); err != nil && !errors.Is(err, cache.ErrNotFound) {
		return platform.Errorf(http.StatusServiceUnavailable, "redis_unavailable", "refresh token store is unavailable")
	}
	return nil
}

// Me returns user profile and memberships.
func (s *Service) Me(ctx context.Context, userID string) (*MeResponse, error) {
	user, err := s.store.GetUserByID(ctx, userID)
	if err != nil {
		return nil, mapRepositoryError(err)
	}
	memberships, err := s.store.ListMembershipsForUser(ctx, userID)
	if err != nil {
		return nil, err
	}
	return &MeResponse{User: user, Memberships: memberships}, nil
}

// InviteMember creates an organization invitation with request idempotency.
func (s *Service) InviteMember(ctx context.Context, actorUserID, organizationID, idempotencyKey string, input InviteInput) (*InviteResponse, error) {
	if strings.TrimSpace(idempotencyKey) == "" {
		return nil, platform.Errorf(http.StatusUnprocessableEntity, "validation_error", "Idempotency-Key header is required")
	}
	if strings.TrimSpace(input.Email) == "" {
		return nil, platform.Errorf(http.StatusUnprocessableEntity, "validation_error", "email is required")
	}
	if !isAllowedRole(input.Role) || input.Role == "owner" {
		return nil, platform.Errorf(http.StatusUnprocessableEntity, "validation_error", "role must be admin or member")
	}

	membership, err := s.store.GetMembership(ctx, organizationID, actorUserID)
	if err != nil {
		return nil, translateMembershipError(err)
	}
	if membership.Role != "owner" && membership.Role != "admin" {
		return nil, platform.Errorf(http.StatusForbidden, "forbidden", "only owner or admin can invite members")
	}

	requestHash := hashValues(strings.ToLower(strings.TrimSpace(input.Email)), input.Role)
	if existing, err := s.store.GetInvitationByIdempotency(ctx, organizationID, idempotencyKey); err == nil {
		if existing.RequestHash != nil && *existing.RequestHash != requestHash {
			return nil, platform.Errorf(http.StatusConflict, "idempotency_conflict", "request payload does not match previous idempotent request")
		}
		return &InviteResponse{Invitation: existing, Replayed: true}, nil
	} else if err != nil && !errors.Is(err, repository.ErrNotFound) {
		return nil, err
	}

	rawToken := uuid.NewString() + "." + uuid.NewString()
	tokenHash := auth.HashOpaqueToken(rawToken)
	invitation := repository.Invitation{
		ID:                    uuid.NewString(),
		OrganizationID:        organizationID,
		Email:                 strings.ToLower(strings.TrimSpace(input.Email)),
		Role:                  input.Role,
		InvitedByUserID:       actorUserID,
		RequestIDempotencyKey: stringPointer(idempotencyKey),
		RequestHash:           stringPointer(requestHash),
	}
	created, err := s.store.CreateInvitation(ctx, invitation, tokenHash)
	if err != nil {
		return nil, mapRepositoryError(err)
	}
	return &InviteResponse{
		Invitation:         created,
		AcceptTokenPreview: rawToken,
		Replayed:           false,
	}, nil
}

// AcceptInvitation accepts an invite token, creates membership, and issues tokens.
func (s *Service) AcceptInvitation(ctx context.Context, input AcceptInvitationInput) (*AuthResponse, error) {
	if strings.TrimSpace(input.Token) == "" || strings.TrimSpace(input.DisplayName) == "" || len(strings.TrimSpace(input.Password)) < 8 {
		return nil, platform.Errorf(http.StatusUnprocessableEntity, "validation_error", "token, display_name, and password(>=8 chars) are required")
	}

	passwordHash, err := bcrypt.GenerateFromPassword([]byte(input.Password), bcrypt.DefaultCost)
	if err != nil {
		return nil, err
	}
	user, membership, err := s.store.AcceptInvitation(ctx, auth.HashOpaqueToken(input.Token), strings.TrimSpace(input.DisplayName), string(passwordHash))
	if err != nil {
		return nil, mapRepositoryError(err)
	}
	memberships, err := s.store.ListMembershipsForUser(ctx, user.ID)
	if err != nil {
		return nil, err
	}
	authResponse, err := s.issueAuthResponse(ctx, user, memberships)
	if err != nil {
		return nil, err
	}
	s.metrics.IncAuthLogins()
	_ = membership
	return authResponse, nil
}

// CreateProject inserts one organization project.
func (s *Service) CreateProject(ctx context.Context, actorUserID, organizationID string, input CreateProjectInput) (repository.Project, error) {
	if strings.TrimSpace(input.Name) == "" || strings.TrimSpace(input.ProjectKey) == "" {
		return repository.Project{}, platform.Errorf(http.StatusUnprocessableEntity, "validation_error", "name and project_key are required")
	}
	membership, err := s.store.GetMembership(ctx, organizationID, actorUserID)
	if err != nil {
		return repository.Project{}, translateMembershipError(err)
	}
	if membership.Role != "owner" && membership.Role != "admin" {
		return repository.Project{}, platform.Errorf(http.StatusForbidden, "forbidden", "only owner or admin can create projects")
	}

	project, err := s.store.CreateProject(ctx, organizationID, actorUserID, strings.TrimSpace(input.Name), strings.ToUpper(strings.TrimSpace(input.ProjectKey)))
	if err != nil {
		return repository.Project{}, mapRepositoryError(err)
	}
	s.invalidateDashboardCache(ctx, organizationID)
	return project, nil
}

// ListProjects loads org projects for one actor.
func (s *Service) ListProjects(ctx context.Context, actorUserID, organizationID string) ([]repository.Project, error) {
	if _, err := s.store.GetMembership(ctx, organizationID, actorUserID); err != nil {
		return nil, translateMembershipError(err)
	}
	return s.store.ListProjects(ctx, organizationID)
}

// CreateIssue inserts a new issue with idempotency and outbox emission.
func (s *Service) CreateIssue(ctx context.Context, actorUserID, projectID, idempotencyKey string, input CreateIssueInput) (*IssueResponse, error) {
	if strings.TrimSpace(idempotencyKey) == "" {
		return nil, platform.Errorf(http.StatusUnprocessableEntity, "validation_error", "Idempotency-Key header is required")
	}
	if strings.TrimSpace(input.Title) == "" {
		return nil, platform.Errorf(http.StatusUnprocessableEntity, "validation_error", "title is required")
	}
	project, err := s.store.GetProjectByID(ctx, projectID)
	if err != nil {
		return nil, mapRepositoryError(err)
	}
	organizationID := project.OrganizationID
	if _, err := s.store.GetMembership(ctx, organizationID, actorUserID); err != nil {
		return nil, translateMembershipError(err)
	}
	if input.AssigneeUserID != nil {
		ok, err := s.store.UserBelongsToOrganization(ctx, organizationID, *input.AssigneeUserID)
		if err != nil {
			return nil, err
		}
		if !ok {
			return nil, platform.Errorf(http.StatusUnprocessableEntity, "validation_error", "assignee must belong to the organization")
		}
	}

	requestHash := hashValues(projectID, strings.TrimSpace(input.Title), strings.TrimSpace(input.Description), derefString(input.AssigneeUserID))
	if existing, err := s.store.GetIssueByIdempotency(ctx, projectID, idempotencyKey); err == nil {
		if existing.RequestHash != nil && *existing.RequestHash != requestHash {
			return nil, platform.Errorf(http.StatusConflict, "idempotency_conflict", "request payload does not match previous idempotent request")
		}
		return &IssueResponse{Issue: existing, Replayed: true}, nil
	} else if err != nil && !errors.Is(err, repository.ErrNotFound) {
		return nil, err
	}

	issue := repository.Issue{
		ID:                 uuid.NewString(),
		OrganizationID:     organizationID,
		ProjectID:          projectID,
		Title:              strings.TrimSpace(input.Title),
		Description:        strings.TrimSpace(input.Description),
		Status:             "todo",
		AssigneeUserID:     input.AssigneeUserID,
		CreatedByUserID:    actorUserID,
		RequestIDempotency: stringPointer(idempotencyKey),
		RequestHash:        stringPointer(requestHash),
	}
	payload, err := json.Marshal(map[string]any{
		"issue_id":           issue.ID,
		"project_id":         issue.ProjectID,
		"title":              issue.Title,
		"status":             issue.Status,
		"assignee_user_id":   issue.AssigneeUserID,
		"created_by_user_id": issue.CreatedByUserID,
	})
	if err != nil {
		return nil, err
	}
	created, err := s.store.CreateIssue(ctx, issue, actorUserID, payload)
	if err != nil {
		return nil, mapRepositoryError(err)
	}
	s.invalidateDashboardCache(ctx, organizationID)
	return &IssueResponse{Issue: created}, nil
}

// ListIssues returns issues in one project for an org member.
func (s *Service) ListIssues(ctx context.Context, actorUserID, projectID string) ([]repository.Issue, error) {
	project, err := s.store.GetProjectByID(ctx, projectID)
	if err != nil {
		return nil, mapRepositoryError(err)
	}
	organizationID := project.OrganizationID
	if _, err := s.store.GetMembership(ctx, organizationID, actorUserID); err != nil {
		return nil, translateMembershipError(err)
	}
	return s.store.ListIssues(ctx, organizationID, projectID)
}

// UpdateIssue patches issue state and assignment with optimistic locking.
func (s *Service) UpdateIssue(ctx context.Context, actorUserID, issueID string, input UpdateIssueInput) (*IssueResponse, error) {
	currentIssue, err := s.store.GetIssueByID(ctx, issueID)
	if err != nil {
		return nil, mapRepositoryError(err)
	}
	organizationID := currentIssue.OrganizationID
	if _, err := s.store.GetMembership(ctx, organizationID, actorUserID); err != nil {
		return nil, translateMembershipError(err)
	}
	if input.Version < 1 {
		return nil, platform.Errorf(http.StatusUnprocessableEntity, "validation_error", "version must be >= 1")
	}
	if !isAllowedStatus(input.Status) {
		return nil, platform.Errorf(http.StatusUnprocessableEntity, "validation_error", "status must be todo, in_progress, or done")
	}
	if input.AssigneeUserID != nil {
		ok, err := s.store.UserBelongsToOrganization(ctx, organizationID, *input.AssigneeUserID)
		if err != nil {
			return nil, err
		}
		if !ok {
			return nil, platform.Errorf(http.StatusUnprocessableEntity, "validation_error", "assignee must belong to the organization")
		}
	}

	payload, err := json.Marshal(map[string]any{
		"issue_id":         issueID,
		"status":           input.Status,
		"assignee_user_id": input.AssigneeUserID,
		"version":          input.Version,
	})
	if err != nil {
		return nil, err
	}
	issue, err := s.store.UpdateIssue(ctx, organizationID, issueID, actorUserID, input.Version, input.Status, input.AssigneeUserID, payload)
	if err != nil {
		return nil, mapRepositoryError(err)
	}
	s.invalidateDashboardCache(ctx, organizationID)
	return &IssueResponse{Issue: issue}, nil
}

// AddComment inserts a comment and an outbox event.
func (s *Service) AddComment(ctx context.Context, actorUserID, issueID string, input AddCommentInput) (repository.Comment, error) {
	currentIssue, err := s.store.GetIssueByID(ctx, issueID)
	if err != nil {
		return repository.Comment{}, mapRepositoryError(err)
	}
	organizationID := currentIssue.OrganizationID
	if _, err := s.store.GetMembership(ctx, organizationID, actorUserID); err != nil {
		return repository.Comment{}, translateMembershipError(err)
	}
	if strings.TrimSpace(input.Body) == "" {
		return repository.Comment{}, platform.Errorf(http.StatusUnprocessableEntity, "validation_error", "body is required")
	}
	payload, err := json.Marshal(map[string]any{
		"issue_id": issueID,
		"body":     strings.TrimSpace(input.Body),
	})
	if err != nil {
		return repository.Comment{}, err
	}
	comment, err := s.store.AddComment(ctx, organizationID, issueID, actorUserID, strings.TrimSpace(input.Body), payload)
	if err != nil {
		return repository.Comment{}, mapRepositoryError(err)
	}
	return comment, nil
}

// ListNotifications returns notifications for the actor inside one organization.
func (s *Service) ListNotifications(ctx context.Context, actorUserID, organizationID string, limit int) ([]repository.Notification, error) {
	if _, err := s.store.GetMembership(ctx, organizationID, actorUserID); err != nil {
		return nil, translateMembershipError(err)
	}
	if limit < 1 || limit > 100 {
		limit = 20
	}
	return s.store.ListNotifications(ctx, organizationID, actorUserID, limit)
}

// DashboardSummary returns an org-wide summary with Redis cache fallback.
func (s *Service) DashboardSummary(ctx context.Context, actorUserID, organizationID string) (repository.DashboardSummary, error) {
	if _, err := s.store.GetMembership(ctx, organizationID, actorUserID); err != nil {
		return repository.DashboardSummary{}, translateMembershipError(err)
	}

	payload, err := s.cache.GetDashboardSummary(ctx, organizationID)
	switch {
	case err == nil:
		s.metrics.IncDashboardCacheHit()
		var summary repository.DashboardSummary
		if err := json.Unmarshal(payload, &summary); err == nil {
			return summary, nil
		}
		s.logger.Warn("invalid dashboard cache payload", "organization_id", organizationID)
	case errors.Is(err, cache.ErrUnavailable):
		s.logger.Warn("dashboard cache unavailable, falling back to database", "organization_id", organizationID)
	default:
		s.metrics.IncDashboardCacheMiss()
	}

	summary, err := s.store.BuildDashboardSummary(ctx, organizationID)
	if err != nil {
		return repository.DashboardSummary{}, err
	}

	encoded, err := json.Marshal(summary)
	if err == nil {
		if err := s.cache.SetDashboardSummary(ctx, organizationID, encoded, s.dashboardCacheTTL); err != nil {
			s.logger.Warn("failed to cache dashboard summary", "organization_id", organizationID, "err", err)
		}
	}
	return summary, nil
}

func (s *Service) issueAuthResponse(ctx context.Context, user repository.User, memberships []repository.Membership) (*AuthResponse, error) {
	accessToken, err := auth.SignAccessToken(s.jwtSecret, auth.Claims{
		Sub:   user.ID,
		Email: user.Email,
		Exp:   s.now().Add(s.accessTokenTTL).Unix(),
	})
	if err != nil {
		return nil, err
	}

	sessionID := uuid.NewString()
	rawRefreshToken, tokenHash, err := auth.GenerateRefreshToken(sessionID)
	if err != nil {
		return nil, err
	}
	session := repository.RefreshSession{
		ID:        sessionID,
		UserID:    user.ID,
		TokenHash: tokenHash,
		ExpiresAt: s.now().Add(s.refreshTokenTTL),
	}
	if err := s.store.InsertRefreshSession(ctx, session); err != nil {
		return nil, err
	}
	if err := s.cache.SetRefreshSession(ctx, session.ID, tokenHash, s.refreshTokenTTL); err != nil {
		_ = s.store.RevokeRefreshSession(ctx, session.ID)
		return nil, platform.Errorf(http.StatusServiceUnavailable, "redis_unavailable", "refresh token store is unavailable")
	}
	return &AuthResponse{
		AccessToken:  accessToken,
		RefreshToken: rawRefreshToken,
		User:         user,
		Memberships:  memberships,
	}, nil
}

func (s *Service) invalidateDashboardCache(ctx context.Context, organizationID string) {
	if err := s.cache.DeleteDashboardSummary(ctx, organizationID); err != nil && !errors.Is(err, cache.ErrNotFound) {
		s.logger.Warn("failed to invalidate dashboard cache", "organization_id", organizationID, "err", err)
	}
}

func validateRegisterOwner(input RegisterOwnerInput) error {
	switch {
	case strings.TrimSpace(input.Email) == "":
		return platform.Errorf(http.StatusUnprocessableEntity, "validation_error", "email is required")
	case len(strings.TrimSpace(input.Password)) < 8:
		return platform.Errorf(http.StatusUnprocessableEntity, "validation_error", "password must be at least 8 characters")
	case strings.TrimSpace(input.DisplayName) == "":
		return platform.Errorf(http.StatusUnprocessableEntity, "validation_error", "display_name is required")
	case strings.TrimSpace(input.OrgName) == "":
		return platform.Errorf(http.StatusUnprocessableEntity, "validation_error", "org_name is required")
	case strings.TrimSpace(input.OrgSlug) == "":
		return platform.Errorf(http.StatusUnprocessableEntity, "validation_error", "org_slug is required")
	}
	return nil
}

func mapRepositoryError(err error) error {
	switch {
	case err == nil:
		return nil
	case errors.Is(err, repository.ErrNotFound):
		return platform.Errorf(http.StatusNotFound, "not_found", "requested resource was not found")
	case errors.Is(err, repository.ErrEmailExists):
		return platform.Errorf(http.StatusConflict, "email_exists", "email already exists")
	case errors.Is(err, repository.ErrOrganizationSlugExists):
		return platform.Errorf(http.StatusConflict, "org_slug_exists", "organization slug already exists")
	case errors.Is(err, repository.ErrAlreadyMember):
		return platform.Errorf(http.StatusConflict, "already_member", "user is already a member of this organization")
	case errors.Is(err, repository.ErrPendingInvitation):
		return platform.Errorf(http.StatusConflict, "pending_invitation", "a pending invitation already exists for this email")
	case errors.Is(err, repository.ErrProjectKeyExists):
		return platform.Errorf(http.StatusConflict, "project_key_exists", "project_key already exists in this organization")
	case errors.Is(err, repository.ErrVersionConflict):
		return platform.Errorf(http.StatusConflict, "version_conflict", "issue version conflict")
	case errors.Is(err, repository.ErrIdempotencyConflict):
		return platform.Errorf(http.StatusConflict, "idempotency_conflict", "request payload does not match previous idempotent request")
	default:
		return err
	}
}

func translateMembershipError(err error) error {
	if errors.Is(err, repository.ErrNotFound) {
		return platform.Errorf(http.StatusForbidden, "forbidden", "you are not a member of this organization")
	}
	return err
}

func isAllowedRole(role string) bool {
	return role == "owner" || role == "admin" || role == "member"
}

func isAllowedStatus(status string) bool {
	return status == "todo" || status == "in_progress" || status == "done"
}

func stringPointer(value string) *string {
	return &value
}

func derefString(value *string) string {
	if value == nil {
		return ""
	}
	return *value
}

func hashValues(parts ...string) string {
	sum := sha256.Sum256([]byte(strings.Join(parts, "::")))
	return hex.EncodeToString(sum[:])
}
