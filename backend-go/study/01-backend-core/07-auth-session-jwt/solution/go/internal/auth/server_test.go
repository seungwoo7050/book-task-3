package auth

import (
	"bytes"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

func newTestServer(t *testing.T) *Server {
	t.Helper()
	server, err := NewServer(func() time.Time {
		return time.Unix(1_700_000_000, 0)
	})
	if err != nil {
		t.Fatalf("new server: %v", err)
	}
	return server
}

func TestSessionLoginAndProtectedResource(t *testing.T) {
	t.Parallel()

	server := newTestServer(t)
	loginReq := httptest.NewRequest(http.MethodPost, "/login/session", bytes.NewBufferString(`{"email":"player@example.com","password":"adventurer"}`))
	loginRR := httptest.NewRecorder()
	server.Routes().ServeHTTP(loginRR, loginReq)

	if loginRR.Code != http.StatusOK {
		t.Fatalf("login status = %d, want %d", loginRR.Code, http.StatusOK)
	}

	meReq := httptest.NewRequest(http.MethodGet, "/me/session", nil)
	for _, cookie := range loginRR.Result().Cookies() {
		meReq.AddCookie(cookie)
	}
	meRR := httptest.NewRecorder()
	server.Routes().ServeHTTP(meRR, meReq)

	if meRR.Code != http.StatusOK {
		t.Fatalf("me status = %d, want %d", meRR.Code, http.StatusOK)
	}
}

func TestJWTProtectedResource(t *testing.T) {
	t.Parallel()

	server := newTestServer(t)
	loginReq := httptest.NewRequest(http.MethodPost, "/login/jwt", bytes.NewBufferString(`{"email":"player@example.com","password":"adventurer"}`))
	loginRR := httptest.NewRecorder()
	server.Routes().ServeHTTP(loginRR, loginReq)

	if loginRR.Code != http.StatusOK {
		t.Fatalf("login status = %d, want %d", loginRR.Code, http.StatusOK)
	}

	token := loginRR.Body.String()
	meReq := httptest.NewRequest(http.MethodGet, "/me/jwt", nil)
	meReq.Header.Set("Authorization", "Bearer "+extractToken(token))
	meRR := httptest.NewRecorder()
	server.Routes().ServeHTTP(meRR, meReq)

	if meRR.Code != http.StatusOK {
		t.Fatalf("me status = %d, want %d", meRR.Code, http.StatusOK)
	}
}

func TestForbiddenRole(t *testing.T) {
	t.Parallel()

	server := newTestServer(t)
	req := httptest.NewRequest(http.MethodGet, "/admin", nil)
	req.Header.Set("Authorization", "Bearer "+server.IssueTokenForTests(Claims{
		Sub:  "player@example.com",
		Role: "player",
		Exp:  time.Unix(1_700_000_000, 0).Add(15 * time.Minute).Unix(),
	}))
	rr := httptest.NewRecorder()

	server.Routes().ServeHTTP(rr, req)
	if rr.Code != http.StatusForbidden {
		t.Fatalf("status = %d, want %d", rr.Code, http.StatusForbidden)
	}
}

func TestExpiredToken(t *testing.T) {
	t.Parallel()

	server := newTestServer(t)
	req := httptest.NewRequest(http.MethodGet, "/me/jwt", nil)
	req.Header.Set("Authorization", "Bearer "+server.IssueTokenForTests(Claims{
		Sub:  "player@example.com",
		Role: "player",
		Exp:  time.Unix(1_700_000_000, 0).Add(-time.Minute).Unix(),
	}))
	rr := httptest.NewRecorder()

	server.Routes().ServeHTTP(rr, req)
	if rr.Code != http.StatusUnauthorized {
		t.Fatalf("status = %d, want %d", rr.Code, http.StatusUnauthorized)
	}
}

func TestInvalidSignature(t *testing.T) {
	t.Parallel()

	server := newTestServer(t)
	other := newTestServer(t)
	other.ForceSecret("different-secret")

	req := httptest.NewRequest(http.MethodGet, "/me/jwt", nil)
	req.Header.Set("Authorization", "Bearer "+other.IssueTokenForTests(Claims{
		Sub:  "player@example.com",
		Role: "player",
		Exp:  time.Unix(1_700_000_000, 0).Add(15 * time.Minute).Unix(),
	}))
	rr := httptest.NewRecorder()

	server.Routes().ServeHTTP(rr, req)
	if rr.Code != http.StatusUnauthorized {
		t.Fatalf("status = %d, want %d", rr.Code, http.StatusUnauthorized)
	}
}

func extractToken(body string) string {
	const prefix = `{"token":"`
	body = body[len(prefix):]
	return body[:len(body)-3]
}
