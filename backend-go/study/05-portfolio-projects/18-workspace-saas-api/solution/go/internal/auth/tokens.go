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
	// ErrInvalidToken은 토큰 형식이나 서명이 유효하지 않을 때 반환된다.
	ErrInvalidToken = errors.New("invalid token")
	// ErrExpiredToken은 토큰 만료 시 반환된다.
	ErrExpiredToken = errors.New("expired token")
)

// Claims는 액세스 토큰에 담기는 사용자 클레임이다.
type Claims struct {
	Sub   string `json:"sub"`
	Email string `json:"email"`
	Exp   int64  `json:"exp"`
}

// SignAccessToken은 HMAC으로 서명한 JWT 호환 액세스 토큰을 만든다.
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

// ParseAccessToken은 액세스 토큰의 서명과 만료 시간을 검증한다.
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

// GenerateRefreshToken은 세션 ID와 연결된 refresh token 원문과 해시를 만든다.
func GenerateRefreshToken(sessionID string) (rawToken string, hash string, err error) {
	buf := make([]byte, 32)
	if _, err := rand.Read(buf); err != nil {
		return "", "", err
	}
	secret := base64.RawURLEncoding.EncodeToString(buf)
	rawToken = sessionID + "." + secret
	return rawToken, HashOpaqueToken(rawToken), nil
}

// ParseRefreshToken은 refresh token에서 세션 ID와 토큰 해시를 추출한다.
func ParseRefreshToken(raw string) (sessionID string, tokenHash string, err error) {
	parts := strings.Split(raw, ".")
	if len(parts) != 2 || parts[0] == "" || parts[1] == "" {
		return "", "", ErrInvalidToken
	}
	return parts[0], HashOpaqueToken(raw), nil
}

// HashOpaqueToken은 불투명 토큰 값을 SHA-256으로 해시한다.
func HashOpaqueToken(raw string) string {
	sum := sha256.Sum256([]byte(raw))
	return hex.EncodeToString(sum[:])
}

func sign(secret []byte, value string) string {
	mac := hmac.New(sha256.New, secret)
	mac.Write([]byte(value))
	return base64.RawURLEncoding.EncodeToString(mac.Sum(nil))
}
