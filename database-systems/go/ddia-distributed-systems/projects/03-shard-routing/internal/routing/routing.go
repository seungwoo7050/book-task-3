package routing

import (
	"slices"

	"study.local/go/shared/hash"
)

type ringEntry struct {
	Hash   uint32
	NodeID string
}

type Ring struct {
	VirtualNodes int
	ring         []ringEntry
	nodes        map[string]struct{}
}

func NewRing(virtualNodes int) *Ring {
	if virtualNodes <= 0 {
		virtualNodes = 150
	}
	return &Ring{
		VirtualNodes: virtualNodes,
		nodes:        map[string]struct{}{},
	}
}

func (ring *Ring) AddNode(nodeID string) {
	if _, exists := ring.nodes[nodeID]; exists {
		return
	}
	ring.nodes[nodeID] = struct{}{}
	for i := 0; i < ring.VirtualNodes; i++ {
		entry := ringEntry{
			Hash:   hash.MurmurHash3([]byte(nodeID+"#v"+itoa(i)), 0),
			NodeID: nodeID,
		}
		index := slices.IndexFunc(ring.ring, func(candidate ringEntry) bool {
			return candidate.Hash >= entry.Hash
		})
		if index == -1 {
			ring.ring = append(ring.ring, entry)
		} else {
			ring.ring = append(ring.ring[:index], append([]ringEntry{entry}, ring.ring[index:]...)...)
		}
	}
}

func (ring *Ring) RemoveNode(nodeID string) {
	delete(ring.nodes, nodeID)
	filtered := make([]ringEntry, 0, len(ring.ring))
	for _, entry := range ring.ring {
		if entry.NodeID != nodeID {
			filtered = append(filtered, entry)
		}
	}
	ring.ring = filtered
}

func (ring *Ring) Nodes() []string {
	nodes := make([]string, 0, len(ring.nodes))
	for nodeID := range ring.nodes {
		nodes = append(nodes, nodeID)
	}
	slices.Sort(nodes)
	return nodes
}

func (ring *Ring) NodeForKey(key string) (string, bool) {
	if len(ring.ring) == 0 {
		return "", false
	}
	target := hash.MurmurHash3([]byte(key), 0)
	index := slices.IndexFunc(ring.ring, func(entry ringEntry) bool {
		return entry.Hash >= target
	})
	if index == -1 {
		index = 0
	}
	return ring.ring[index].NodeID, true
}

func (ring *Ring) Assignments(keys []string) map[string]string {
	assignments := make(map[string]string, len(keys))
	for _, key := range keys {
		nodeID, ok := ring.NodeForKey(key)
		if ok {
			assignments[key] = nodeID
		}
	}
	return assignments
}

func (ring *Ring) MovedKeys(keys []string, previous map[string]string) int {
	current := ring.Assignments(keys)
	moved := 0
	for _, key := range keys {
		if previous[key] != "" && previous[key] != current[key] {
			moved++
		}
	}
	return moved
}

type Router struct {
	Ring *Ring
}

func NewRouter(ring *Ring) *Router {
	return &Router{Ring: ring}
}

func (router *Router) Route(key string) (string, bool) {
	return router.Ring.NodeForKey(key)
}

func (router *Router) RouteBatch(keys []string) map[string][]string {
	grouped := map[string][]string{}
	for _, key := range keys {
		nodeID, ok := router.Ring.NodeForKey(key)
		if !ok {
			continue
		}
		grouped[nodeID] = append(grouped[nodeID], key)
	}
	return grouped
}

func itoa(value int) string {
	if value == 0 {
		return "0"
	}
	buffer := make([]byte, 0, 4)
	for value > 0 {
		buffer = append([]byte{byte('0' + value%10)}, buffer...)
		value /= 10
	}
	return string(buffer)
}
