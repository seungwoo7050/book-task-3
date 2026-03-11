package tests

import (
	"os"
	"path/filepath"
	"testing"

	"study.local/go/database-internals/projects/04-wal-recovery/internal/store"
	"study.local/go/database-internals/projects/04-wal-recovery/internal/wal"
)

func TestRecoverPutRecords(t *testing.T) {
	walPath := filepath.Join(t.TempDir(), "test.wal")
	log := wal.New(walPath, false)
	mustNoErr(t, log.Open())
	mustNoErr(t, log.AppendPut("name", "Alice"))
	mustNoErr(t, log.AppendPut("age", "30"))
	mustNoErr(t, log.Close())

	records, err := wal.New(walPath, false).Recover()
	mustNoErr(t, err)
	if len(records) != 2 || records[0].Type != "put" || records[0].Key != "name" || *records[0].Value != "Alice" {
		t.Fatalf("unexpected records: %+v", records)
	}
}

func TestRecoverDeleteRecords(t *testing.T) {
	walPath := filepath.Join(t.TempDir(), "test.wal")
	log := wal.New(walPath, false)
	mustNoErr(t, log.Open())
	mustNoErr(t, log.AppendPut("x", "val"))
	mustNoErr(t, log.AppendDelete("x"))
	mustNoErr(t, log.Close())

	records, err := wal.New(walPath, false).Recover()
	mustNoErr(t, err)
	if len(records) != 2 || records[1].Type != "delete" || records[1].Key != "x" {
		t.Fatalf("unexpected records: %+v", records)
	}
}

func TestRecoverManyRecords(t *testing.T) {
	walPath := filepath.Join(t.TempDir(), "test.wal")
	log := wal.New(walPath, false)
	mustNoErr(t, log.Open())
	for i := 0; i < 500; i++ {
		mustNoErr(t, log.AppendPut("key:"+itoa(i), "value:"+itoa(i)))
	}
	mustNoErr(t, log.Close())

	records, err := wal.New(walPath, false).Recover()
	mustNoErr(t, err)
	if len(records) != 500 || records[0].Key != "key:0" || records[499].Key != "key:499" {
		t.Fatalf("unexpected record set length=%d", len(records))
	}
}

func TestStopAtCorruptedRecord(t *testing.T) {
	walPath := filepath.Join(t.TempDir(), "test.wal")
	log := wal.New(walPath, false)
	mustNoErr(t, log.Open())
	mustNoErr(t, log.AppendPut("good1", "val1"))
	mustNoErr(t, log.AppendPut("good2", "val2"))
	mustNoErr(t, log.Close())

	file, err := os.OpenFile(walPath, os.O_APPEND|os.O_WRONLY, 0o644)
	mustNoErr(t, err)
	_, err = file.Write([]byte{0xDE, 0xAD, 0xBE, 0xEF, 0x01, 0x00})
	mustNoErr(t, err)
	mustNoErr(t, file.Close())

	records, err := wal.New(walPath, false).Recover()
	mustNoErr(t, err)
	if len(records) != 2 {
		t.Fatalf("expected only 2 valid records, got %d", len(records))
	}
}

func TestRecoverNonexistentAndTruncated(t *testing.T) {
	records, err := wal.New(filepath.Join(t.TempDir(), "missing.wal"), false).Recover()
	mustNoErr(t, err)
	if len(records) != 0 {
		t.Fatalf("expected empty recovery on missing wal")
	}

	walPath := filepath.Join(t.TempDir(), "truncated.wal")
	mustNoErr(t, os.WriteFile(walPath, []byte{0, 0, 0, 0, 1}, 0o644))
	records, err = wal.New(walPath, false).Recover()
	mustNoErr(t, err)
	if len(records) != 0 {
		t.Fatalf("expected truncated wal to recover 0 records")
	}
}

func TestStoreRecoversFromWALAfterReopen(t *testing.T) {
	tempDir := t.TempDir()
	store1 := store.New(tempDir, 4096, false)
	mustNoErr(t, store1.Open())
	mustNoErr(t, store1.Put("persist", "me"))
	mustNoErr(t, store1.Close())

	store2 := store.New(tempDir, 4096, false)
	mustNoErr(t, store2.Open())
	value, found, err := store2.Get("persist")
	mustNoErr(t, err)
	if !found || value == nil || *value != "me" {
		t.Fatalf("expected recovered value, got found=%v value=%v", found, value)
	}
}

func TestForceFlushRotatesWAL(t *testing.T) {
	tempDir := t.TempDir()
	durable := store.New(tempDir, 4096, false)
	mustNoErr(t, durable.Open())
	mustNoErr(t, durable.Put("alpha", "1"))
	mustNoErr(t, durable.ForceFlush())

	info, err := os.Stat(filepath.Join(tempDir, "active.wal"))
	mustNoErr(t, err)
	if info.Size() != 0 {
		t.Fatalf("expected fresh empty wal after rotation, got %d bytes", info.Size())
	}

	reopened := store.New(tempDir, 4096, false)
	mustNoErr(t, reopened.Open())
	value, found, err := reopened.Get("alpha")
	mustNoErr(t, err)
	if !found || value == nil || *value != "1" {
		t.Fatalf("expected value from sstable after reopen, got found=%v value=%v", found, value)
	}
}

func mustNoErr(t *testing.T, err error) {
	t.Helper()
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
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
