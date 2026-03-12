package txn

import (
	"context"
	"database/sql"
	"errors"
	"fmt"
)

const RetryableErrorCode = "40001"

type PgError interface {
	error
	SQLState() string
}

func IsRetryable(err error) bool {
	var pgErr PgError
	if errors.As(err, &pgErr) {
		return pgErr.SQLState() == RetryableErrorCode
	}
	return false
}
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
	}
	return fmt.Errorf("transaction failed after %d retries: %w", maxRetries, lastErr)
}
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
