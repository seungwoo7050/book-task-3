# 20 핵심 상태 전이: overlap, version advance, responder selection

이 project가 좋은 이유는 quorum을 "분산 합의"처럼 크게 설명하지 않고, 버전 하나를 언제 올리고 언제 그대로 두는지로 압축해 보여 주기 때문이다. 실제로 중요한 invariant도 세 개뿐이다.

## Session 1 — write quorum failure는 version을 절대 올리지 않는다

`Write` 구현은 먼저 살아 있는 replica 수가 `W` 이상인지 확인하고, 부족하면 바로 실패한다.

```go
func (cluster *Cluster) Write(key string, value string) (WriteResult, error) {
	available := cluster.availableReplicas()
	if len(available) < cluster.policy.W {
		return WriteResult{}, fmt.Errorf("write quorum unavailable: need %d replicas, have %d", cluster.policy.W, len(available))
	}

	version := cluster.versions[key] + 1
	versioned := Value{Version: version, Data: value}
```

테스트 `TestWriteFailureDoesNotAdvanceVersion`가 바로 이 규칙을 묶어 둔다. write quorum이 깨졌을 때

- `LatestVersion("order") == 0`
- replica-1에도 값이 쓰이지 않음

이 두 조건이 같이 남아 있기 때문에, 이 구현에서는 partial write 후 rollback을 고민할 필요가 없다. 아예 advance 자체를 막아 버린다.

## Session 2 — 하지만 성공한 write는 정확히 `W`개가 아니라 "현재 살아 있는 replica 전부"에 퍼진다

교과서 설명과 코드가 조금 다른 지점은 여기다.

```go
	replicated := make([]string, 0, len(available))
	for _, replica := range available {
		replica.data[key] = versioned
		replicated = append(replicated, replica.ID)
	}
	cluster.versions[key] = version
```

즉 `W=2`라고 해서 두 replica만 고르는 게 아니다. quorum은 성공 조건일 뿐이고, 실제 fanout은 available replica 전체로 간다. 임시 검증에서도 첫 write 결과가 `replicated=[replica-1 replica-2 replica-3]`로 찍혔다.

이 차이를 문서에 남겨야 하는 이유는, 이 project의 핵심 질문이 overlap이긴 해도 구현 세부는 실제 Dynamo-style sloppy quorum과 다르기 때문이다. 여기서는 write target selection보다 "version advance를 해도 되는가"가 더 큰 질문이다.

## Session 3 — read는 fastest responder merge가 아니라 고정 순서 merge다

`Read`도 비슷하게 단순화돼 있다.

```go
	for _, replica := range available[:cluster.policy.R] {
		value, ok := replica.data[key]
		...
		if !result.Found || copyValue.Version > result.Value.Version {
			result.Value = copyValue
			result.Found = true
		}
	}
```

중요한 건 두 가지다.

- responder 집합은 `available[:R]`이므로 replica order에 의해 결정된다.
- merge 규칙은 "가장 높은 version 하나"이며 concurrent branch는 없다.

임시 검증에서도 `replica-1`을 내린 뒤 read responder가 `replica-2,replica-3`으로 고정됐다. 따라서 이 구현은 네트워크 지연이나 도착 순서가 아니라, "어떤 replica 집합이 겹치는가"를 deterministic하게 재현하는 데 최적화돼 있다.

이 단순화 덕분에 `TestReadReturnsLatestWhenQuorumsOverlap`과 `TestStaleReadAppearsWhenQuorumsDoNotOverlap`이 정확히 같은 틀 안에서 비교된다. 하나는 stale responder가 섞여 있어도 latest version이 이기고, 다른 하나는 stale responder만 보면 stale value가 그대로 선택된다.
