package txn

import (
	"context"
	"database/sql"
	"errors"
	"fmt"
	"math/rand"
	"time"
)

// RetryableErrorCode is SQLSTATE code for serialization failures.
const RetryableErrorCode = "40001"

// sqlStateError matches pg error types that expose SQLSTATE.
type sqlStateError interface {
	error
	SQLState() string
}

// IsRetryable reports whether err should trigger transaction retry.
func IsRetryable(err error) bool {
	var se sqlStateError
	if errors.As(err, &se) {
		return se.SQLState() == RetryableErrorCode
	}
	return false
}

// RunInTx runs fn in a SERIALIZABLE transaction with retry on SQLSTATE 40001.
func RunInTx(ctx context.Context, db *sql.DB, maxRetries int, fn func(tx *sql.Tx) error) error {
	if maxRetries <= 0 {
		maxRetries = 3
	}

	var lastErr error
	for attempt := 0; attempt < maxRetries; attempt++ {
		lastErr = runOnce(ctx, db, fn)
		if lastErr == nil {
			return nil
		}
		if !IsRetryable(lastErr) {
			return lastErr
		}
		if attempt == maxRetries-1 {
			break
		}
		if err := sleepWithContext(ctx, backoff(attempt)); err != nil {
			return err
		}
	}

	return fmt.Errorf("transaction failed after %d retries: %w", maxRetries, lastErr)
}

func runOnce(ctx context.Context, db *sql.DB, fn func(tx *sql.Tx) error) error {
	tx, err := db.BeginTx(ctx, &sql.TxOptions{Isolation: sql.LevelSerializable})
	if err != nil {
		return fmt.Errorf("begin tx: %w", err)
	}

	if err := fn(tx); err != nil {
		_ = tx.Rollback()
		return err
	}

	if err := tx.Commit(); err != nil {
		return err
	}
	return nil
}

func backoff(attempt int) time.Duration {
	base := 40 * time.Millisecond
	jitter := time.Duration(rand.Intn(30)) * time.Millisecond
	return time.Duration(1<<attempt)*base + jitter
}

func sleepWithContext(ctx context.Context, d time.Duration) error {
	timer := time.NewTimer(d)
	defer timer.Stop()

	select {
	case <-ctx.Done():
		return ctx.Err()
	case <-timer.C:
		return nil
	}
}
