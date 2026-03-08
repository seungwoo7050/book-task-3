// Package txn provides a generic transaction retry helper for CockroachDB.
package txn

import (
	"context"
	"database/sql"
	"errors"
	"fmt"
)

// RetryableErrorCode is the SQLSTATE code for CockroachDB serialization errors.
const RetryableErrorCode = "40001"

// PgError is a minimal interface matching *pgconn.PgError so we
// don't import pgx in this package.
type PgError interface {
	error
	SQLState() string
}

// IsRetryable returns true if the error is a CockroachDB serialization
// failure (SQLSTATE 40001) that should be retried.
func IsRetryable(err error) bool {
	var pgErr PgError
	if errors.As(err, &pgErr) {
		return pgErr.SQLState() == RetryableErrorCode
	}
	return false
}

// RunInTx executes fn within a database transaction. If the commit fails
// with a retryable error (40001), the entire transaction is retried up to
// maxRetries times. fn must be safe to call multiple times.
func RunInTx(ctx context.Context, db *sql.DB, maxRetries int, fn func(tx *sql.Tx) error) error {
	if maxRetries <= 0 {
		maxRetries = 3
	}

	var lastErr error
	for attempt := 0; attempt < maxRetries; attempt++ {
		lastErr = execTx(ctx, db, fn)
		if lastErr == nil {
			return nil
		}
		if !IsRetryable(lastErr) {
			return lastErr
		}
		// Retryable error — loop again.
	}
	return fmt.Errorf("transaction failed after %d retries: %w", maxRetries, lastErr)
}

// execTx runs fn in a single transaction attempt.
func execTx(ctx context.Context, db *sql.DB, fn func(tx *sql.Tx) error) error {
	tx, err := db.BeginTx(ctx, &sql.TxOptions{
		Isolation: sql.LevelSerializable,
	})
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
