package tests

import (
	"reflect"
	"testing"

	"study.local/go/database-internals/projects/08-btree-index-and-query-scan/internal/btreeindex"
)

func TestSplitAndLookup(t *testing.T) {
	index := btreeindex.New(3)
	keys := []string{"ada", "ben", "cora", "dina", "erin", "finn", "gwen"}

	for rowID, key := range keys {
		index.Insert(key, rowID+1)
	}
	index.Insert("dina", 99)

	if index.Height() < 2 {
		t.Fatalf("expected split to grow the tree height, got %d", index.Height())
	}
	if got := index.Lookup("dina"); !reflect.DeepEqual(got, []int{4, 99}) {
		t.Fatalf("expected duplicate row ids for dina, got %v", got)
	}
	if got := index.Lookup("missing"); got != nil {
		t.Fatalf("expected missing lookup to be nil, got %v", got)
	}
}

func TestRangeCursorReturnsOrderedKeys(t *testing.T) {
	index := btreeindex.New(3)
	for rowID, key := range []string{"ada", "ben", "cora", "dina", "erin", "finn"} {
		index.Insert(key, rowID+1)
	}

	cursor := index.OpenRange("ben", "erin")
	keys := []string{}
	for {
		entry, ok := cursor.Next()
		if !ok {
			break
		}
		keys = append(keys, entry.Key)
	}

	expected := []string{"ben", "cora", "dina", "erin"}
	if !reflect.DeepEqual(keys, expected) {
		t.Fatalf("expected ordered keys %v, got %v", expected, keys)
	}
}
