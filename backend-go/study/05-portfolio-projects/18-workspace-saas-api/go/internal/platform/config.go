package platform

import (
	"os"
	"strconv"
	"time"
)

// Config holds runtime configuration for API and worker binaries.
type Config struct {
	AppEnv             string
	Port               int
	DatabaseURL        string
	RedisAddr          string
	RedisPassword      string
	RedisDB            int
	JWTSecret          []byte
	AccessTokenTTL     time.Duration
	RefreshTokenTTL    time.Duration
	WorkerPollInterval time.Duration
	DashboardCacheTTL  time.Duration
}

// LoadConfig reads configuration from environment variables.
func LoadConfig() Config {
	return Config{
		AppEnv:             envString("APP_ENV", "development"),
		Port:               envInt("PORT", 4080),
		DatabaseURL:        envString("DATABASE_URL", "postgres://postgres:postgres@localhost:54339/workspace_saas?sslmode=disable"),
		RedisAddr:          envString("REDIS_ADDR", "localhost:6381"),
		RedisPassword:      envString("REDIS_PASSWORD", ""),
		RedisDB:            envInt("REDIS_DB", 0),
		JWTSecret:          []byte(envString("JWT_SECRET", "workspace-saas-secret")),
		AccessTokenTTL:     envDuration("ACCESS_TOKEN_TTL", 15*time.Minute),
		RefreshTokenTTL:    envDuration("REFRESH_TOKEN_TTL", 7*24*time.Hour),
		WorkerPollInterval: envDuration("WORKER_POLL_INTERVAL", 300*time.Millisecond),
		DashboardCacheTTL:  envDuration("DASHBOARD_CACHE_TTL", 30*time.Second),
	}
}

func envString(key, fallback string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return fallback
}

func envInt(key string, fallback int) int {
	if value := os.Getenv(key); value != "" {
		if n, err := strconv.Atoi(value); err == nil {
			return n
		}
	}
	return fallback
}

func envDuration(key string, fallback time.Duration) time.Duration {
	if value := os.Getenv(key); value != "" {
		if duration, err := time.ParseDuration(value); err == nil {
			return duration
		}
	}
	return fallback
}
