package httpapi

import (
	"context"
	"errors"
	"log/slog"
	"math/rand"
	"net/http"
	"strconv"
	"strings"
	"time"

	"github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/auth"
	"github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/platform"
	"github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/service"
)

type contextKey string

const principalContextKey contextKey = "workspace-principal"

// Principal describes the authenticated caller.
type Principal struct {
	UserID string
	Email  string
}

type appHandler func(http.ResponseWriter, *http.Request) error

// Server exposes the HTTP API for the portfolio project.
type Server struct {
	service   *service.Service
	logger    *slog.Logger
	metrics   *platform.Metrics
	jwtSecret []byte
	now       func() time.Time
}

// New constructs an HTTP server with middleware and routes.
func New(svc *service.Service, logger *slog.Logger, metrics *platform.Metrics, jwtSecret []byte) *Server {
	if logger == nil {
		logger = slog.Default()
	}
	if metrics == nil {
		metrics = &platform.Metrics{}
	}
	return &Server{
		service:   svc,
		logger:    logger,
		metrics:   metrics,
		jwtSecret: jwtSecret,
		now:       time.Now,
	}
}

// Routes returns the public HTTP handler tree.
func (s *Server) Routes() http.Handler {
	mux := http.NewServeMux()

	mux.HandleFunc("GET /healthz", s.wrap(s.healthz))
	mux.HandleFunc("GET /readyz", s.wrap(s.readyz))
	mux.HandleFunc("GET /metrics", s.metrics.Handler)

	mux.HandleFunc("POST /v1/auth/register-owner", s.wrap(s.registerOwner))
	mux.HandleFunc("POST /v1/auth/login", s.wrap(s.login))
	mux.HandleFunc("POST /v1/auth/refresh", s.wrap(s.refresh))
	mux.HandleFunc("POST /v1/auth/logout", s.wrap(s.logout))

	mux.HandleFunc("GET /v1/me", s.wrap(s.requireAuth(s.me)))
	mux.HandleFunc("POST /v1/orgs/{orgID}/invitations", s.wrap(s.requireAuth(s.createInvitation)))
	mux.HandleFunc("POST /v1/invitations/accept", s.wrap(s.acceptInvitation))
	mux.HandleFunc("GET /v1/orgs/{orgID}/projects", s.wrap(s.requireAuth(s.listProjects)))
	mux.HandleFunc("POST /v1/orgs/{orgID}/projects", s.wrap(s.requireAuth(s.createProject)))
	mux.HandleFunc("GET /v1/projects/{projectID}/issues", s.wrap(s.requireAuth(s.listIssues)))
	mux.HandleFunc("POST /v1/projects/{projectID}/issues", s.wrap(s.requireAuth(s.createIssue)))
	mux.HandleFunc("PATCH /v1/issues/{issueID}", s.wrap(s.requireAuth(s.updateIssue)))
	mux.HandleFunc("POST /v1/issues/{issueID}/comments", s.wrap(s.requireAuth(s.addComment)))
	mux.HandleFunc("GET /v1/orgs/{orgID}/notifications", s.wrap(s.requireAuth(s.listNotifications)))
	mux.HandleFunc("GET /v1/orgs/{orgID}/dashboard/summary", s.wrap(s.requireAuth(s.dashboardSummary)))

	return s.withObservability(mux)
}

func (s *Server) wrap(next appHandler) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		if err := next(w, r); err != nil {
			var appErr *platform.AppError
			if !errors.As(err, &appErr) {
				s.logger.Error("request failed", "method", r.Method, "path", r.URL.Path, "err", err)
			}
			platform.WriteError(w, err)
		}
	}
}

func (s *Server) requireAuth(next appHandler) appHandler {
	return func(w http.ResponseWriter, r *http.Request) error {
		raw := strings.TrimSpace(strings.TrimPrefix(r.Header.Get("Authorization"), "Bearer "))
		if raw == "" || raw == r.Header.Get("Authorization") {
			return platform.Errorf(http.StatusUnauthorized, "unauthorized", "bearer token is required")
		}
		claims, err := auth.ParseAccessToken(s.jwtSecret, raw, s.now())
		switch {
		case errors.Is(err, auth.ErrInvalidToken), errors.Is(err, auth.ErrExpiredToken):
			return platform.Errorf(http.StatusUnauthorized, "unauthorized", "bearer token is invalid or expired")
		case err != nil:
			return err
		}

		principal := Principal{UserID: claims.Sub, Email: claims.Email}
		ctx := context.WithValue(r.Context(), principalContextKey, principal)
		return next(w, r.WithContext(ctx))
	}
}

