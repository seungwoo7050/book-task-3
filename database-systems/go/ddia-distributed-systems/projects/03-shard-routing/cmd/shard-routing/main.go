package main

import (
	"fmt"

	"study.local/go/ddia-distributed-systems/projects/03-shard-routing/internal/routing"
)

func main() {
	ring := routing.NewRing(64)
	ring.AddNode("node-a")
	ring.AddNode("node-b")
	ring.AddNode("node-c")

	router := routing.NewRouter(ring)
	for _, key := range []string{"alpha", "beta", "gamma"} {
		nodeID, _ := router.Route(key)
		fmt.Printf("%s -> %s\n", key, nodeID)
	}
}
