# 10 범위를 다시 좁히기: quorum 공식보다 작은 register 모델

이 프로젝트를 다시 읽을 때 먼저 정리해야 했던 건 "분산 저장소의 quorum" 전체를 구현한 게 아니라는 점이었다. 여기서는 Dynamo식 주변 기능을 일부러 걷어내고, `(version, data)` 두 값만 가진 register에 `N/W/R` 정책을 입혀 겹침 여부만 관찰한다.

## Session 1 — problem 문서가 고정하는 질문

[`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency/problem/README.md)가 고정하는 질문은 생각보다 좁다.

- replica는 3개다.
- write는 quorum이 확보될 때만 version을 올린다.
- read는 responder 집합 안에서 가장 높은 version을 고른다.
- `W + R > N`과 `W + R <= N`의 차이를 fixture로 재현한다.

반대로 문서가 빼는 것들도 명확하다.

- read repair
- hinted handoff
- anti-entropy
- vector clock
- sibling merge
- membership change

이렇게 먼저 쳐내고 나면, 이 project를 "Dynamo mini"로 읽기보다 "overlap 조건이 정말 stale read를 갈라내는가"를 보여 주는 최소 모델로 읽게 된다.

## Session 2 — 구현의 중심은 `Policy`와 `Cluster` 두 타입이다

핵심 구현 파일 [`internal/quorum/quorum.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency/internal/quorum/quorum.go)는 구조가 단순하다.

- `Policy { N, W, R }`
- `Value { Version, Data }`
- `Replica { up, data }`
- `Cluster { policy, replicas, order, versions }`

여기서 `order` 필드가 특히 중요했다. 처음에는 read quorum이 "현재 살아 있는 replica 중 아무 R개"일 거라고 예상했는데, 코드를 읽고 나니 실제로는 `availableReplicas()`가 `order` 순서대로 살아 있는 replica를 모으고, `Read`는 그중 앞의 `R`개만 본다. 즉 이 구현은 latency race나 random sample이 아니라 결정적 responder selection 모델에 가깝다.

## Session 3 — demo가 보여 주는 surface도 공식 설명에 맞춰 아주 얇다

demo entrypoint [`cmd/quorum-demo/main.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency/cmd/quorum-demo/main.go)는 두 시나리오만 남긴다.

```text
N=3 W=2 R=2 selected=v2:v2 responders=[replica-2=v2:v2, replica-3=v1:v1]
N=3 W=1 R=1 selected=v1:v1 responders=[replica-3=v1:v1]
```

첫 줄은 overlap이 있으면 stale responder가 섞여 있어도 최신 version을 고른다는 사실을, 둘째 줄은 overlap이 깨지면 stale read가 그대로 성공할 수 있다는 사실을 보여 준다. 이 정도로 surface가 얇기 때문에 다음 글에서는 오히려 구현의 세부 단순화가 더 중요해진다.
