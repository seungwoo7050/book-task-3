package quorum

import "fmt"

type Value struct {
	Version int
	Data    string
}

type Policy struct {
	N int
	W int
	R int
}

func (policy Policy) Validate(replicaCount int) error {
	if policy.N != replicaCount {
		return fmt.Errorf("policy: N=%d does not match replica count %d", policy.N, replicaCount)
	}
	if policy.N <= 0 || policy.W <= 0 || policy.R <= 0 {
		return fmt.Errorf("policy: N/W/R must be positive")
	}
	if policy.W > policy.N || policy.R > policy.N {
		return fmt.Errorf("policy: W/R cannot exceed N")
	}
	return nil
}

type Replica struct {
	ID   string
	up   bool
	data map[string]Value
}

func (replica *Replica) IsUp() bool {
	return replica.up
}

type Observation struct {
	ReplicaID string
	Value     *Value
}

type ReadResult struct {
	Value      Value
	Found      bool
	Responders []Observation
}

type WriteResult struct {
	Version    int
	Replicated []string
}

type Cluster struct {
	policy   Policy
	replicas map[string]*Replica
	order    []string
	versions map[string]int
}

func NewCluster(ids []string, policy Policy) (*Cluster, error) {
	cluster := &Cluster{
		policy:   policy,
		replicas: map[string]*Replica{},
		order:    append([]string(nil), ids...),
		versions: map[string]int{},
	}
	if err := policy.Validate(len(ids)); err != nil {
		return nil, err
	}
	for _, id := range ids {
		cluster.replicas[id] = &Replica{
			ID:   id,
			up:   true,
			data: map[string]Value{},
		}
	}
	return cluster, nil
}

func (cluster *Cluster) Policy() Policy {
	return cluster.policy
}

func (cluster *Cluster) DownReplica(id string) error {
	replica, err := cluster.replica(id)
	if err != nil {
		return err
	}
	replica.up = false
	return nil
}

func (cluster *Cluster) UpReplica(id string) error {
	replica, err := cluster.replica(id)
	if err != nil {
		return err
	}
	replica.up = true
	return nil
}

func (cluster *Cluster) Write(key string, value string) (WriteResult, error) {
	available := cluster.availableReplicas()
	if len(available) < cluster.policy.W {
		return WriteResult{}, fmt.Errorf("write quorum unavailable: need %d replicas, have %d", cluster.policy.W, len(available))
	}

	version := cluster.versions[key] + 1
	versioned := Value{Version: version, Data: value}
	replicated := make([]string, 0, len(available))
	for _, replica := range available {
		replica.data[key] = versioned
		replicated = append(replicated, replica.ID)
	}
	cluster.versions[key] = version
	return WriteResult{Version: version, Replicated: replicated}, nil
}

func (cluster *Cluster) Read(key string) (ReadResult, error) {
	available := cluster.availableReplicas()
	if len(available) < cluster.policy.R {
		return ReadResult{}, fmt.Errorf("read quorum unavailable: need %d replicas, have %d", cluster.policy.R, len(available))
	}

	result := ReadResult{
		Responders: make([]Observation, 0, cluster.policy.R),
	}
	for _, replica := range available[:cluster.policy.R] {
		value, ok := replica.data[key]
		if ok {
			copyValue := value
			result.Responders = append(result.Responders, Observation{
				ReplicaID: replica.ID,
				Value:     &copyValue,
			})
			if !result.Found || copyValue.Version > result.Value.Version {
				result.Value = copyValue
				result.Found = true
			}
			continue
		}
		result.Responders = append(result.Responders, Observation{ReplicaID: replica.ID})
	}
	return result, nil
}

func (cluster *Cluster) ReplicaValue(id string, key string) (Value, bool, error) {
	replica, err := cluster.replica(id)
	if err != nil {
		return Value{}, false, err
	}
	value, ok := replica.data[key]
	return value, ok, nil
}

func (cluster *Cluster) LatestVersion(key string) int {
	return cluster.versions[key]
}

func (cluster *Cluster) availableReplicas() []*Replica {
	available := make([]*Replica, 0, len(cluster.order))
	for _, id := range cluster.order {
		replica := cluster.replicas[id]
		if replica != nil && replica.up {
			available = append(available, replica)
		}
	}
	return available
}

func (cluster *Cluster) replica(id string) (*Replica, error) {
	replica := cluster.replicas[id]
	if replica == nil {
		return nil, fmt.Errorf("unknown replica %s", id)
	}
	return replica, nil
}
