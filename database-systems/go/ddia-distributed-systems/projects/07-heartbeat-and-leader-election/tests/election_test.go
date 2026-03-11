package tests

import (
	"testing"

	"study.local/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/internal/election"
)

func TestHealthyLeaderKeepsSendingHeartbeats(t *testing.T) {
	cluster := election.NewCluster([]string{"node-1", "node-2", "node-3"})
	leader := tickUntilLeader(t, cluster, 12)
	originalTerm := leader.Term

	for range 10 {
		cluster.Tick()
	}

	current := cluster.Leader()
	if current == nil || current.ID != leader.ID {
		t.Fatalf("expected leader %s to stay in charge, got %+v", leader.ID, current)
	}
	if current.Term != originalTerm {
		t.Fatalf("expected term %d to remain stable, got %d", originalTerm, current.Term)
	}
	if cluster.Node("node-2").Suspected || cluster.Node("node-3").Suspected {
		t.Fatalf("expected followers to stay healthy under heartbeats")
	}
}

func TestLeaderFailureTriggersSingleReelection(t *testing.T) {
	cluster := election.NewCluster([]string{"node-1", "node-2", "node-3"})
	leader := tickUntilLeader(t, cluster, 12)
	cluster.DownNode(leader.ID)

	next := tickUntilLeader(t, cluster, 12)
	if next.ID == leader.ID {
		t.Fatalf("expected a new leader after failover")
	}
	if next.Term <= leader.Term {
		t.Fatalf("expected term to increase after failover, old=%d new=%d", leader.Term, next.Term)
	}
}

func TestIsolatedNodeCannotPromoteItself(t *testing.T) {
	cluster := election.NewCluster([]string{"node-1", "node-2", "node-3"})
	cluster.DownNode("node-2")
	cluster.DownNode("node-3")

	for range 12 {
		cluster.Tick()
	}

	if cluster.Leader() != nil {
		t.Fatalf("expected no leader with only one node alive")
	}
	if node := cluster.Node("node-1"); node.State == election.Leader {
		t.Fatalf("isolated node must not become leader")
	}
}

func TestHigherTermHeartbeatForcesOldLeaderToStepDown(t *testing.T) {
	cluster := election.NewCluster([]string{"node-1", "node-2", "node-3"})
	leader := tickUntilLeader(t, cluster, 12)
	cluster.DownNode(leader.ID)
	newLeader := tickUntilLeader(t, cluster, 12)

	cluster.UpNode(leader.ID)
	for range 4 {
		cluster.Tick()
	}

	recovered := cluster.Node(leader.ID)
	if recovered.State != election.Follower {
		t.Fatalf("expected recovered old leader to step down, got %s", recovered.State)
	}
	if recovered.Term != newLeader.Term {
		t.Fatalf("expected recovered term %d, got %d", newLeader.Term, recovered.Term)
	}
}

func tickUntilLeader(t *testing.T, cluster *election.Cluster, maxTicks int) *election.Node {
	t.Helper()
	for range maxTicks {
		cluster.Tick()
		if leader := cluster.Leader(); leader != nil {
			return leader
		}
	}
	t.Fatalf("leader not elected within %d ticks", maxTicks)
	return nil
}
