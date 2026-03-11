# 06-quorum-and-consistency 개발 타임라인

## 1. 프로젝트 골격 만들기

```bash
mkdir -p go/ddia-distributed-systems/projects/06-quorum-and-consistency/{cmd/quorum-demo,docs/concepts,docs/references,internal/quorum,notion,notion-archive,problem,tests}
cd go/ddia-distributed-systems/projects/06-quorum-and-consistency
go mod init study.local/go/ddia-distributed-systems/projects/06-quorum-and-consistency
```

## 2. 최소 모델 먼저 고정

처음부터 분산 KV를 만들지 않고 다음 타입만 고정했다.

- `Policy { N, W, R }`
- `Replica`
- `Value { Version, Data }`
- `Cluster`
- `ReadResult`, `WriteResult`

핵심 결정은 “single-key register로 줄인다”와 “responder 선택은 결정적으로 고정한다”였다.

## 3. stale read 시나리오 설계

두 가지 대표 시나리오를 먼저 만들었다.

### overlap 있는 경우

- `N=3, W=2, R=2`
- 최신 write를 본 replica와 stale replica가 함께 응답
- read merge는 최신 version 선택

### overlap 없는 경우

- `N=3, W=1, R=1`
- 최신 write를 보지 못한 stale replica만 응답
- stale read 재현

이 두 시나리오가 있어야 데모와 테스트가 같은 메시지를 전달한다.

## 4. 테스트 추가

| 테스트명 | 검증 대상 |
| --- | --- |
| `TestReadReturnsLatestWhenQuorumsOverlap` | `W + R > N`일 때 최신 read |
| `TestStaleReadAppearsWhenQuorumsDoNotOverlap` | `W + R <= N`일 때 stale read |
| `TestWriteFailureDoesNotAdvanceVersion` | quorum 없는 write 실패 시 version 동결 |
| `TestReplicaFailuresReduceAvailability` | replica down 시 read/write quorum 실패 |

## 5. 데모 출력 설계

`go run ./cmd/quorum-demo`는 아래 두 줄만 보여 준다.

```text
N=3 W=2 R=2 selected=v2:v2 responders=[replica-2=v2:v2, replica-3=v1:v1]
N=3 W=1 R=1 selected=v1:v1 responders=[replica-3=v1:v1]
```

첫 줄은 overlap이 있기 때문에 stale responder가 섞여도 최신이 선택되는 장면이다.  
둘째 줄은 stale responder만 보이기 때문에 read가 오래된 version을 반환하는 장면이다.

## 6. 검증 명령

```bash
cd go/ddia-distributed-systems/projects/06-quorum-and-consistency
GOWORK=off go test ./...
GOWORK=off go run ./cmd/quorum-demo
```

## 7. 핵심 파일

| 항목 | 위치 |
| --- | --- |
| 핵심 구현 | `internal/quorum/quorum.go` |
| 테스트 | `tests/quorum_test.go` |
| 데모 | `cmd/quorum-demo/main.go` |
| 개념 문서 | `docs/concepts/quorum-read-write.md` |

## 8. 다시 구현할 때 주의점

- write quorum 확인 전에 version을 올리지 말 것
- read merge는 responder 순서가 아니라 version 비교로 결정할 것
- stale read는 장애 유무보다 responder 집합 설계가 핵심이라는 점을 문서에서 분명히 남길 것
