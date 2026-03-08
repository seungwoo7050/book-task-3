package config

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

// Config holds runtime settings for the API and relay worker.
type Config struct {
	Addr            string
	DatabaseURL     string
	RelayInterval   time.Duration
	RelayBatchSize  int
	RateLimitRPS    int
	ShutdownTimeout time.Duration
}

// Load builds config from environment variables with sane defaults.
func Load() (Config, error) {
	cfg := Config{
		Addr:            getEnv("ADDR", ":8080"),
		DatabaseURL:     getEnv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/game_store?sslmode=disable"),
		RelayInterval:   time.Second,
		RelayBatchSize:  50,
		RateLimitRPS:    30,
		ShutdownTimeout: 10 * time.Second,
	}

	if v := os.Getenv("RELAY_INTERVAL"); v != "" {
		d, err := time.ParseDuration(v)
		if err != nil {
			return Config{}, fmt.Errorf("parse RELAY_INTERVAL: %w", err)
		}
		cfg.RelayInterval = d
	}

	if v := os.Getenv("RELAY_BATCH_SIZE"); v != "" {
		n, err := strconv.Atoi(v)
		if err != nil || n <= 0 {
			return Config{}, fmt.Errorf("invalid RELAY_BATCH_SIZE: %q", v)
		}
		cfg.RelayBatchSize = n
	}

	if v := os.Getenv("RATE_LIMIT_RPS"); v != "" {
		n, err := strconv.Atoi(v)
		if err != nil || n <= 0 {
			return Config{}, fmt.Errorf("invalid RATE_LIMIT_RPS: %q", v)
		}
		cfg.RateLimitRPS = n
	}

	if v := os.Getenv("SHUTDOWN_TIMEOUT"); v != "" {
		d, err := time.ParseDuration(v)
		if err != nil {
			return Config{}, fmt.Errorf("parse SHUTDOWN_TIMEOUT: %w", err)
		}
		cfg.ShutdownTimeout = d
	}

	return cfg, nil
}

func getEnv(key, fallback string) string {
	v := os.Getenv(key)
	if v == "" {
		return fallback
	}
	return v
}
