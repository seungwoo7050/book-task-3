package log

import (
	"fmt"
	"os"
	"testing"
)

func TestLogAppendRead(t *testing.T) {
	dir, err := os.MkdirTemp("", "log_test")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(dir)

	c := Config{
		MaxStoreBytes: 1024,
		MaxIndexBytes: indexEntryWidth * 100,
	}

	l, err := NewLog(dir, c)
	if err != nil {
		t.Fatal(err)
	}
	defer l.Close()

	records := [][]byte{
		[]byte("record-0"),
		[]byte("record-1"),
		[]byte("record-2"),
	}

	for i, r := range records {
		off, err := l.Append(r)
		if err != nil {
			t.Fatalf("Append(%q): %v", r, err)
		}
		if off != uint64(i) {
			t.Errorf("Append(%q): got offset=%d, want %d", r, off, i)
		}
	}

	for i, r := range records {
		got, err := l.Read(uint64(i))
		if err != nil {
			t.Fatalf("Read(%d): %v", i, err)
		}
		if string(got) != string(r) {
			t.Errorf("Read(%d): got %q, want %q", i, got, r)
		}
	}

	// Read out of range.
	_, err = l.Read(999)
	if err == nil {
		t.Error("Read(999) should return error")
	}
}

func TestLogMultipleSegments(t *testing.T) {
	dir, err := os.MkdirTemp("", "log_multi_seg_test")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(dir)

	// Small store so segments fill quickly.
	c := Config{
		MaxStoreBytes: 32, // ~1 record per segment (8 len + data)
		MaxIndexBytes: indexEntryWidth * 10,
	}

	l, err := NewLog(dir, c)
	if err != nil {
		t.Fatal(err)
	}
	defer l.Close()

	numRecords := 5
	for i := 0; i < numRecords; i++ {
		data := fmt.Appendf(nil, "rec-%d", i)
		off, err := l.Append(data)
		if err != nil {
			t.Fatalf("Append(%d): %v", i, err)
		}
		if off != uint64(i) {
			t.Errorf("offset = %d, want %d", off, i)
		}
	}

	// Should have created multiple segments.
	if len(l.segments) < 2 {
		t.Errorf("expected multiple segments, got %d", len(l.segments))
	}

	// Read all records back.
	for i := 0; i < numRecords; i++ {
		got, err := l.Read(uint64(i))
		if err != nil {
			t.Fatalf("Read(%d): %v", i, err)
		}
		want := fmt.Sprintf("rec-%d", i)
		if string(got) != want {
			t.Errorf("Read(%d): got %q, want %q", i, got, want)
		}
	}
}

func TestLogRestore(t *testing.T) {
	dir, err := os.MkdirTemp("", "log_restore_test")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(dir)

	c := Config{
		MaxStoreBytes: 1024,
		MaxIndexBytes: indexEntryWidth * 100,
	}

	l, err := NewLog(dir, c)
	if err != nil {
		t.Fatal(err)
	}

	l.Append([]byte("alpha"))
	l.Append([]byte("beta"))
	l.Append([]byte("gamma"))
	l.Close()

	// Restore.
	l2, err := NewLog(dir, c)
	if err != nil {
		t.Fatal(err)
	}
	defer l2.Close()

	if l2.LowestOffset() != 0 {
		t.Errorf("LowestOffset = %d, want 0", l2.LowestOffset())
	}
	if l2.HighestOffset() != 2 {
		t.Errorf("HighestOffset = %d, want 2", l2.HighestOffset())
	}

	got, err := l2.Read(1)
	if err != nil {
		t.Fatal(err)
	}
	if string(got) != "beta" {
		t.Errorf("Read(1) after restore: got %q, want %q", got, "beta")
	}

	// Continue appending.
	off, err := l2.Append([]byte("delta"))
	if err != nil {
		t.Fatal(err)
	}
	if off != 3 {
		t.Errorf("Append after restore: got offset=%d, want 3", off)
	}
}

func TestLogTruncate(t *testing.T) {
	dir, err := os.MkdirTemp("", "log_truncate_test")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(dir)

	c := Config{
		MaxStoreBytes: 32,
		MaxIndexBytes: indexEntryWidth * 10,
	}

	l, err := NewLog(dir, c)
	if err != nil {
		t.Fatal(err)
	}
	defer l.Close()

	for i := 0; i < 5; i++ {
		l.Append([]byte(fmt.Sprintf("rec-%d", i)))
	}

	segsBefore := len(l.segments)

	// Truncate segments whose highest offset < 3.
	if err := l.Truncate(3); err != nil {
		t.Fatal(err)
	}

	if len(l.segments) >= segsBefore {
		t.Error("Truncate should have removed some segments")
	}
}

func TestLogReset(t *testing.T) {
	dir, err := os.MkdirTemp("", "log_reset_test")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(dir)

	c := Config{
		MaxStoreBytes: 1024,
		MaxIndexBytes: indexEntryWidth * 100,
	}

	l, err := NewLog(dir, c)
	if err != nil {
		t.Fatal(err)
	}

	l.Append([]byte("before-reset"))

	if err := l.Reset(); err != nil {
		t.Fatal(err)
	}

	if l.HighestOffset() != 0 {
		t.Errorf("HighestOffset after reset = %d, want 0", l.HighestOffset())
	}

	// Append after reset.
	off, err := l.Append([]byte("after-reset"))
	if err != nil {
		t.Fatal(err)
	}
	if off != 0 {
		t.Errorf("offset after reset = %d, want 0", off)
	}

	if err := l.Close(); err != nil {
		t.Fatal(err)
	}
}

func BenchmarkLogAppend(b *testing.B) {
	dir, err := os.MkdirTemp("", "log_bench")
	if err != nil {
		b.Fatal(err)
	}
	defer os.RemoveAll(dir)

	c := Config{
		MaxStoreBytes: 64 * 1024 * 1024,
		MaxIndexBytes: 4 * 1024 * 1024,
	}

	l, err := NewLog(dir, c)
	if err != nil {
		b.Fatal(err)
	}
	defer l.Close()

	data := make([]byte, 256)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		if _, err := l.Append(data); err != nil {
			b.Fatal(err)
		}
	}
}
