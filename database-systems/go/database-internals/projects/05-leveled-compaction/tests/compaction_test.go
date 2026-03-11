package tests

import (
	"os"
	"path/filepath"
	"slices"
	"testing"

	"study.local/go/database-internals/projects/05-leveled-compaction/internal/compaction"
	"study.local/go/database-internals/projects/05-leveled-compaction/internal/sstable"
	"study.local/go/shared/serializer"
)

func TestKWayMergeKeepsNewerValue(t *testing.T) {
	merged := compaction.KWayMerge([][]serializer.Record{
		{{Key: "a", Value: serializer.StringPtr("new")}},
		{{Key: "a", Value: serializer.StringPtr("old")}},
	}, false)

	if len(merged) != 1 || *merged[0].Value != "new" {
		t.Fatalf("unexpected merge result: %+v", merged)
	}
}

func TestKWayMergeDropsTombstonesAtDeepestLevel(t *testing.T) {
	merged := compaction.KWayMerge([][]serializer.Record{
		{{Key: "gone", Value: nil}},
		{{Key: "gone", Value: serializer.StringPtr("alive")}},
	}, true)

	if len(merged) != 0 {
		t.Fatalf("expected tombstone to be dropped, got %+v", merged)
	}
}

func TestCompactL0ToL1(t *testing.T) {
	dataDir := t.TempDir()
	manager := compaction.New(dataDir, 4)

	datasets := [][]serializer.Record{
		{{Key: "a", Value: serializer.StringPtr("1")}, {Key: "b", Value: serializer.StringPtr("2")}},
		{{Key: "b", Value: serializer.StringPtr("2-new")}, {Key: "c", Value: serializer.StringPtr("3")}},
		{{Key: "a", Value: serializer.StringPtr("1-newer")}, {Key: "d", Value: serializer.StringPtr("4")}},
		{{Key: "c", Value: nil}, {Key: "e", Value: serializer.StringPtr("5")}},
	}

	for i, dataset := range datasets {
		fileName := filepath.Base(sstable.FileName(dataDir, i+1))
		table := sstable.New(filepath.Join(dataDir, fileName))
		if err := table.Write(dataset); err != nil {
			t.Fatalf("write sstable: %v", err)
		}
		manager.AddToLevel(0, fileName)
		manager.NextSequence = i + 2
	}

	result, err := manager.CompactL0ToL1()
	if err != nil {
		t.Fatalf("compact L0->L1: %v", err)
	}
	if !result.DroppedTombstones {
		t.Fatalf("expected deepest-level compaction to drop tombstones")
	}
	if len(result.Added) != 1 || len(result.Removed) != 4 {
		t.Fatalf("unexpected compaction result: %+v", result)
	}
	if len(manager.Levels[0]) != 0 || len(manager.Levels[1]) != 1 {
		t.Fatalf("unexpected levels after compaction: %+v", manager.Levels)
	}

	compacted := sstable.New(filepath.Join(dataDir, result.Added[0]))
	value, ok, err := compacted.Get("a")
	if err != nil || !ok || value == nil || *value != "1-newer" {
		t.Fatalf("unexpected a: ok=%v value=%v err=%v", ok, value, err)
	}
	value, ok, err = compacted.Get("b")
	if err != nil || !ok || value == nil || *value != "2-new" {
		t.Fatalf("unexpected b: ok=%v value=%v err=%v", ok, value, err)
	}
	if value, ok, err = compacted.Get("c"); err != nil || ok || value != nil {
		t.Fatalf("expected c tombstone to be removed, got ok=%v value=%v err=%v", ok, value, err)
	}

	for _, fileName := range result.Removed {
		if _, err := os.Stat(filepath.Join(dataDir, fileName)); !os.IsNotExist(err) {
			t.Fatalf("expected %s to be removed", fileName)
		}
	}
}

func TestManifestRoundTrip(t *testing.T) {
	dataDir := t.TempDir()
	manager := compaction.New(dataDir, 4)
	manager.Levels[0] = []string{"000001.sst", "000002.sst"}
	manager.Levels[1] = []string{"000010.sst"}
	manager.NextSequence = 11

	if err := manager.SaveManifest(); err != nil {
		t.Fatalf("save manifest: %v", err)
	}

	loaded := compaction.New(dataDir, 4)
	if err := loaded.LoadManifest(); err != nil {
		t.Fatalf("load manifest: %v", err)
	}

	if loaded.NextSequence != 11 {
		t.Fatalf("expected next sequence 11, got %d", loaded.NextSequence)
	}
	slices.Sort(loaded.Levels[0])
	if !slices.Equal(loaded.Levels[0], []string{"000001.sst", "000002.sst"}) {
		t.Fatalf("unexpected L0 manifest: %+v", loaded.Levels[0])
	}
	if !slices.Equal(loaded.Levels[1], []string{"000010.sst"}) {
		t.Fatalf("unexpected L1 manifest: %+v", loaded.Levels[1])
	}
}