func (s *Server) withObservability(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		s.metrics.IncRequests()
		traceID := r.Header.Get("X-Trace-ID")
		if traceID == "" {
			traceID = "trace-" + strconv.FormatInt(rand.Int63(), 36)
		}
		w.Header().Set("X-Trace-ID", traceID)
		s.logger.Info("request", "trace_id", traceID, "method", r.Method, "path", r.URL.Path)
		next.ServeHTTP(w, r)
	})
}

func (s *Server) healthz(w http.ResponseWriter, _ *http.Request) error {
	platform.WriteJSON(w, http.StatusOK, map[string]any{"status": "available"})
	return nil
}

func (s *Server) readyz(w http.ResponseWriter, r *http.Request) error {
	if err := s.service.Ready(r.Context()); err != nil {
		return err
	}
	platform.WriteJSON(w, http.StatusOK, map[string]any{"status": "ready"})
	return nil
}

func (s *Server) registerOwner(w http.ResponseWriter, r *http.Request) error {
	var input service.RegisterOwnerInput
	if err := platform.DecodeJSON(r, &input); err != nil {
		return err
	}
	response, err := s.service.RegisterOwner(r.Context(), input)
	if err != nil {
		return err
	}
	platform.WriteJSON(w, http.StatusCreated, response)
	return nil
}

func (s *Server) login(w http.ResponseWriter, r *http.Request) error {
	var input service.LoginInput
	if err := platform.DecodeJSON(r, &input); err != nil {
		return err
	}
	response, err := s.service.Login(r.Context(), input)
	if err != nil {
		return err
	}
	platform.WriteJSON(w, http.StatusOK, response)
	return nil
}

func (s *Server) refresh(w http.ResponseWriter, r *http.Request) error {
	var input service.RefreshInput
	if err := platform.DecodeJSON(r, &input); err != nil {
		return err
	}
	response, err := s.service.Refresh(r.Context(), input)
	if err != nil {
		return err
	}
	platform.WriteJSON(w, http.StatusOK, response)
	return nil
}

func (s *Server) logout(w http.ResponseWriter, r *http.Request) error {
	var input service.LogoutInput
	if err := platform.DecodeJSON(r, &input); err != nil {
		return err
	}
	if err := s.service.Logout(r.Context(), input); err != nil {
		return err
	}
	w.WriteHeader(http.StatusNoContent)
	return nil
}

func (s *Server) me(w http.ResponseWriter, r *http.Request) error {
	principal, err := principalFromContext(r.Context())
	if err != nil {
		return err
	}
	response, err := s.service.Me(r.Context(), principal.UserID)
	if err != nil {
		return err
	}
	platform.WriteJSON(w, http.StatusOK, response)
	return nil
}

func (s *Server) createInvitation(w http.ResponseWriter, r *http.Request) error {
	principal, err := principalFromContext(r.Context())
	if err != nil {
		return err
	}
	var input service.InviteInput
	if err := platform.DecodeJSON(r, &input); err != nil {
		return err
	}
	response, err := s.service.InviteMember(r.Context(), principal.UserID, r.PathValue("orgID"), r.Header.Get("Idempotency-Key"), input)
	if err != nil {
		return err
	}
	status := http.StatusCreated
	if response.Replayed {
		status = http.StatusOK
	}
	platform.WriteJSON(w, status, response)
	return nil
}

func (s *Server) acceptInvitation(w http.ResponseWriter, r *http.Request) error {
	var input service.AcceptInvitationInput
	if err := platform.DecodeJSON(r, &input); err != nil {
		return err
	}
	response, err := s.service.AcceptInvitation(r.Context(), input)
	if err != nil {
		return err
	}
	platform.WriteJSON(w, http.StatusOK, response)
	return nil
}

