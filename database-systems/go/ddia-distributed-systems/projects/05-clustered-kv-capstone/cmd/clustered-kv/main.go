package main

import (
	"fmt"
	"path/filepath"

	"study.local/go/ddia-distributed-systems/projects/05-clustered-kv-capstone/internal/capstone"
)

func main() {
	cluster, err := capstone.NewCluster(filepath.Join(".", ".demo-data"), []capstone.ReplicaGroup{
		{ShardID: "shard-a", Leader: "node-1", Followers: []string{"node-2"}},
		{ShardID: "shard-b", Leader: "node-2", Followers: []string{"node-3"}},
	}, 64)
	if err != nil {
		panic(err)
	}

	shardID, err := cluster.Put("alpha", "1")
	if err != nil {
		panic(err)
	}
	group := cluster.Group(shardID)
	value, ok, _ := cluster.ReadFromNode(group.Followers[0], "alpha")
	fmt.Printf("key=alpha shard=%s follower=%s value=%s ok=%v\n", shardID, group.Followers[0], value, ok)
}
