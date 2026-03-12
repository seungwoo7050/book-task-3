package lesson

import "testing"

func TestBuildSummary(t *testing.T) {
	t.Parallel()

	summary := BuildSummary("Go makes Go tooling approachable, and Go tests stay fast.")
	if summary.TotalWords != 10 {
		t.Fatalf("total words = %d, want 10", summary.TotalWords)
	}
	if summary.UniqueWords != 8 {
		t.Fatalf("unique words = %d, want 8", summary.UniqueWords)
	}
	if summary.TopWord != "go" {
		t.Fatalf("top word = %q, want go", summary.TopWord)
	}
}

func TestCountWords(t *testing.T) {
	t.Parallel()

	counts := CountWords([]string{"map", "slice", "map"})
	if counts["map"] != 2 {
		t.Fatalf("map count = %d, want 2", counts["map"])
	}
	if counts["slice"] != 1 {
		t.Fatalf("slice count = %d, want 1", counts["slice"])
	}
}
