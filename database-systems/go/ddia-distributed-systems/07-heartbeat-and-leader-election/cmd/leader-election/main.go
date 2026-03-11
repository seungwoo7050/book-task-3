package main

import (
	"fmt"

	"study.local/ddia-distributed-systems/07-heartbeat-and-leader-election/internal/election"
)

func main() {
	cluster := election.NewCluster([]string{"node-1", "node-2", "node-3"})
	tick := 0

	for tick < 12 {
		tick++
		cluster.Tick()
		if leader := cluster.Leader(); leader != nil {
			fmt.Printf("tick=%d leader=%s term=%d suspected=[]\n", tick, leader.ID, leader.Term)
			break
		}
	}

	downed := cluster.Leader()
	cluster.DownNode(downed.ID)
	fmt.Printf("leader-down id=%s\n", downed.ID)

	for tick < 24 {
		tick++
		cluster.Tick()
		node2 := cluster.Node("node-2")
		if node2 != nil && node2.Suspected {
			fmt.Printf("tick=%d suspected=[%s]\n", tick, node2.ID)
			break
		}
	}

	for tick < 36 {
		tick++
		cluster.Tick()
		if leader := cluster.Leader(); leader != nil {
			fmt.Printf("tick=%d reelected=%s term=%d\n", tick, leader.ID, leader.Term)
			break
		}
	}

	cluster.UpNode(downed.ID)
	for range 4 {
		cluster.Tick()
	}
	recovered := cluster.Node(downed.ID)
	fmt.Printf("recovered=%s state=%s term=%d\n", recovered.ID, recovered.State, recovered.Term)
}
