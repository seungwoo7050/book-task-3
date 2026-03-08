package txn

import (
	"errors"
	"fmt"
	"testing"
)

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
			name: "serialization failure is retryable",
			err:  &mockPgError{code: RetryableErrorCode, msg: "retry"},
			want: true,
		},
		{
			name: "different sqlstate is not retryable",
			err:  &mockPgError{code: "23505", msg: "unique violation"},
			want: false,
		},
		{
			name: "wrapped serialization failure is retryable",
			err:  fmt.Errorf("wrapped: %w", &mockPgError{code: RetryableErrorCode, msg: "retry"}),
			want: true,
		},
		{
			name: "plain error is not retryable",
			err:  errors.New("boom"),
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
				t.Fatalf("IsRetryable(%v) = %v, want %v", tc.err, got, tc.want)
			}
		})
	}
}
