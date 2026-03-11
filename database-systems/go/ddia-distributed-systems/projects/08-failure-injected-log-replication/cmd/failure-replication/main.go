package main

import (
	"fmt"

	"study.local/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/internal/replication"
)

func main() {
	cluster := replication.NewCluster("leader-1", []string{"node-2", "node-3"})

	cluster.DropNext(replication.MessageAppend, "node-2", 0, 1)
	cluster.Put("alpha", "1")
	cluster.Tick()
	node2 := mustFollower(cluster, "node-2")
	node3 := mustFollower(cluster, "node-3")
	fmt.Printf("drop tick commit=%d node-2=%d node-3=%d\n", cluster.Leader.CommitIndex(), node2.Watermark(), node3.Watermark())

	cluster.Tick()
	fmt.Printf("retry tick commit=%d node-2=%d node-3=%d\n", cluster.Leader.CommitIndex(), node2.Watermark(), node3.Watermark())

	cluster.DuplicateNext(replication.MessageAppend, "node-3", 1, 1)
	cluster.Put("beta", "2")
	cluster.Tick()
	fmt.Printf("duplicate tick commit=%d node-3-log=%d node-3-applied=%d\n", cluster.Leader.CommitIndex(), node3.LogLength(), node3.AppliedCount())

	cluster.PauseNode("node-2")
	cluster.Put("gamma", "3")
	cluster.Tick()
	fmt.Printf("pause tick commit=%d node-2=%d node-3=%d\n", cluster.Leader.CommitIndex(), node2.Watermark(), node3.Watermark())

	cluster.ResumeNode("node-2")
	cluster.Tick()
	fmt.Printf("recover tick commit=%d node-2=%d node-3=%d\n", cluster.Leader.CommitIndex(), node2.Watermark(), node3.Watermark())
}

func mustFollower(cluster *replication.Cluster, id string) *replication.Follower {
	follower, err := cluster.Follower(id)
	if err != nil {
		panic(err)
	}
	return follower
}
