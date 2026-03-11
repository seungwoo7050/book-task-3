package tests

import (
	"testing"

	"study.local/go/ddia-distributed-systems/projects/02-leader-follower-replication/internal/replication"
)

func TestReplicationLogAssignsSequentialOffsets(t *testing.T) {
	log := &replication.ReplicationLog{}
	if offset := log.Append("put", "a", stringPtr("1")); offset != 0 {
		t.Fatalf("expected offset 0, got %d", offset)
	}
	if offset := log.Append("put", "b", stringPtr("2")); offset != 1 {
		t.Fatalf("expected offset 1, got %d", offset)
	}
}

func TestFollowerApplyIsIdempotent(t *testing.T) {
	follower := replication.NewFollower()
	entries := []replication.LogEntry{
		{Offset: 0, Operation: "put", Key: "x", Value: stringPtr("v1")},
		{Offset: 1, Operation: "put", Key: "x", Value: stringPtr("v2")},
	}
	if applied := follower.Apply(entries); applied != 2 {
		t.Fatalf("expected 2 applied, got %d", applied)
	}
	if applied := follower.Apply(entries); applied != 0 {
		t.Fatalf("expected replay to apply 0 entries, got %d", applied)
	}
	if value, ok := follower.Get("x"); !ok || value != "v2" {
		t.Fatalf("unexpected follower value %q", value)
	}
}

func TestReplicateOnceIncrementalAndDeletes(t *testing.T) {
	leader := replication.NewLeader()
	follower := replication.NewFollower()

	leader.Put("a", "1")
	if applied := replication.ReplicateOnce(leader, follower); applied != 1 {
		t.Fatalf("expected 1 applied, got %d", applied)
	}
	if follower.Watermark() != 0 {
		t.Fatalf("expected watermark 0, got %d", follower.Watermark())
	}

	leader.Put("b", "2")
	leader.Delete("a")
	if applied := replication.ReplicateOnce(leader, follower); applied != 2 {
		t.Fatalf("expected 2 applied, got %d", applied)
	}
	if _, ok := follower.Get("a"); ok {
		t.Fatalf("expected delete to replicate")
	}
	if value, ok := follower.Get("b"); !ok || value != "2" {
		t.Fatalf("unexpected b=%q", value)
	}
}

func stringPtr(value string) *string {
	copyValue := value
	return &copyValue
}
