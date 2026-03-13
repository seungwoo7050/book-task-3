package tests

import (
	"testing"

	"study.local/go/database-internals/projects/09-mvcc/internal/mvcc"
)

func TestBasicReadWrite(t *testing.T) {
	manager := mvcc.NewTransactionManager()
	t1 := manager.Begin()
	manager.Write(t1, "x", 10)
	if got := manager.Read(t1, "x"); got != 10 {
		t.Fatalf("expected read-your-own-write 10, got %v", got)
	}
	if err := manager.Commit(t1); err != nil {
		t.Fatal(err)
	}

	t2 := manager.Begin()
	if got := manager.Read(t2, "missing"); got != nil {
		t.Fatalf("expected nil for missing key, got %v", got)
	}
	if err := manager.Commit(t2); err != nil {
		t.Fatal(err)
	}
}

func TestSnapshotIsolation(t *testing.T) {
	manager := mvcc.NewTransactionManager()
	t1 := manager.Begin()
	manager.Write(t1, "x", 100)
	mustCommit(t, manager, t1)

	t2 := manager.Begin()
	t3 := manager.Begin()
	manager.Write(t3, "x", 200)
	mustCommit(t, manager, t3)

	if got := manager.Read(t2, "x"); got != 100 {
		t.Fatalf("expected snapshot to see 100, got %v", got)
	}
	mustCommit(t, manager, t2)
}

func TestLatestCommittedValue(t *testing.T) {
	manager := mvcc.NewTransactionManager()
	t1 := manager.Begin()
	manager.Write(t1, "a", "v1")
	mustCommit(t, manager, t1)

	t2 := manager.Begin()
	manager.Write(t2, "a", "v2")
	mustCommit(t, manager, t2)

	t3 := manager.Begin()
	if got := manager.Read(t3, "a"); got != "v2" {
		t.Fatalf("expected latest committed value v2, got %v", got)
	}
	mustCommit(t, manager, t3)
}

func TestWriteWriteConflict(t *testing.T) {
	manager := mvcc.NewTransactionManager()
	t1 := manager.Begin()
	t2 := manager.Begin()
	manager.Write(t1, "x", "alpha")
	manager.Write(t2, "x", "beta")
	mustCommit(t, manager, t1)
	if err := manager.Commit(t2); err == nil {
		t.Fatalf("expected conflict")
	}
}

func TestDifferentKeysNoConflict(t *testing.T) {
	manager := mvcc.NewTransactionManager()
	t1 := manager.Begin()
	t2 := manager.Begin()
	manager.Write(t1, "x", 1)
	manager.Write(t2, "y", 2)
	mustCommit(t, manager, t1)
	mustCommit(t, manager, t2)
}

func TestAbortAndDelete(t *testing.T) {
	manager := mvcc.NewTransactionManager()
	t1 := manager.Begin()
	manager.Write(t1, "x", "temp")
	manager.Abort(t1)

	t2 := manager.Begin()
	if got := manager.Read(t2, "x"); got != nil {
		t.Fatalf("expected aborted write to disappear, got %v", got)
	}
	mustCommit(t, manager, t2)

	t3 := manager.Begin()
	manager.Write(t3, "x", "hello")
	mustCommit(t, manager, t3)

	t4 := manager.Begin()
	manager.Delete(t4, "x")
	mustCommit(t, manager, t4)

	t5 := manager.Begin()
	if got := manager.Read(t5, "x"); got != nil {
		t.Fatalf("expected delete to hide key, got %v", got)
	}
	mustCommit(t, manager, t5)
}

func TestGC(t *testing.T) {
	manager := mvcc.NewTransactionManager()
	t1 := manager.Begin()
	manager.Write(t1, "x", "v1")
	mustCommit(t, manager, t1)

	t2 := manager.Begin()
	manager.Write(t2, "x", "v2")
	mustCommit(t, manager, t2)

	t3 := manager.Begin()
	manager.Write(t3, "x", "v3")
	mustCommit(t, manager, t3)

	manager.GC()

	t4 := manager.Begin()
	if got := manager.Read(t4, "x"); got != "v3" {
		t.Fatalf("expected latest value after GC, got %v", got)
	}
	mustCommit(t, manager, t4)

	if chain := manager.VersionStore.Store["x"]; len(chain) > 2 {
		t.Fatalf("expected GC to trim old versions, got %d", len(chain))
	}
}

func mustCommit(t *testing.T, manager *mvcc.TransactionManager, txID int) {
	t.Helper()
	if err := manager.Commit(txID); err != nil {
		t.Fatalf("commit failed: %v", err)
	}
}
