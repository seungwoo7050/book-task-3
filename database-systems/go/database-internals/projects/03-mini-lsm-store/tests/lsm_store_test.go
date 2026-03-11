package tests

import (
	"testing"

	"study.local/go/database-internals/projects/03-mini-lsm-store/internal/lsmstore"
)

func TestPutAndGet(t *testing.T) {
	store := openStore(t, 1024)

	if err := store.Put("greeting", "hello"); err != nil {
		t.Fatalf("put failed: %v", err)
	}
	value, found, err := store.Get("greeting")
	if err != nil {
		t.Fatalf("get failed: %v", err)
	}
	if !found || value == nil || *value != "hello" {
		t.Fatalf("expected hello, got found=%v value=%v", found, value)
	}
}

func TestMissingKey(t *testing.T) {
	store := openStore(t, 1024)
	value, found, err := store.Get("nope")
	if err != nil {
		t.Fatalf("get failed: %v", err)
	}
	if found || value != nil {
		t.Fatalf("expected missing value, got found=%v value=%v", found, value)
	}
}

func TestUpdate(t *testing.T) {
	store := openStore(t, 1024)
	if err := store.Put("k", "v1"); err != nil {
		t.Fatal(err)
	}
	if err := store.Put("k", "v2"); err != nil {
		t.Fatal(err)
	}
	value, found, err := store.Get("k")
	if err != nil {
		t.Fatal(err)
	}
	if !found || value == nil || *value != "v2" {
		t.Fatalf("expected v2, got found=%v value=%v", found, value)
	}
}

func TestDelete(t *testing.T) {
	store := openStore(t, 1024)
	if err := store.Put("k", "v"); err != nil {
		t.Fatal(err)
	}
	if err := store.Delete("k"); err != nil {
		t.Fatal(err)
	}
	value, found, err := store.Get("k")
	if err != nil {
		t.Fatal(err)
	}
	if !found || value != nil {
		t.Fatalf("expected tombstone, got found=%v value=%v", found, value)
	}
}

func TestFlushCreatesSSTable(t *testing.T) {
	store := openStore(t, 512)
	for i := 0; i < 50; i++ {
		if err := store.Put(paddedKey(i), repeated("x", 30)); err != nil {
			t.Fatal(err)
		}
	}
	if len(store.SSTables) == 0 {
		t.Fatalf("expected flush to create sstable")
	}
}

func TestReadAfterForceFlush(t *testing.T) {
	store := openStore(t, 1024)
	for i := 0; i < 50; i++ {
		if err := store.Put("k"+leftPad(i), "v"+itoa(i)); err != nil {
			t.Fatal(err)
		}
	}
	if err := store.ForceFlush(); err != nil {
		t.Fatal(err)
	}

	value, found, err := store.Get("k025")
	if err != nil {
		t.Fatal(err)
	}
	if !found || value == nil || *value != "v25" {
		t.Fatalf("expected v25, got found=%v value=%v", found, value)
	}
}

func TestMemtableWinsOverSSTable(t *testing.T) {
	store := openStore(t, 1024)
	if err := store.Put("key", "old"); err != nil {
		t.Fatal(err)
	}
	if err := store.ForceFlush(); err != nil {
		t.Fatal(err)
	}
	if err := store.Put("key", "new"); err != nil {
		t.Fatal(err)
	}

	value, found, err := store.Get("key")
	if err != nil {
		t.Fatal(err)
	}
	if !found || value == nil || *value != "new" {
		t.Fatalf("expected new, got found=%v value=%v", found, value)
	}
}

func TestTombstoneAcrossLevels(t *testing.T) {
	store := openStore(t, 1024)
	if err := store.Put("key", "value"); err != nil {
		t.Fatal(err)
	}
	if err := store.ForceFlush(); err != nil {
		t.Fatal(err)
	}
	if err := store.Delete("key"); err != nil {
		t.Fatal(err)
	}

	value, found, err := store.Get("key")
	if err != nil {
		t.Fatal(err)
	}
	if !found || value != nil {
		t.Fatalf("expected tombstone, got found=%v value=%v", found, value)
	}
}

func TestPersistenceAfterReopen(t *testing.T) {
	tempDir := t.TempDir()
	store := lsmstore.New(tempDir, 1024)
	if err := store.Open(); err != nil {
		t.Fatal(err)
	}
	if err := store.Put("persist", "me"); err != nil {
		t.Fatal(err)
	}
	if err := store.Close(); err != nil {
		t.Fatal(err)
	}

	reopened := lsmstore.New(tempDir, 1024)
	if err := reopened.Open(); err != nil {
		t.Fatal(err)
	}

	value, found, err := reopened.Get("persist")
	if err != nil {
		t.Fatal(err)
	}
	if !found || value == nil || *value != "me" {
		t.Fatalf("expected persist=me, got found=%v value=%v", found, value)
	}
}

func openStore(t *testing.T, threshold int) *lsmstore.LSMStore {
	t.Helper()
	store := lsmstore.New(t.TempDir(), threshold)
	if err := store.Open(); err != nil {
		t.Fatalf("open store: %v", err)
	}
	return store
}

func paddedKey(index int) string {
	return "key-" + leftPad(index)
}

func leftPad(value int) string {
	switch {
	case value < 10:
		return "00" + itoa(value)
	case value < 100:
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

func repeated(ch string, count int) string {
	result := ""
	for i := 0; i < count; i++ {
		result += ch
	}
	return result
}
