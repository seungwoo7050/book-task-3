package auth

import (
	"crypto/hmac"
	"crypto/rand"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"strings"
	"sync"
	"time"

	"golang.org/x/crypto/bcrypt"
)

var (
	errUnauthorized = errors.New("unauthorized")
	errForbidden    = errors.New("forbidden")
)

type User struct {
	Email        string
	Role         string
	PasswordHash []byte
}

type Session struct {
	Email     string
	Role      string
	ExpiresAt time.Time
}

type Claims struct {
	Sub  string `json:"sub"`
	Role string `json:"role"`
	Exp  int64  `json:"exp"`
}

type Server struct {
	mu       sync.Mutex
	now      func() time.Time
	users    map[string]User
	sessions map[string]Session
	secret   []byte
}

func NewServer(now func() time.Time) (*Server, error) {
	if now == nil {
		now = time.Now
	}
	adminHash, err := bcrypt.GenerateFromPassword([]byte("swordfish"), bcrypt.DefaultCost)
	if err != nil {
		return nil, err
	}
	playerHash, err := bcrypt.GenerateFromPassword([]byte("adventurer"), bcrypt.DefaultCost)
	if err != nil {
		return nil, err
	}

	return &Server{
		now: now,
		users: map[string]User{
			"admin@example.com":  {Email: "admin@example.com", Role: "admin", PasswordHash: adminHash},
			"player@example.com": {Email: "player@example.com", Role: "player", PasswordHash: playerHash},
		},
		sessions: make(map[string]Session),
		secret:   []byte("study-secret-key"),
	}, nil
}

func (s *Server) Routes() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("POST /login/session", s.loginSession)
	mux.HandleFunc("POST /login/jwt", s.loginJWT)
	mux.HandleFunc("GET /me/session", s.requireSession(s.me))
	mux.HandleFunc("GET /me/jwt", s.requireBearer(s.me))
	mux.HandleFunc("GET /admin", s.requireAnyAuth(s.requireRole("admin", s.admin)))
	return mux
}

func (s *Server) loginSession(w http.ResponseWriter, r *http.Request) {
	user, err := s.authenticateCredentials(r)
	if err != nil {
		writeError(w, http.StatusUnauthorized, "invalid credentials")
		return
	}

	token, err := randomToken()
	if err != nil {
		writeError(w, http.StatusInternalServerError, "could not create session")
		return
	}

	s.mu.Lock()
	s.sessions[token] = Session{
		Email:     user.Email,
		Role:      user.Role,
		ExpiresAt: s.now().Add(30 * time.Minute),
	}
	s.mu.Unlock()

	http.SetCookie(w, &http.Cookie{
		Name:     "session_token",
		Value:    token,
		HttpOnly: true,
		Path:     "/",
		Expires:  s.now().Add(30 * time.Minute),
	})
	writeJSON(w, http.StatusOK, map[string]any{"email": user.Email, "role": user.Role})
}

func (s *Server) loginJWT(w http.ResponseWriter, r *http.Request) {
	user, err := s.authenticateCredentials(r)
	if err != nil {
		writeError(w, http.StatusUnauthorized, "invalid credentials")
		return
	}

	token, err := s.signClaims(Claims{
		Sub:  user.Email,
		Role: user.Role,
		Exp:  s.now().Add(15 * time.Minute).Unix(),
	})
	if err != nil {
		writeError(w, http.StatusInternalServerError, "could not sign token")
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{"token": token})
}

func (s *Server) me(w http.ResponseWriter, _ *http.Request, claims Claims) {
	writeJSON(w, http.StatusOK, map[string]any{
		"email": claims.Sub,
		"role":  claims.Role,
	})
}

func (s *Server) admin(w http.ResponseWriter, _ *http.Request, claims Claims) {
	writeJSON(w, http.StatusOK, map[string]any{
		"message": "admin access granted",
		"email":   claims.Sub,
	})
}

func (s *Server) requireSession(next func(http.ResponseWriter, *http.Request, Claims)) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		claims, err := s.claimsFromSession(r)
		if err != nil {
			writeError(w, http.StatusUnauthorized, "invalid session")
			return
		}
		next(w, r, claims)
	}
}

func (s *Server) requireBearer(next func(http.ResponseWriter, *http.Request, Claims)) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		claims, err := s.claimsFromBearer(r)
		if err != nil {
			writeError(w, http.StatusUnauthorized, "invalid bearer token")
			return
		}
		next(w, r, claims)
	}
}

