package main

import (
	"fmt"

	"study.local/go/ddia-distributed-systems/projects/04-raft-lite/internal/raft"
)

func main() {
	cluster := raft.NewCluster([]string{"n1", "n2", "n3"})
	leader := waitLeader(cluster)
	cluster.ClientRequest("SET alpha 1")
	for i := 0; i < 10; i++ {
		cluster.Tick()
	}
	fmt.Printf("leader=%s commit=%d log_len=%d\n", leader.ID, leader.CommitIdx, len(leader.Log))
}

func waitLeader(cluster *raft.Cluster) *raft.Node {
	for i := 0; i < 20; i++ {
		cluster.Tick()
		if leader := cluster.Leader(); leader != nil {
			return leader
		}
	}
	panic("no leader elected")
}
