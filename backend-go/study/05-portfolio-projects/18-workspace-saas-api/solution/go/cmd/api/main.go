package main

import (
	"context"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"strconv"
	"syscall"
	"time"

	"github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/cache"
	"github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/httpapi"
	"github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/platform"
	"github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/repository"
	"github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/service"
)

func main() {
	cfg := platform.LoadConfig()
	logger := slog.New(slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelInfo}))
	metrics := &platform.Metrics{}

	ctx := context.Background()
	store, err := repository.Open(ctx, cfg.DatabaseURL)
	if err != nil {
		logger.Error("open database", "err", err)
		os.Exit(1)
	}
	defer store.Close()

	cacheClient := cache.New(cfg.RedisAddr, cfg.RedisPassword, cfg.RedisDB)
	svc := service.New(store, cacheClient, logger, metrics, cfg)
	server := httpapi.New(svc, logger, metrics, cfg.JWTSecret)

	httpServer := &http.Server{
		Addr:         ":" + strconv.Itoa(cfg.Port),
		Handler:      server.Routes(),
		ReadTimeout:  5 * time.Second,
		WriteTimeout: 10 * time.Second,
		IdleTimeout:  time.Minute,
	}

	shutdownDone := make(chan struct{})
	go func() {
		quit := make(chan os.Signal, 1)
		signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
		<-quit

		shutdownCtx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()
		_ = httpServer.Shutdown(shutdownCtx)
		close(shutdownDone)
	}()

	logger.Info("workspace saas api listening", "port", cfg.Port)
	if err := httpServer.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		logger.Error("listen and serve", "err", err)
		os.Exit(1)
	}
	<-shutdownDone
}
