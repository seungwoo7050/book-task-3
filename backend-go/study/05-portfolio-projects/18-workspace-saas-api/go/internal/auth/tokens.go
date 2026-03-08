package auth

import (
	"crypto/hmac"
	"crypto/rand"
	"crypto/sha256"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"errors"
	"strings"
	"time"
)

var (
	// ErrInvalidToken is returned when token format or signature is invalid.
	ErrInvalidToken = errors.New("invalid token")
	// ErrExpiredToken is returned when token expiration is in the past.
	ErrExpiredToken = errors.New("expired token")
)

// Claims represents access token claims.
type Claims struct {
	Sub   string `json:"sub"`
	Email string `json:"email"`
	Exp   int64  `json:"exp"`
}

// SignAccessToken creates an HMAC-signed JWT-compatible token.
func SignAccessToken(secret []byte, claims Claims) (string, error) {
	header := base64.RawURLEncoding.EncodeToString([]byte(`{"alg":"HS256","typ":"JWT"}`))
	payloadBytes, err := json.Marshal(claims)
	if err != nil {
		return "", err
	}
	payload := base64.RawURLEncoding.EncodeToString(payloadBytes)
	unsigned := header + "." + payload
	signature := sign(secret, unsigned)
	return unsigned + "." + signature, nil
}

// ParseAccessToken verifies token signature and expiration.
func ParseAccessToken(secret []byte, token string, now time.Time) (Claims, error) {
	parts := strings.Split(token, ".")
	if len(parts) != 3 {
		return Claims{}, ErrInvalidToken
	}
	unsigned := parts[0] + "." + parts[1]
	expected := sign(secret, unsigned)
	if !hmac.Equal([]byte(expected), []byte(parts[2])) {
		return Claims{}, ErrInvalidToken
	}

	payloadBytes, err := base64.RawURLEncoding.DecodeString(parts[1])
	if err != nil {
		return Claims{}, ErrInvalidToken
	}

	var claims Claims
	if err := json.Unmarshal(payloadBytes, &claims); err != nil {
		return Claims{}, ErrInvalidToken
	}
	if claims.Exp <= now.Unix() {
		return Claims{}, ErrExpiredToken
	}
	return claims, nil
}

// GenerateRefreshToken creates an opaque refresh token prefixed with a session id.
func GenerateRefreshToken(sessionID string) (rawToken string, hash string, err error) {
	buf := make([]byte, 32)
	if _, err := rand.Read(buf); err != nil {
		return "", "", err
	}
	secret := base64.RawURLEncoding.EncodeToString(buf)
	rawToken = sessionID + "." + secret
	return rawToken, HashOpaqueToken(rawToken), nil
}

// ParseRefreshToken extracts the session id and hash for lookup.
func ParseRefreshToken(raw string) (sessionID string, tokenHash string, err error) {
	parts := strings.Split(raw, ".")
	if len(parts) != 2 || parts[0] == "" || parts[1] == "" {
		return "", "", ErrInvalidToken
	}
	return parts[0], HashOpaqueToken(raw), nil
}

// HashOpaqueToken returns the SHA-256 hash of the raw token.
func HashOpaqueToken(raw string) string {
	sum := sha256.Sum256([]byte(raw))
	return hex.EncodeToString(sum[:])
}

func sign(secret []byte, value string) string {
	mac := hmac.New(sha256.New, secret)
	mac.Write([]byte(value))
	return base64.RawURLEncoding.EncodeToString(mac.Sum(nil))
}
