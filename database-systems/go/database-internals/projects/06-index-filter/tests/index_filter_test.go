package tests

import (
	"path/filepath"
	"testing"

	"study.local/go/database-internals/projects/06-index-filter/internal/bloomfilter"
	"study.local/go/database-internals/projects/06-index-filter/internal/sparseindex"
	"study.local/go/database-internals/projects/06-index-filter/internal/sstable"
	"study.local/go/shared/serializer"
)

func TestBloomFilterHasNoFalseNegatives(t *testing.T) {
	filter := bloomfilter.New(512, 0.01)
	keys := make([]string, 0, 512)
	for i := 0; i < 512; i++ {
		key := fmtKey(i)
		keys = append(keys, key)
		filter.Add(key)
	}
	for _, key := range keys {
		if !filter.MightContain(key) {
			t.Fatalf("false negative for %s", key)
		}
	}
}

func TestBloomFilterFalsePositiveRateIsBounded(t *testing.T) {
	filter := bloomfilter.New(1000, 0.01)
	for i := 0; i < 1000; i++ {
		filter.Add("present-" + fmtKey(i))
	}

	falsePositives := 0
	total := 5000
	for i := 0; i < total; i++ {
		if filter.MightContain("absent-" + fmtKey(i)) {
			falsePositives++
		}
	}
	rate := float64(falsePositives) / float64(total)
	if rate > 0.03 {
		t.Fatalf("false positive rate too high: %.4f", rate)
	}
}

func TestSparseIndexFindsExpectedBlock(t *testing.T) {
	index := sparseindex.New(8)
	entries := make([]sparseindex.Entry, 0, 32)
	for i := 0; i < 32; i++ {
		entries = append(entries, sparseindex.Entry{Key: fmtKey(i), Offset: int64(i * 20)})
	}
	index.Build(entries)

	block, ok := index.FindBlock(fmtKey(17), 640)
	if !ok {
		t.Fatalf("expected block to exist")
	}
	if block.Start != 320 || block.End != 480 {
		t.Fatalf("unexpected block %+v", block)
	}
}

func TestSSTableBloomRejectAndBoundedScan(t *testing.T) {
	tempDir := t.TempDir()
	table := sstable.New(filepath.Join(tempDir, "index.sst"), 8)
	records := make([]serializer.Record, 0, 64)
	for i := 0; i < 64; i++ {
		records = append(records, serializer.Record{
			Key:   fmtKey(i),
			Value: serializer.StringPtr("value-" + fmtKey(i)),
		})
	}
	if err := table.Write(records); err != nil {
		t.Fatalf("write table: %v", err)
	}

	value, ok, stats, err := table.GetWithStats("missing-key")
	if err != nil {
		t.Fatalf("lookup missing: %v", err)
	}
	if ok || value != nil || !stats.BloomRejected || stats.BytesRead != 0 {
		t.Fatalf("expected bloom reject, got ok=%v value=%v stats=%+v", ok, value, stats)
	}

	value, ok, stats, err = table.GetWithStats(fmtKey(23))
	if err != nil {
		t.Fatalf("lookup present: %v", err)
	}
	if !ok || value == nil || *value != "value-"+fmtKey(23) {
		t.Fatalf("unexpected lookup result: ok=%v value=%v", ok, value)
	}
	if stats.BytesRead <= 0 || stats.BytesRead >= table.DataSize {
		t.Fatalf("expected bounded scan, stats=%+v dataSize=%d", stats, table.DataSize)
	}
}

func fmtKey(value int) string {
	return string([]byte{
		'k',
		byte('0' + (value/100)%10),
		byte('0' + (value/10)%10),
		byte('0' + value%10),
	})
}
