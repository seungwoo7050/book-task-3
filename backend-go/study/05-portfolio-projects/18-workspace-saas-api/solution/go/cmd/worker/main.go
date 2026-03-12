package main

import (
	"context"
	"log/slog"
	"os"
	"os/signal"
	"syscall"

	"github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/cache"
	"github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/platform"
	"github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/repository"
	workerpkg "github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/worker"
)

func main() {
	cfg := platform.LoadConfig()
	logger := slog.New(slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelInfo}))
	metrics := &platform.Metrics{}

	store, err := repository.Open(context.Background(), cfg.DatabaseURL)
	if err != nil {
		logger.Error("open database", "err", err)
		os.Exit(1)
	}
	defer store.Close()

	cacheClient := cache.New(cfg.RedisAddr, cfg.RedisPassword, cfg.RedisDB)
	processor := workerpkg.New(store, cacheClient, logger, metrics)

	ctx, cancel := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
	defer cancel()

	logger.Info("workspace saas worker started", "interval", cfg.WorkerPollInterval.String())
	if err := processor.Run(ctx, cfg.WorkerPollInterval); err != nil && err != context.Canceled {
		logger.Error("worker stopped with error", "err", err)
		os.Exit(1)
	}
}
