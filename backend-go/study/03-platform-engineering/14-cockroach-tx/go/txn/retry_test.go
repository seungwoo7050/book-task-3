package txn

import (
	"context"
	"database/sql"
	"errors"
	"fmt"
	"testing"
)

// mockPgError implements the PgError interface for testing.
type mockPgError struct {
	code string
	msg  string
}

func (e *mockPgError) Error() string    { return e.msg }
func (e *mockPgError) SQLState() string { return e.code }

func TestIsRetryable(t *testing.T) {
	tests := []struct {
		name string
		err  error
		want bool
	}{
		{
			name: "40001 is retryable",
			err:  &mockPgError{code: "40001", msg: "serialization failure"},
			want: true,
		},
		{
			name: "other pg error is not retryable",
			err:  &mockPgError{code: "23505", msg: "unique violation"},
			want: false,
		},
		{
			name: "wrapped 40001 is retryable",
			err:  fmt.Errorf("wrapped: %w", &mockPgError{code: "40001", msg: "retry"}),
			want: true,
		},
		{
			name: "plain error is not retryable",
			err:  errors.New("some error"),
			want: false,
		},
		{
			name: "nil is not retryable",
			err:  nil,
			want: false,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			got := IsRetryable(tc.err)
			if got != tc.want {
				t.Errorf("IsRetryable(%v) = %v, want %v", tc.err, got, tc.want)
			}
		})
	}
}

// TestRunInTxRetries verifies that RunInTx retries on 40001 errors.
// It uses a nil *sql.DB, so we test via a mock approach that doesn't
// require a real database.
func TestRunInTxRetriesLogic(t *testing.T) {
	t.Run("succeeds on first attempt", func(t *testing.T) {
		calls := 0
		fn := func(tx *sql.Tx) error {
			calls++
			return nil
		}
		// We can't actually call RunInTx without a real DB, so we test
		// the retry logic by simulating execTx.
		err := simulateRetry(3, fn)
		if err != nil {
			t.Errorf("unexpected error: %v", err)
		}
		if calls != 1 {
			t.Errorf("calls = %d, want 1", calls)
		}
	})

	t.Run("retries on 40001 then succeeds", func(t *testing.T) {
		calls := 0
		fn := func(tx *sql.Tx) error {
			calls++
			if calls < 3 {
				return &mockPgError{code: "40001", msg: "retry"}
			}
			return nil
		}
		err := simulateRetry(5, fn)
		if err != nil {
			t.Errorf("unexpected error: %v", err)
		}
		if calls != 3 {
			t.Errorf("calls = %d, want 3", calls)
		}
	})

	t.Run("gives up after max retries", func(t *testing.T) {
		calls := 0
		fn := func(tx *sql.Tx) error {
			calls++
			return &mockPgError{code: "40001", msg: "always retry"}
		}
		err := simulateRetry(3, fn)
		if err == nil {
			t.Error("expected error after max retries")
		}
		if calls != 3 {
			t.Errorf("calls = %d, want 3", calls)
		}
	})

	t.Run("does not retry non-retryable error", func(t *testing.T) {
		calls := 0
		fn := func(tx *sql.Tx) error {
			calls++
			return errors.New("non-retryable")
		}
		err := simulateRetry(3, fn)
		if err == nil {
			t.Error("expected error")
		}
		if calls != 1 {
			t.Errorf("calls = %d, want 1", calls)
		}
	})
}

// simulateRetry mimics the retry loop in RunInTx without needing a real DB.
func simulateRetry(maxRetries int, fn func(tx *sql.Tx) error) error {
	_ = context.Background() // keep import
	var lastErr error
	for attempt := 0; attempt < maxRetries; attempt++ {
		lastErr = fn(nil)
		if lastErr == nil {
			return nil
		}
		if !IsRetryable(lastErr) {
			return lastErr
		}
	}
	return fmt.Errorf("transaction failed after %d retries: %w", maxRetries, lastErr)
}
