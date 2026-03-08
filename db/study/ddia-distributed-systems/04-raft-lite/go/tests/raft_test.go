package tests

import (
	"testing"

	"study.local/ddia-distributed-systems/04-raft-lite/internal/raft"
)

func electLeader(cluster *raft.Cluster, maxTicks int) *raft.Node {
	for i := 0; i < maxTicks; i++ {
		cluster.Tick()
		if leader := cluster.Leader(); leader != nil {
			return leader
		}
	}
	return nil
}

func TestLeaderElection(t *testing.T) {
	cluster := raft.NewCluster([]string{"n1", "n2", "n3"})
	leader := electLeader(cluster, 20)
	if leader == nil || leader.State != raft.Leader {
		t.Fatalf("expected leader election")
	}

	leaders := 0
	for _, node := range cluster.Nodes() {
		if node.State == raft.Leader {
			leaders++
		}
	}
	if leaders != 1 {
		t.Fatalf("expected exactly one leader, got %d", leaders)
	}
}

func TestLeaderFailover(t *testing.T) {
	cluster := raft.NewCluster([]string{"n1", "n2", "n3"})
	first := electLeader(cluster, 20)
	if first == nil {
		t.Fatalf("expected first leader")
	}
	cluster.DownNode(first.ID)
	second := electLeader(cluster, 40)
	if second == nil || second.ID == first.ID {
		t.Fatalf("expected new leader after failover")
	}
}

func TestLogReplicationAndCommit(t *testing.T) {
	cluster := raft.NewCluster([]string{"n1", "n2", "n3"})
	leader := electLeader(cluster, 20)
	if leader == nil {
		t.Fatalf("expected leader")
	}

	cluster.ClientRequest("SET x 1")
	cluster.ClientRequest("SET y 2")
	for i := 0; i < 20; i++ {
		cluster.Tick()
	}

	leader = cluster.Leader()
	if leader == nil || leader.CommitIdx < 1 {
		t.Fatalf("expected committed entries, leader=%v", leader)
	}
	for _, node := range cluster.Nodes() {
		if len(node.Log) < 2 {
			t.Fatalf("%s missing replicated entries", node.ID)
		}
		if node.Log[0].Command != "SET x 1" || node.Log[1].Command != "SET y 2" {
			t.Fatalf("%s has unexpected log %+v", node.ID, node.Log)
		}
	}
}

func TestHigherTermForcesStepDown(t *testing.T) {
	cluster := raft.NewCluster([]string{"n1", "n2", "n3"})
	leader := electLeader(cluster, 20)
	if leader == nil {
		t.Fatalf("expected leader")
	}

	originalTerm := leader.Term
	for _, node := range cluster.Nodes() {
		if node.State == raft.Follower {
			node.Term = originalTerm + 5
			break
		}
	}

	for i := 0; i < 20; i++ {
		cluster.Tick()
	}
	newLeader := electLeader(cluster, 20)
	if newLeader == nil || newLeader.Term <= originalTerm {
		t.Fatalf("expected higher-term leader after step down")
	}
}
