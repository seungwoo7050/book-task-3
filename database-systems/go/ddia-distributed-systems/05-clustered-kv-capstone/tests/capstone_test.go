package tests

import (
	"testing"

	"study.local/ddia-distributed-systems/05-clustered-kv-capstone/internal/capstone"
)

func TestWriteRoutesToLeaderAndReplicates(t *testing.T) {
	cluster := newCluster(t)
	shardID, err := cluster.Put("alpha", "1")
	if err != nil {
		t.Fatal(err)
	}
	group := cluster.Group(shardID)

	if value, ok, _ := cluster.ReadFromNode(group.Leader, "alpha"); !ok || value != "1" {
		t.Fatalf("leader missing value")
	}
	if value, ok, _ := cluster.ReadFromNode(group.Followers[0], "alpha"); !ok || value != "1" {
		t.Fatalf("follower missing replicated value")
	}
}

func TestFollowerCatchUpAndDelete(t *testing.T) {
	cluster := newCluster(t)
	cluster.SetAutoReplicate(false)

	shardID, err := cluster.Put("beta", "2")
	if err != nil {
		t.Fatal(err)
	}
	group := cluster.Group(shardID)
	if _, ok, _ := cluster.ReadFromNode(group.Followers[0], "beta"); ok {
		t.Fatalf("expected follower to lag before catch-up")
	}

	applied, err := cluster.SyncFollower(shardID, group.Followers[0])
	if err != nil || applied != 1 {
		t.Fatalf("unexpected catch-up result applied=%d err=%v", applied, err)
	}
	if value, ok, _ := cluster.ReadFromNode(group.Followers[0], "beta"); !ok || value != "2" {
		t.Fatalf("expected follower catch-up value")
	}

	cluster.SetAutoReplicate(true)
	if _, err := cluster.Delete("beta"); err != nil {
		t.Fatal(err)
	}
	if _, ok, _ := cluster.ReadFromNode(group.Followers[0], "beta"); ok {
		t.Fatalf("expected delete to replicate")
	}
}

func TestRestartNodeLoadsFromDisk(t *testing.T) {
	cluster := newCluster(t)
	shardID, err := cluster.Put("gamma", "3")
	if err != nil {
		t.Fatal(err)
	}
	group := cluster.Group(shardID)
	follower := group.Followers[0]

	if err := cluster.RestartNode(follower); err != nil {
		t.Fatal(err)
	}
	if value, ok, err := cluster.ReadFromNode(follower, "gamma"); err != nil || !ok || value != "3" {
		t.Fatalf("expected restarted node to recover value, got value=%q ok=%v err=%v", value, ok, err)
	}
}

func newCluster(t *testing.T) *capstone.Cluster {
	t.Helper()
	cluster, err := capstone.NewCluster(t.TempDir(), []capstone.ReplicaGroup{
		{ShardID: "shard-a", Leader: "node-1", Followers: []string{"node-2"}},
		{ShardID: "shard-b", Leader: "node-2", Followers: []string{"node-3"}},
	}, 64)
	if err != nil {
		t.Fatal(err)
	}
	return cluster
}
