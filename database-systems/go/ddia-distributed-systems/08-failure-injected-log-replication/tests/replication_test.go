package tests

import (
	"testing"

	"study.local/ddia-distributed-systems/08-failure-injected-log-replication/internal/replication"
)

func TestDroppedAppendRetriesUntilFollowerConverges(t *testing.T) {
	cluster := replication.NewCluster("leader-1", []string{"node-2", "node-3"})
	cluster.DropNext(replication.MessageAppend, "node-2", 0, 1)

	cluster.Put("alpha", "1")
	cluster.Tick()

	if cluster.Leader.CommitIndex() != 0 {
		t.Fatalf("expected quorum commit after node-3 ack, got %d", cluster.Leader.CommitIndex())
	}
	node2 := follower(t, cluster, "node-2")
	if node2.Watermark() != -1 {
		t.Fatalf("expected node-2 to miss first append, got watermark %d", node2.Watermark())
	}

	cluster.Tick()

	if node2.Watermark() != 0 {
		t.Fatalf("expected retry to converge node-2, got watermark %d", node2.Watermark())
	}
	if value, ok := node2.Read("alpha"); !ok || value != "1" {
		t.Fatalf("expected converged follower value alpha=1, got ok=%v value=%q", ok, value)
	}
}

func TestDuplicateAppendIsIdempotent(t *testing.T) {
	cluster := replication.NewCluster("leader-1", []string{"node-2", "node-3"})
	cluster.DuplicateNext(replication.MessageAppend, "node-2", 0, 1)

	cluster.Put("alpha", "1")
	cluster.Tick()

	node2 := follower(t, cluster, "node-2")
	if node2.LogLength() != 1 {
		t.Fatalf("expected duplicate append to keep log length 1, got %d", node2.LogLength())
	}
	if node2.AppliedCount() != 1 {
		t.Fatalf("expected duplicate append to apply once, got %d", node2.AppliedCount())
	}
}

func TestPausedFollowerLagsButRecoversAfterResume(t *testing.T) {
	cluster := replication.NewCluster("leader-1", []string{"node-2", "node-3"})
	cluster.PauseNode("node-2")

	cluster.Put("alpha", "1")
	cluster.Tick()
	cluster.Put("beta", "2")
	cluster.Tick()

	node2 := follower(t, cluster, "node-2")
	if cluster.Leader.CommitIndex() != 1 {
		t.Fatalf("expected quorum commit to advance to 1, got %d", cluster.Leader.CommitIndex())
	}
	if node2.Watermark() != -1 {
		t.Fatalf("expected paused follower to lag completely, got %d", node2.Watermark())
	}

	cluster.ResumeNode("node-2")
	cluster.Tick()
	cluster.Tick()

	if node2.Watermark() != 1 {
		t.Fatalf("expected resumed follower to catch up to index 1, got %d", node2.Watermark())
	}
	if value, ok := node2.Read("beta"); !ok || value != "2" {
		t.Fatalf("expected resumed follower to converge beta=2, got ok=%v value=%q", ok, value)
	}
}

func follower(t *testing.T, cluster *replication.Cluster, id string) *replication.Follower {
	t.Helper()
	follower, err := cluster.Follower(id)
	if err != nil {
		t.Fatal(err)
	}
	return follower
}
