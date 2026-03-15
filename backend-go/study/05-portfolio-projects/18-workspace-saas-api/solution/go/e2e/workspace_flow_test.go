//go:build e2e
// +build e2e

package e2e

import (
	"bytes"
	"context"
	"database/sql"
	"encoding/json"
	"io"
	"log/slog"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/redis/go-redis/v9"

	"github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/cache"
	"github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/httpapi"
	"github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/platform"
	"github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/repository"
	"github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/service"
	workerpkg "github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/worker"
)

func TestWorkspaceSaaSFlow(t *testing.T) {
	t.Parallel()

	ctx := context.Background()
	cfg := platform.LoadConfig()
	store, err := repository.Open(ctx, cfg.DatabaseURL)
	if err != nil {
		t.Fatalf("open store: %v", err)
	}
	defer store.Close()

	if err := resetDatabase(ctx, store.DB()); err != nil {
		t.Fatalf("reset database: %v", err)
	}
	if err := flushRedis(ctx, cfg); err != nil {
		t.Fatalf("flush redis: %v", err)
	}

	logger := slog.New(slog.NewTextHandler(io.Discard, nil))
	metrics := &platform.Metrics{}
	cacheClient := cache.New(cfg.RedisAddr, cfg.RedisPassword, cfg.RedisDB)
	svc := service.New(store, cacheClient, logger, metrics, cfg)
	server := httptest.NewServer(httpapi.New(svc, logger, metrics, cfg.JWTSecret).Routes())
	defer server.Close()

	worker := workerpkg.New(store, cacheClient, logger, metrics)
	client := server.Client()

	owner := mustJSON(t, client, "POST", server.URL+"/v1/auth/register-owner", "", map[string]any{
		"email":        "owner@example.com",
		"password":     "OwnerPass123!",
		"display_name": "Owner",
		"org_name":     "Workspace",
		"org_slug":     "workspace-main",
	}, http.StatusCreated)
	ownerAccess := owner["access_token"].(string)
	ownerRefresh := owner["refresh_token"].(string)
	orgID := owner["memberships"].([]any)[0].(map[string]any)["organization_id"].(string)

	projectResp := mustJSON(t, client, "POST", server.URL+"/v1/orgs/"+orgID+"/projects", ownerAccess, map[string]any{
		"name":        "Operations",
		"project_key": "OPS",
	}, http.StatusCreated)
	projectID := projectResp["project"].(map[string]any)["id"].(string)

	inviteResp := mustJSONWithHeaders(t, client, "POST", server.URL+"/v1/orgs/"+orgID+"/invitations", ownerAccess, map[string]any{
		"email": "member@example.com",
		"role":  "member",
	}, http.StatusCreated, map[string]string{"Idempotency-Key": "invite-1"})
	inviteToken := inviteResp["accept_token_preview"].(string)

	acceptResp := mustJSON(t, client, "POST", server.URL+"/v1/invitations/accept", "", map[string]any{
		"token":        inviteToken,
		"display_name": "Member",
		"password":     "MemberPass123!",
	}, http.StatusOK)
	memberAccess := acceptResp["access_token"].(string)
	memberID := acceptResp["user"].(map[string]any)["id"].(string)

	issueResp := mustJSONWithHeaders(t, client, "POST", server.URL+"/v1/projects/"+projectID+"/issues", memberAccess, map[string]any{
		"title":       "Investigate lag",
		"description": "Summary cache needs profiling",
	}, http.StatusCreated, map[string]string{"Idempotency-Key": "issue-1"})
	issue := issueResp["issue"].(map[string]any)
	issueID := issue["id"].(string)
	issueVersion := int(issue["version"].(float64))

	replayed := mustJSONWithHeaders(t, client, "POST", server.URL+"/v1/projects/"+projectID+"/issues", memberAccess, map[string]any{
		"title":       "Investigate lag",
		"description": "Summary cache needs profiling",
	}, http.StatusOK, map[string]string{"Idempotency-Key": "issue-1"})
	if replayed["issue"].(map[string]any)["id"].(string) != issueID {
		t.Fatalf("idempotent replay returned a different issue")
	}

	mustStatus(t, client, "PATCH", server.URL+"/v1/issues/"+issueID, ownerAccess, map[string]any{
		"status":           "done",
		"assignee_user_id": memberID,
		"version":          999,
	}, http.StatusConflict)

	updated := mustJSON(t, client, "PATCH", server.URL+"/v1/issues/"+issueID, ownerAccess, map[string]any{
		"status":           "in_progress",
		"assignee_user_id": memberID,
		"version":          issueVersion,
	}, http.StatusOK)
	if updated["issue"].(map[string]any)["status"].(string) != "in_progress" {
		t.Fatalf("unexpected issue update response: %#v", updated)
	}

	mustJSON(t, client, "POST", server.URL+"/v1/issues/"+issueID+"/comments", memberAccess, map[string]any{
		"body": "Profiling complete, caching helps.",
	}, http.StatusCreated)

	processed, err := worker.RunOnce(ctx)
	if err != nil {
		t.Fatalf("worker RunOnce: %v", err)
	}
	if processed < 1 {
		t.Fatalf("worker processed %d events, want >= 1", processed)
	}
	if processedAgain, err := worker.RunOnce(ctx); err != nil {
		t.Fatalf("worker RunOnce second pass: %v", err)
	} else if processedAgain != 0 {
		t.Fatalf("worker second pass processed %d events, want 0", processedAgain)
	}

	notifications := mustJSON(t, client, "GET", server.URL+"/v1/orgs/"+orgID+"/notifications", ownerAccess, nil, http.StatusOK)
	if len(notifications["notifications"].([]any)) < 1 {
		t.Fatalf("expected at least one notification")
	}

	summary := mustJSON(t, client, "GET", server.URL+"/v1/orgs/"+orgID+"/dashboard/summary", ownerAccess, nil, http.StatusOK)
	summaryBody := summary["summary"].(map[string]any)
	if int(summaryBody["projects_total"].(float64)) != 1 {
		t.Fatalf("unexpected projects_total: %#v", summaryBody)
	}
	if int(summaryBody["issues_in_progress"].(float64)) != 1 {
		t.Fatalf("unexpected issues_in_progress: %#v", summaryBody)
	}
	if int(summaryBody["unread_notifications"].(float64)) < 1 {
		t.Fatalf("unexpected unread_notifications: %#v", summaryBody)
	}

	secondOwner := mustJSON(t, client, "POST", server.URL+"/v1/auth/register-owner", "", map[string]any{
		"email":        "owner2@example.com",
		"password":     "OwnerPass123!",
		"display_name": "Owner Two",
		"org_name":     "Workspace Two",
		"org_slug":     "workspace-two",
	}, http.StatusCreated)
	secondAccess := secondOwner["access_token"].(string)
	mustStatus(t, client, "GET", server.URL+"/v1/orgs/"+orgID+"/projects", secondAccess, nil, http.StatusForbidden)

	refreshed := mustJSON(t, client, "POST", server.URL+"/v1/auth/refresh", "", map[string]any{
		"refresh_token": ownerRefresh,
	}, http.StatusOK)
	newRefresh := refreshed["refresh_token"].(string)
	mustStatus(t, client, "POST", server.URL+"/v1/auth/logout", "", map[string]any{
		"refresh_token": newRefresh,
	}, http.StatusNoContent)
	mustStatus(t, client, "POST", server.URL+"/v1/auth/refresh", "", map[string]any{
		"refresh_token": newRefresh,
	}, http.StatusUnauthorized)
}