func (s *Server) listProjects(w http.ResponseWriter, r *http.Request) error {
	principal, err := principalFromContext(r.Context())
	if err != nil {
		return err
	}
	projects, err := s.service.ListProjects(r.Context(), principal.UserID, r.PathValue("orgID"))
	if err != nil {
		return err
	}
	platform.WriteJSON(w, http.StatusOK, map[string]any{"projects": projects})
	return nil
}

func (s *Server) createProject(w http.ResponseWriter, r *http.Request) error {
	principal, err := principalFromContext(r.Context())
	if err != nil {
		return err
	}
	var input service.CreateProjectInput
	if err := platform.DecodeJSON(r, &input); err != nil {
		return err
	}
	project, err := s.service.CreateProject(r.Context(), principal.UserID, r.PathValue("orgID"), input)
	if err != nil {
		return err
	}
	platform.WriteJSON(w, http.StatusCreated, map[string]any{"project": project})
	return nil
}

func (s *Server) listIssues(w http.ResponseWriter, r *http.Request) error {
	principal, err := principalFromContext(r.Context())
	if err != nil {
		return err
	}
	issues, err := s.service.ListIssues(r.Context(), principal.UserID, r.PathValue("projectID"))
	if err != nil {
		return err
	}
	platform.WriteJSON(w, http.StatusOK, map[string]any{"issues": issues})
	return nil
}

func (s *Server) createIssue(w http.ResponseWriter, r *http.Request) error {
	principal, err := principalFromContext(r.Context())
	if err != nil {
		return err
	}
	var input service.CreateIssueInput
	if err := platform.DecodeJSON(r, &input); err != nil {
		return err
	}
	response, err := s.service.CreateIssue(r.Context(), principal.UserID, r.PathValue("projectID"), r.Header.Get("Idempotency-Key"), input)
	if err != nil {
		return err
	}
	status := http.StatusCreated
	if response.Replayed {
		status = http.StatusOK
	}
	platform.WriteJSON(w, status, response)
	return nil
}

func (s *Server) updateIssue(w http.ResponseWriter, r *http.Request) error {
	principal, err := principalFromContext(r.Context())
	if err != nil {
		return err
	}
	var input service.UpdateIssueInput
	if err := platform.DecodeJSON(r, &input); err != nil {
		return err
	}
	response, err := s.service.UpdateIssue(r.Context(), principal.UserID, r.PathValue("issueID"), input)
	if err != nil {
		return err
	}
	platform.WriteJSON(w, http.StatusOK, response)
	return nil
}

func (s *Server) addComment(w http.ResponseWriter, r *http.Request) error {
	principal, err := principalFromContext(r.Context())
	if err != nil {
		return err
	}
	var input service.AddCommentInput
	if err := platform.DecodeJSON(r, &input); err != nil {
		return err
	}
	comment, err := s.service.AddComment(r.Context(), principal.UserID, r.PathValue("issueID"), input)
	if err != nil {
		return err
	}
	platform.WriteJSON(w, http.StatusCreated, map[string]any{"comment": comment})
	return nil
}

func (s *Server) listNotifications(w http.ResponseWriter, r *http.Request) error {
	principal, err := principalFromContext(r.Context())
	if err != nil {
		return err
	}
	limit, _ := strconv.Atoi(r.URL.Query().Get("limit"))
	notifications, err := s.service.ListNotifications(r.Context(), principal.UserID, r.PathValue("orgID"), limit)
	if err != nil {
		return err
	}
	platform.WriteJSON(w, http.StatusOK, map[string]any{"notifications": notifications})
	return nil
}

func (s *Server) dashboardSummary(w http.ResponseWriter, r *http.Request) error {
	principal, err := principalFromContext(r.Context())
	if err != nil {
		return err
	}
	summary, err := s.service.DashboardSummary(r.Context(), principal.UserID, r.PathValue("orgID"))
	if err != nil {
		return err
	}
	platform.WriteJSON(w, http.StatusOK, map[string]any{"summary": summary})
	return nil
}

func principalFromContext(ctx context.Context) (Principal, error) {
	principal, ok := ctx.Value(principalContextKey).(Principal)
	if !ok {
		return Principal{}, platform.Errorf(http.StatusUnauthorized, "unauthorized", "authentication required")
	}
	return principal, nil
}

func init() {
	rand.Seed(time.Now().UnixNano())
}
