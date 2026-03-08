package main

import (
	"context"
	"database/sql"
	"errors"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"sync"
	"syscall"
	"time"

	_ "github.com/jackc/pgx/v5/stdlib"

	"github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/config"
	"github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/httpapi"
	"github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/relay"
	"github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/repository"
	"github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone/internal/service"
)

func main() {
	logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))

	cfg, err := config.Load()
	if err != nil {
		logger.Error("load config", "err", err)
		os.Exit(1)
	}

	db, err := sql.Open("pgx", cfg.DatabaseURL)
	if err != nil {
		logger.Error("open database", "err", err)
		os.Exit(1)
	}
	defer db.Close()

	db.SetMaxOpenConns(20)
	db.SetMaxIdleConns(10)
	db.SetConnMaxLifetime(5 * time.Minute)

	pingCtx, pingCancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer pingCancel()
	if err := db.PingContext(pingCtx); err != nil {
		logger.Error("ping database", "err", err)
		os.Exit(1)
	}

	store := repository.NewStore(db)
	purchaseService := service.NewPurchaseService(db, store)
	queryService := service.NewQueryService(store)
	api := httpapi.NewAPI(purchaseService, queryService, logger, cfg.RateLimitRPS)

	srv := &http.Server{
		Addr:         cfg.Addr,
		Handler:      api.Routes(),
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 15 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	relayRunner := relay.New(
		store,
		relay.NewLogPublisher(logger),
		logger,
		cfg.RelayInterval,
		cfg.RelayBatchSize,
	)

	runCtx, runCancel := context.WithCancel(context.Background())
	defer runCancel()

	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		if err := relayRunner.Run(runCtx); err != nil && !errors.Is(err, context.Canceled) {
			logger.Error("relay stopped with error", "err", err)
		}
	}()

	serverErrCh := make(chan error, 1)
	go func() {
		logger.Info("http server listening", "addr", cfg.Addr)
		if err := srv.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
			serverErrCh <- err
			return
		}
		serverErrCh <- nil
	}()

	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)

	select {
	case err := <-serverErrCh:
		if err != nil {
			logger.Error("server error", "err", err)
		}
	case sig := <-sigCh:
		logger.Info("received shutdown signal", "signal", sig.String())
	}

	runCancel()

	shutdownCtx, shutdownCancel := context.WithTimeout(context.Background(), cfg.ShutdownTimeout)
	defer shutdownCancel()
	if err := srv.Shutdown(shutdownCtx); err != nil {
		logger.Error("server shutdown", "err", err)
	}

	wg.Wait()
	logger.Info("server stopped")
}
