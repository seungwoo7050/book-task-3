package tests

import (
	"testing"

	"study.local/go/ddia-distributed-systems/projects/06-quorum-and-consistency/internal/quorum"
)

func TestReadReturnsLatestWhenQuorumsOverlap(t *testing.T) {
	cluster := newCluster(t, quorum.Policy{N: 3, W: 2, R: 2})
	if _, err := cluster.Write("order", "v1"); err != nil {
		t.Fatal(err)
	}
	if err := cluster.DownReplica("replica-3"); err != nil {
		t.Fatal(err)
	}
	if _, err := cluster.Write("order", "v2"); err != nil {
		t.Fatal(err)
	}
	if err := cluster.UpReplica("replica-3"); err != nil {
		t.Fatal(err)
	}
	if err := cluster.DownReplica("replica-1"); err != nil {
		t.Fatal(err)
	}

	result, err := cluster.Read("order")
	if err != nil {
		t.Fatal(err)
	}
	if !result.Found || result.Value.Version != 2 || result.Value.Data != "v2" {
		t.Fatalf("expected latest value v2/version 2, got found=%v value=%+v", result.Found, result.Value)
	}
	if len(result.Responders) != 2 || result.Responders[0].ReplicaID != "replica-2" || result.Responders[1].ReplicaID != "replica-3" {
		t.Fatalf("unexpected responders: %+v", result.Responders)
	}
	if result.Responders[1].Value == nil || result.Responders[1].Value.Version != 1 {
		t.Fatalf("expected stale responder replica-3 to hold version 1, got %+v", result.Responders[1].Value)
	}
}

func TestStaleReadAppearsWhenQuorumsDoNotOverlap(t *testing.T) {
	cluster := newCluster(t, quorum.Policy{N: 3, W: 1, R: 1})
	if _, err := cluster.Write("order", "v1"); err != nil {
		t.Fatal(err)
	}
	if err := cluster.DownReplica("replica-2"); err != nil {
		t.Fatal(err)
	}
	if err := cluster.DownReplica("replica-3"); err != nil {
		t.Fatal(err)
	}
	if _, err := cluster.Write("order", "v2"); err != nil {
		t.Fatal(err)
	}
	if err := cluster.UpReplica("replica-3"); err != nil {
		t.Fatal(err)
	}
	if err := cluster.DownReplica("replica-1"); err != nil {
		t.Fatal(err)
	}

	result, err := cluster.Read("order")
	if err != nil {
		t.Fatal(err)
	}
	if !result.Found || result.Value.Version != 1 || result.Value.Data != "v1" {
		t.Fatalf("expected stale value v1/version 1, got found=%v value=%+v", result.Found, result.Value)
	}
	if len(result.Responders) != 1 || result.Responders[0].ReplicaID != "replica-3" {
		t.Fatalf("unexpected responders: %+v", result.Responders)
	}
}

func TestWriteFailureDoesNotAdvanceVersion(t *testing.T) {
	cluster := newCluster(t, quorum.Policy{N: 3, W: 2, R: 1})
	if err := cluster.DownReplica("replica-2"); err != nil {
		t.Fatal(err)
	}
	if err := cluster.DownReplica("replica-3"); err != nil {
		t.Fatal(err)
	}

	if _, err := cluster.Write("order", "v1"); err == nil {
		t.Fatalf("expected write quorum failure")
	}
	if version := cluster.LatestVersion("order"); version != 0 {
		t.Fatalf("expected version to stay 0, got %d", version)
	}
	if _, ok, err := cluster.ReplicaValue("replica-1", "order"); err != nil || ok {
		t.Fatalf("expected replica-1 to remain empty, ok=%v err=%v", ok, err)
	}
}

func TestReplicaFailuresReduceAvailability(t *testing.T) {
	cluster := newCluster(t, quorum.Policy{N: 3, W: 2, R: 2})
	if _, err := cluster.Write("order", "v1"); err != nil {
		t.Fatal(err)
	}
	if err := cluster.DownReplica("replica-2"); err != nil {
		t.Fatal(err)
	}
	if err := cluster.DownReplica("replica-3"); err != nil {
		t.Fatal(err)
	}

	if _, err := cluster.Read("order"); err == nil {
		t.Fatalf("expected read quorum failure")
	}
	if _, err := cluster.Write("order", "v2"); err == nil {
		t.Fatalf("expected write quorum failure")
	}
}

func newCluster(t *testing.T, policy quorum.Policy) *quorum.Cluster {
	t.Helper()
	cluster, err := quorum.NewCluster([]string{"replica-1", "replica-2", "replica-3"}, policy)
	if err != nil {
		t.Fatal(err)
	}
	return cluster
}
