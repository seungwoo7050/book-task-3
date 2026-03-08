package tests

import (
	"testing"

	"study.local/database-internals/01-memtable-skiplist/internal/skiplist"
)

func TestPutAndGet(t *testing.T) {
	list := skiplist.New()
	list.Put("hello", "world")

	value, state := list.Get("hello")
	if state != skiplist.Present {
		t.Fatalf("expected present state, got %v", state)
	}
	if value != "world" {
		t.Fatalf("expected world, got %q", value)
	}
}

func TestMissingKey(t *testing.T) {
	list := skiplist.New()

	_, state := list.Get("missing")
	if state != skiplist.Missing {
		t.Fatalf("expected missing state, got %v", state)
	}
}

func TestUpdateKeepsLogicalSize(t *testing.T) {
	list := skiplist.New()
	list.Put("key", "v1")
	list.Put("key", "v2")

	value, state := list.Get("key")
	if state != skiplist.Present || value != "v2" {
		t.Fatalf("expected updated value, got %q / %v", value, state)
	}
	if list.Size() != 1 {
		t.Fatalf("expected logical size 1, got %d", list.Size())
	}
}

func TestManyInserts(t *testing.T) {
	list := skiplist.New()
	for i := 0; i < 1000; i++ {
		list.Put(paddedKey(i), "value")
	}

	if list.Size() != 1000 {
		t.Fatalf("expected 1000 records, got %d", list.Size())
	}
	if _, state := list.Get("key:0500"); state != skiplist.Present {
		t.Fatalf("expected key:0500 to exist")
	}
}

func TestDeleteProducesTombstone(t *testing.T) {
	list := skiplist.New()
	list.Put("a", "1")
	list.Delete("a")

	_, state := list.Get("a")
	if state != skiplist.Tombstone {
		t.Fatalf("expected tombstone, got %v", state)
	}
	if list.Size() != 1 {
		t.Fatalf("expected tombstone to keep size 1, got %d", list.Size())
	}
}

func TestEntriesStaySorted(t *testing.T) {
	list := skiplist.New()
	list.Put("c", "3")
	list.Put("a", "1")
	list.Put("b", "2")

	entries := list.Entries()
	if len(entries) != 3 {
		t.Fatalf("expected 3 entries, got %d", len(entries))
	}
	if entries[0].Key != "a" || entries[1].Key != "b" || entries[2].Key != "c" {
		t.Fatalf("unexpected order: %+v", entries)
	}
}

func TestEntriesIncludeTombstones(t *testing.T) {
	list := skiplist.New()
	list.Put("x", "1")
	list.Put("y", "2")
	list.Delete("x")

	entries := list.Entries()
	if len(entries) != 2 {
		t.Fatalf("expected 2 entries, got %d", len(entries))
	}
	if entries[0].Value != nil {
		t.Fatalf("expected first entry to be a tombstone")
	}
}

func TestByteSizeTracking(t *testing.T) {
	list := skiplist.New()
	if list.ByteSize() != 0 {
		t.Fatalf("expected empty byte size 0, got %d", list.ByteSize())
	}

	list.Put("key", "value")
	if list.ByteSize() <= 0 {
		t.Fatalf("expected positive byte size, got %d", list.ByteSize())
	}
}

func TestClear(t *testing.T) {
	list := skiplist.New()
	list.Put("a", "1")
	list.Put("b", "2")
	list.Clear()

	if list.Size() != 0 {
		t.Fatalf("expected size 0 after clear, got %d", list.Size())
	}
	if list.ByteSize() != 0 {
		t.Fatalf("expected byte size 0 after clear, got %d", list.ByteSize())
	}
	if _, state := list.Get("a"); state != skiplist.Missing {
		t.Fatalf("expected cleared key to be missing")
	}
}

func paddedKey(index int) string {
	return "key:" + leftPad(index)
}

func leftPad(value int) string {
	switch {
	case value < 10:
		return "000" + string(rune('0'+value))
	case value < 100:
		return "00" + itoa(value)
	case value < 1000:
		return "0" + itoa(value)
	default:
		return itoa(value)
	}
}

func itoa(value int) string {
	if value == 0 {
		return "0"
	}

	buffer := make([]byte, 0, 4)
	for value > 0 {
		buffer = append([]byte{byte('0' + value%10)}, buffer...)
		value /= 10
	}
	return string(buffer)
}