func mustJSON(t *testing.T, client *http.Client, method, url, bearer string, payload any, status int) map[string]any {
	t.Helper()
	return mustJSONWithHeaders(t, client, method, url, bearer, payload, status, nil)
}

func mustJSONWithHeaders(t *testing.T, client *http.Client, method, url, bearer string, payload any, status int, headers map[string]string) map[string]any {
	t.Helper()

	var body io.Reader
	if payload != nil {
		encoded, err := json.Marshal(payload)
		if err != nil {
			t.Fatalf("marshal payload: %v", err)
		}
		body = bytes.NewReader(encoded)
	}

	req, err := http.NewRequest(method, url, body)
	if err != nil {
		t.Fatalf("new request: %v", err)
	}
	if payload != nil {
		req.Header.Set("Content-Type", "application/json")
	}
	if bearer != "" {
		req.Header.Set("Authorization", "Bearer "+bearer)
	}
	for key, value := range headers {
		req.Header.Set(key, value)
	}

	resp, err := client.Do(req)
	if err != nil {
		t.Fatalf("do request: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != status {
		buf, _ := io.ReadAll(resp.Body)
		t.Fatalf("%s %s status = %d, want %d; body=%s", method, url, resp.StatusCode, status, strings.TrimSpace(string(buf)))
	}

	if status == http.StatusNoContent {
		return nil
	}
	var out map[string]any
	if err := json.NewDecoder(resp.Body).Decode(&out); err != nil {
		t.Fatalf("decode response: %v", err)
	}
	return out
}

func mustStatus(t *testing.T, client *http.Client, method, url, bearer string, payload any, status int) {
	t.Helper()
	_ = mustJSON(t, client, method, url, bearer, payload, status)
}

func resetDatabase(ctx context.Context, db *sql.DB) error {
	_, err := db.ExecContext(ctx, `
TRUNCATE TABLE
    notifications,
    outbox_events,
    comments,
    issues,
    projects,
    invitations,
    organization_memberships,
    refresh_sessions,
    organizations,
    users
CASCADE
`)
	return err
}

func flushRedis(ctx context.Context, cfg platform.Config) error {
	client := redis.NewClient(&redis.Options{
		Addr:     cfg.RedisAddr,
		Password: cfg.RedisPassword,
		DB:       cfg.RedisDB,
	})
	defer client.Close()
	return client.FlushDB(ctx).Err()
}
