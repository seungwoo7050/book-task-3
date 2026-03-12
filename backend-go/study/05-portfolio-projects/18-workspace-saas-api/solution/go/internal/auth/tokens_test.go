package auth

import (
	"testing"
	"time"
)

func TestAccessTokenRoundTrip(t *testing.T) {
	t.Parallel()

	token, err := SignAccessToken([]byte("secret"), Claims{
		Sub:   "user-1",
		Email: "owner@example.com",
		Exp:   time.Now().Add(time.Minute).Unix(),
	})
	if err != nil {
		t.Fatalf("SignAccessToken() error = %v", err)
	}

	claims, err := ParseAccessToken([]byte("secret"), token, time.Now())
	if err != nil {
		t.Fatalf("ParseAccessToken() error = %v", err)
	}
	if claims.Sub != "user-1" || claims.Email != "owner@example.com" {
		t.Fatalf("claims = %#v", claims)
	}
}

func TestRefreshTokenRoundTrip(t *testing.T) {
	t.Parallel()

	raw, hash, err := GenerateRefreshToken("session-1")
	if err != nil {
		t.Fatalf("GenerateRefreshToken() error = %v", err)
	}

	sessionID, parsedHash, err := ParseRefreshToken(raw)
	if err != nil {
		t.Fatalf("ParseRefreshToken() error = %v", err)
	}
	if sessionID != "session-1" {
		t.Fatalf("sessionID = %q, want %q", sessionID, "session-1")
	}
	if parsedHash != hash {
		t.Fatalf("hash = %q, want %q", parsedHash, hash)
	}
}
