package log

import (
	"os"
	"testing"
)

func TestIndexWriteRead(t *testing.T) {
	f, err := os.CreateTemp("", "index_test")
	if err != nil {
		t.Fatal(err)
	}
	defer os.Remove(f.Name())

	maxBytes := uint64(1024)
	idx, err := newIndex(f, maxBytes)
	if err != nil {
		t.Fatal(err)
	}

	entries := []struct {
		off uint32
		pos uint64
	}{
		{0, 0},
		{1, 13},
		{2, 30},
		{3, 100},
	}

	for _, e := range entries {
		if err := idx.Write(e.off, e.pos); err != nil {
			t.Fatalf("Write(off=%d, pos=%d): %v", e.off, e.pos, err)
		}
	}

	if idx.Entries() != uint64(len(entries)) {
		t.Errorf("Entries() = %d, want %d", idx.Entries(), len(entries))
	}

	// Read each entry.
	for i, e := range entries {
		off, pos, err := idx.Read(int64(i))
		if err != nil {
			t.Fatalf("Read(%d): %v", i, err)
		}
		if off != e.off || pos != e.pos {
			t.Errorf("Read(%d): got (off=%d, pos=%d), want (off=%d, pos=%d)",
				i, off, pos, e.off, e.pos)
		}
	}

	// Read last entry with -1.
	off, pos, err := idx.Read(-1)
	if err != nil {
		t.Fatalf("Read(-1): %v", err)
	}
	last := entries[len(entries)-1]
	if off != last.off || pos != last.pos {
		t.Errorf("Read(-1): got (off=%d, pos=%d), want (off=%d, pos=%d)",
			off, pos, last.off, last.pos)
	}

	if err := idx.Close(); err != nil {
		t.Fatal(err)
	}

	// Verify file was truncated to actual size.
	fi, err := os.Stat(f.Name())
	if err != nil {
		t.Fatal(err)
	}
	wantSize := int64(len(entries)) * indexEntryWidth
	if fi.Size() != wantSize {
		t.Errorf("file size after close = %d, want %d", fi.Size(), wantSize)
	}
}

func TestIndexReadEmpty(t *testing.T) {
	f, err := os.CreateTemp("", "index_empty_test")
	if err != nil {
		t.Fatal(err)
	}
	defer os.Remove(f.Name())

	idx, err := newIndex(f, 1024)
	if err != nil {
		t.Fatal(err)
	}
	defer idx.Close()

	_, _, err = idx.Read(0)
	if err != ErrIndexEmpty {
		t.Errorf("Read(0) on empty index: got err=%v, want %v", err, ErrIndexEmpty)
	}

	_, _, err = idx.Read(-1)
	if err != ErrIndexEmpty {
		t.Errorf("Read(-1) on empty index: got err=%v, want %v", err, ErrIndexEmpty)
	}
}

func TestIndexFull(t *testing.T) {
	f, err := os.CreateTemp("", "index_full_test")
	if err != nil {
		t.Fatal(err)
	}
	defer os.Remove(f.Name())

	// Only room for 2 entries.
	maxBytes := uint64(indexEntryWidth * 2)
	idx, err := newIndex(f, maxBytes)
	if err != nil {
		t.Fatal(err)
	}
	defer idx.Close()

	if err := idx.Write(0, 0); err != nil {
		t.Fatal(err)
	}
	if err := idx.Write(1, 13); err != nil {
		t.Fatal(err)
	}
	// Third write should fail.
	if err := idx.Write(2, 30); err != ErrIndexFull {
		t.Errorf("Write on full index: got err=%v, want %v", err, ErrIndexFull)
	}
}

func TestIndexReopen(t *testing.T) {
	f, err := os.CreateTemp("", "index_reopen_test")
	if err != nil {
		t.Fatal(err)
	}
	name := f.Name()
	defer os.Remove(name)

	idx, err := newIndex(f, 1024)
	if err != nil {
		t.Fatal(err)
	}

	if err := idx.Write(0, 0); err != nil {
		t.Fatal(err)
	}
	if err := idx.Write(1, 100); err != nil {
		t.Fatal(err)
	}
	if err := idx.Close(); err != nil {
		t.Fatal(err)
	}

	// Reopen.
	f2, err := os.OpenFile(name, os.O_RDWR, 0644)
	if err != nil {
		t.Fatal(err)
	}
	idx2, err := newIndex(f2, 1024)
	if err != nil {
		t.Fatal(err)
	}
	defer idx2.Close()

	if idx2.Entries() != 2 {
		t.Errorf("reopened index entries = %d, want 2", idx2.Entries())
	}

	off, pos, err := idx2.Read(1)
	if err != nil {
		t.Fatal(err)
	}
	if off != 1 || pos != 100 {
		t.Errorf("Read(1) after reopen: got (off=%d, pos=%d), want (1, 100)", off, pos)
	}
}