func (s *Server) requireAnyAuth(next func(http.ResponseWriter, *http.Request, Claims)) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		if claims, err := s.claimsFromBearer(r); err == nil {
			next(w, r, claims)
			return
		}
		if claims, err := s.claimsFromSession(r); err == nil {
			next(w, r, claims)
			return
		}
		writeError(w, http.StatusUnauthorized, "authentication required")
	}
}

func (s *Server) requireRole(role string, next func(http.ResponseWriter, *http.Request, Claims)) func(http.ResponseWriter, *http.Request, Claims) {
	return func(w http.ResponseWriter, r *http.Request, claims Claims) {
		if claims.Role != role {
			writeError(w, http.StatusForbidden, "forbidden")
			return
		}
		next(w, r, claims)
	}
}

func (s *Server) authenticateCredentials(r *http.Request) (User, error) {
	var input struct {
		Email    string `json:"email"`
		Password string `json:"password"`
	}
	if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
		return User{}, errUnauthorized
	}

	user, ok := s.users[input.Email]
	if !ok {
		return User{}, errUnauthorized
	}
	if err := bcrypt.CompareHashAndPassword(user.PasswordHash, []byte(input.Password)); err != nil {
		return User{}, errUnauthorized
	}
	return user, nil
}

func (s *Server) claimsFromSession(r *http.Request) (Claims, error) {
	cookie, err := r.Cookie("session_token")
	if err != nil {
		return Claims{}, errUnauthorized
	}

	s.mu.Lock()
	session, ok := s.sessions[cookie.Value]
	s.mu.Unlock()
	if !ok || session.ExpiresAt.Before(s.now()) {
		return Claims{}, errUnauthorized
	}
	return Claims{
		Sub:  session.Email,
		Role: session.Role,
		Exp:  session.ExpiresAt.Unix(),
	}, nil
}

func (s *Server) claimsFromBearer(r *http.Request) (Claims, error) {
	raw := strings.TrimPrefix(r.Header.Get("Authorization"), "Bearer ")
	if raw == "" || raw == r.Header.Get("Authorization") {
		return Claims{}, errUnauthorized
	}
	return s.verifyToken(raw)
}

func (s *Server) signClaims(claims Claims) (string, error) {
	headerPayload := []string{
		base64.RawURLEncoding.EncodeToString([]byte(`{"alg":"HS256","typ":"JWT"}`)),
	}

	payloadBytes, err := json.Marshal(claims)
	if err != nil {
		return "", err
	}
	headerPayload = append(headerPayload, base64.RawURLEncoding.EncodeToString(payloadBytes))
	unsigned := strings.Join(headerPayload, ".")
	signature := s.sign(unsigned)
	return unsigned + "." + signature, nil
}

func (s *Server) verifyToken(token string) (Claims, error) {
	parts := strings.Split(token, ".")
	if len(parts) != 3 {
		return Claims{}, errUnauthorized
	}

	unsigned := parts[0] + "." + parts[1]
	if !hmac.Equal([]byte(parts[2]), []byte(s.sign(unsigned))) {
		return Claims{}, errUnauthorized
	}

	payload, err := base64.RawURLEncoding.DecodeString(parts[1])
	if err != nil {
		return Claims{}, errUnauthorized
	}
	var claims Claims
	if err := json.Unmarshal(payload, &claims); err != nil {
		return Claims{}, errUnauthorized
	}
	if claims.Exp < s.now().Unix() {
		return Claims{}, errUnauthorized
	}
	return claims, nil
}

func (s *Server) sign(unsigned string) string {
	mac := hmac.New(sha256.New, s.secret)
	mac.Write([]byte(unsigned))
	return base64.RawURLEncoding.EncodeToString(mac.Sum(nil))
}

func randomToken() (string, error) {
	var buf [16]byte
	if _, err := rand.Read(buf[:]); err != nil {
		return "", err
	}
	return base64.RawURLEncoding.EncodeToString(buf[:]), nil
}

func writeJSON(w http.ResponseWriter, status int, payload map[string]any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(payload)
}

func writeError(w http.ResponseWriter, status int, message string) {
	writeJSON(w, status, map[string]any{"error": map[string]string{"message": message}})
}

func (s *Server) ForceSecret(secret string) {
	s.secret = []byte(secret)
}

func (s *Server) IssueTokenForTests(claims Claims) string {
	token, err := s.signClaims(claims)
	if err != nil {
		panic(fmt.Sprintf("test token: %v", err))
	}
	return token
}
