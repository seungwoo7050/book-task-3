package main

import (
	"fmt"
	"strings"

	"study.local/go/ddia-distributed-systems/projects/06-quorum-and-consistency/internal/quorum"
)

func main() {
	safe := mustCluster(quorum.Policy{N: 3, W: 2, R: 2})
	mustWrite(safe, "alpha", "v1")
	must(safe.DownReplica("replica-3"))
	mustWrite(safe, "alpha", "v2")
	must(safe.UpReplica("replica-3"))
	must(safe.DownReplica("replica-1"))
	safeRead, err := safe.Read("alpha")
	must(err)

	stale := mustCluster(quorum.Policy{N: 3, W: 1, R: 1})
	mustWrite(stale, "alpha", "v1")
	must(stale.DownReplica("replica-2"))
	must(stale.DownReplica("replica-3"))
	mustWrite(stale, "alpha", "v2")
	must(stale.UpReplica("replica-3"))
	must(stale.DownReplica("replica-1"))
	staleRead, err := stale.Read("alpha")
	must(err)

	fmt.Printf("N=3 W=2 R=2 selected=%s responders=[%s]\n", formatValue(safeRead), formatResponders(safeRead))
	fmt.Printf("N=3 W=1 R=1 selected=%s responders=[%s]\n", formatValue(staleRead), formatResponders(staleRead))
}

func mustCluster(policy quorum.Policy) *quorum.Cluster {
	cluster, err := quorum.NewCluster([]string{"replica-1", "replica-2", "replica-3"}, policy)
	must(err)
	return cluster
}

func mustWrite(cluster *quorum.Cluster, key string, value string) {
	_, err := cluster.Write(key, value)
	must(err)
}

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func formatValue(result quorum.ReadResult) string {
	if !result.Found {
		return "missing"
	}
	return fmt.Sprintf("v%d:%s", result.Value.Version, result.Value.Data)
}

func formatResponders(result quorum.ReadResult) string {
	parts := make([]string, 0, len(result.Responders))
	for _, responder := range result.Responders {
		if responder.Value == nil {
			parts = append(parts, responder.ReplicaID+"=missing")
			continue
		}
		parts = append(parts, fmt.Sprintf("%s=v%d:%s", responder.ReplicaID, responder.Value.Version, responder.Value.Data))
	}
	return strings.Join(parts, ", ")
}
