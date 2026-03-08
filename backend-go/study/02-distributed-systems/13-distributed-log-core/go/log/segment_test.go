package log

import (
	"os"
	"testing"
)

func TestSegmentAppendRead(t *testing.T) {
	dir, err := os.MkdirTemp("", "segment_test")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(dir)

	c := Config{
		MaxStoreBytes: 1024,
		MaxIndexBytes: indexEntryWidth * 10,
	}

	seg, err := newSegment(dir, 16, c)
	if err != nil {
		t.Fatal(err)
	}

	records := [][]byte{
		[]byte("hello"),
		[]byte("world"),
		[]byte("distributed log"),
	}

	for i, r := range records {
		off, err := seg.Append(r)
		if err != nil {
			t.Fatalf("Append(%q): %v", r, err)
		}
		wantOff := uint64(16 + i)
		if off != wantOff {
			t.Errorf("Append(%q): got offset=%d, want %d", r, off, wantOff)
		}
	}

	for i, r := range records {
		got, err := seg.Read(uint64(16 + i))
		if err != nil {
			t.Fatalf("Read(%d): %v", 16+i, err)
		}
		if string(got) != string(r) {
			t.Errorf("Read(%d): got %q, want %q", 16+i, got, r)
		}
	}

	if err := seg.Close(); err != nil {
		t.Fatal(err)
	}
}

func TestSegmentReopen(t *testing.T) {
	dir, err := os.MkdirTemp("", "segment_reopen_test")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(dir)

	c := Config{
		MaxStoreBytes: 1024,
		MaxIndexBytes: indexEntryWidth * 10,
	}

	seg, err := newSegment(dir, 0, c)
	if err != nil {
		t.Fatal(err)
	}

	seg.Append([]byte("first"))
	seg.Append([]byte("second"))
	seg.Close()

	// Reopen same segment.
	seg2, err := newSegment(dir, 0, c)
	if err != nil {
		t.Fatal(err)
	}
	defer seg2.Close()

	// nextOffset should be 2.
	if seg2.nextOffset != 2 {
		t.Errorf("nextOffset after reopen = %d, want 2", seg2.nextOffset)
	}

	// Read existing records.
	got, err := seg2.Read(0)
	if err != nil {
		t.Fatal(err)
	}
	if string(got) != "first" {
		t.Errorf("Read(0) after reopen: got %q, want %q", got, "first")
	}

	// Append more.
	off, err := seg2.Append([]byte("third"))
	if err != nil {
		t.Fatal(err)
	}
	if off != 2 {
		t.Errorf("Append after reopen: got offset=%d, want 2", off)
	}
}

func TestSegmentFull(t *testing.T) {
	dir, err := os.MkdirTemp("", "segment_full_test")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(dir)

	// Very small store limit.
	c := Config{
		MaxStoreBytes: 30, // ~1-2 records with length prefix
		MaxIndexBytes: indexEntryWidth * 10,
	}

	seg, err := newSegment(dir, 0, c)
	if err != nil {
		t.Fatal(err)
	}
	defer seg.Close()

	// First append should succeed.
	_, err = seg.Append([]byte("hello"))
	if err != nil {
		t.Fatalf("first Append: %v", err)
	}

	// Keep appending until full.
	for i := 0; i < 100; i++ {
		_, err = seg.Append([]byte("data"))
		if err == ErrSegmentFull {
			return // expected
		}
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}
	}
	t.Error("segment never became full")
}

func TestSegmentRemove(t *testing.T) {
	dir, err := os.MkdirTemp("", "segment_remove_test")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(dir)

	c := Config{
		MaxStoreBytes: 1024,
		MaxIndexBytes: indexEntryWidth * 10,
	}

	seg, err := newSegment(dir, 0, c)
	if err != nil {
		t.Fatal(err)
	}

	seg.Append([]byte("hello"))

	if err := seg.Remove(); err != nil {
		t.Fatal(err)
	}

	// Files should be gone.
	entries, _ := os.ReadDir(dir)
	if len(entries) != 0 {
		t.Errorf("dir should be empty after Remove, has %d entries", len(entries))
	}
}
