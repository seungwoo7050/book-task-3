package tests

import (
	"testing"

	"study.local/go/ddia-distributed-systems/projects/03-shard-routing/internal/routing"
)

func TestEmptyAndSingleNodeRouting(t *testing.T) {
	ring := routing.NewRing(50)
	if _, ok := ring.NodeForKey("key"); ok {
		t.Fatalf("expected empty ring to reject key")
	}

	ring.AddNode("node-a")
	if nodeID, ok := ring.NodeForKey("key"); !ok || nodeID != "node-a" {
		t.Fatalf("expected single node route, got %q ok=%v", nodeID, ok)
	}
}

func TestDistributionAndRebalance(t *testing.T) {
	ring := routing.NewRing(150)
	ring.AddNode("node-a")
	ring.AddNode("node-b")
	ring.AddNode("node-c")

	keys := make([]string, 0, 3000)
	counts := map[string]int{}
	for i := 0; i < 3000; i++ {
		key := keyString(i)
		keys = append(keys, key)
		nodeID, _ := ring.NodeForKey(key)
		counts[nodeID]++
	}
	for _, nodeID := range []string{"node-a", "node-b", "node-c"} {
		share := float64(counts[nodeID]) / 3000
		if share <= 0.2 || share >= 0.5 {
			t.Fatalf("unexpected distribution for %s: %.2f", nodeID, share)
		}
	}

	movementKeys := keys[:1000]
	before := ring.Assignments(movementKeys)
	ring.AddNode("node-d")
	moved := ring.MovedKeys(movementKeys, before)
	if moved <= 50 || moved >= 500 {
		t.Fatalf("unexpected moved count on add: %d", moved)
	}

	ring.RemoveNode("node-b")
	for i := 0; i < 100; i++ {
		nodeID, _ := ring.NodeForKey(keyString(i))
		if nodeID == "node-b" {
			t.Fatalf("key routed to removed node")
		}
	}
}

func TestBatchRouting(t *testing.T) {
	ring := routing.NewRing(100)
	ring.AddNode("node-a")
	ring.AddNode("node-b")
	router := routing.NewRouter(ring)

	grouped := router.RouteBatch([]string{"k1", "k2", "k3", "k4", "k5"})
	total := 0
	for _, keys := range grouped {
		total += len(keys)
	}
	if total != 5 {
		t.Fatalf("expected 5 routed keys, got %d", total)
	}
}

func keyString(value int) string {
	return "key-" + itoa(value)
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
