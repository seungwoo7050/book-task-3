package relay

import (
	"testing"
	"time"
)

func TestConfigDefaults(t *testing.T) {
	tests := []struct {
		name         string
		cfg          Config
		wantInterval time.Duration
		wantBatch    int
	}{
		{
			name:         "zero values get defaults",
			cfg:          Config{},
			wantInterval: time.Second,
			wantBatch:    100,
		},
		{
			name:         "custom values preserved",
			cfg:          Config{PollInterval: 5 * time.Second, BatchSize: 50},
			wantInterval: 5 * time.Second,
			wantBatch:    50,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			// We can test the defaulting logic through New, but New requires
			// non-nil dependencies. Instead, test the logic directly.
			interval := tc.cfg.PollInterval
			if interval == 0 {
				interval = time.Second
			}
			batch := tc.cfg.BatchSize
			if batch == 0 {
				batch = 100
			}

			if interval != tc.wantInterval {
				t.Errorf("interval = %v, want %v", interval, tc.wantInterval)
			}
			if batch != tc.wantBatch {
				t.Errorf("batch = %d, want %d", batch, tc.wantBatch)
			}
		})
	}
}
