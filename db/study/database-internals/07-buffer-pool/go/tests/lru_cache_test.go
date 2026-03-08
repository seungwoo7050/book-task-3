package tests

import (
	"reflect"
	"testing"

	"study.local/database-internals/07-buffer-pool/internal/lrucache"
)

func TestLRUBasicOperations(t *testing.T) {
	cache := lrucache.New(3)
	cache.Put("a", 1)
	if got := cache.Get("a"); got != 1 {
		t.Fatalf("expected 1, got %v", got)
	}
	if got := cache.Get("missing"); got != nil {
		t.Fatalf("expected missing key to return nil, got %v", got)
	}

	cache.Put("a", 2)
	if got := cache.Get("a"); got != 2 {
		t.Fatalf("expected updated value 2, got %v", got)
	}
	if cache.Size() != 1 {
		t.Fatalf("expected cache size 1, got %d", cache.Size())
	}
}

func TestLRUEvictionAndPromotion(t *testing.T) {
	cache := lrucache.New(3)
	cache.Put("a", 1)
	cache.Put("b", 2)
	cache.Put("c", 3)

	evicted := cache.Put("d", 4)
	if evicted == nil || evicted.Key != "a" {
		t.Fatalf("expected a to be evicted, got %+v", evicted)
	}

	cache.Get("b")
	evicted = cache.Put("e", 5)
	if evicted == nil || evicted.Key != "c" {
		t.Fatalf("expected c to be evicted after promoting b, got %+v", evicted)
	}
}

func TestLRUOrderingAndDelete(t *testing.T) {
	cache := lrucache.New(3)
	cache.Put("a", 1)
	cache.Put("b", 2)
	cache.Put("c", 3)

	if !reflect.DeepEqual(cache.Keys(), []string{"c", "b", "a"}) {
		t.Fatalf("unexpected order: %+v", cache.Keys())
	}
	cache.Get("a")
	if !reflect.DeepEqual(cache.Keys(), []string{"a", "c", "b"}) {
		t.Fatalf("unexpected order after promotion: %+v", cache.Keys())
	}
	if !cache.Delete("a") {
		t.Fatalf("expected delete to succeed")
	}
	if cache.Delete("missing") {
		t.Fatalf("expected delete miss to return false")
	}
}
