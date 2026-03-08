package main

import (
	"fmt"

	"study.local/ddia-distributed-systems/02-leader-follower-replication/internal/replication"
)

func main() {
	leader := replication.NewLeader()
	follower := replication.NewFollower()

	leader.Put("alpha", "1")
	leader.Put("beta", "2")
	replication.ReplicateOnce(leader, follower)

	leader.Delete("alpha")
	replication.ReplicateOnce(leader, follower)

	if _, ok := follower.Get("alpha"); !ok {
		fmt.Println("alpha deleted")
	}
	if value, ok := follower.Get("beta"); ok {
		fmt.Printf("beta=%s watermark=%d\n", value, follower.Watermark())
	}
}
