package analyzer

import (
	"fmt"
	"sync"
	"testing"
)

func TestParseLine(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name    string
		line    string
		wantErr bool
	}{
		{name: "valid", line: "search,120"},
		{name: "missing comma", line: "search", wantErr: true},
		{name: "empty category", line: ",10", wantErr: true},
	}

	for _, tc := range tests {
		tc := tc
		t.Run(tc.name, func(t *testing.T) {
			t.Parallel()
			_, err := ParseLine(tc.line)
			if tc.wantErr && err == nil {
				t.Fatalf("expected error for %q", tc.line)
			}
			if !tc.wantErr && err != nil {
				t.Fatalf("unexpected error: %v", err)
			}
		})
	}
}

func TestSummarize(t *testing.T) {
	t.Parallel()

	summaries, err := Summarize([]string{"search,100", "search,200", "checkout,90"})
	if err != nil {
		t.Fatalf("summarize error: %v", err)
	}
	if summaries["search"].AverageMS != 150 {
		t.Fatalf("search average = %d, want 150", summaries["search"].AverageMS)
	}
	if summaries["checkout"].Count != 1 {
		t.Fatalf("checkout count = %d, want 1", summaries["checkout"].Count)
	}
}

func TestRecorderSnapshot(t *testing.T) {
	t.Parallel()

	recorder := &Recorder{}
	var wg sync.WaitGroup
	for i := 0; i < 20; i++ {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()
			recorder.Add(Event{Category: "worker", DurationMS: i})
		}(i)
	}
	wg.Wait()
	if got := len(recorder.Snapshot()); got != 20 {
		t.Fatalf("snapshot len = %d, want 20", got)
	}
}

func BenchmarkSummarize(b *testing.B) {
	lines := make([]string, 0, 1000)
	for i := 0; i < 1000; i++ {
		lines = append(lines, fmt.Sprintf("search,%d", i%300))
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		if _, err := Summarize(lines); err != nil {
			b.Fatal(err)
		}
	}
}
