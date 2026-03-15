# 06 Quorum and Consistency 시리즈 맵

`06 Quorum and Consistency`는 합의 알고리즘으로 넘어가기 전에, replica overlap만으로 최신 읽기와 stale read를 어떻게 설명할 수 있는지 작은 versioned register로 고정하는 프로젝트다. 이번 문서 묶음은 교과서 공식을 요약하는 대신, 이 구현이 실제로 어떤 단순화를 택했는지까지 같이 드러내는 데 초점을 둔다.

## 이번 Todo에서 다시 잡은 질문

- 이 구현에서 write quorum은 정확히 무엇을 뜻하는가?
- read quorum은 "아무 R개"인가, 아니면 결정된 responder 집합인가?
- `W + R > N`과 `W + R <= N`의 차이가 테스트와 demo에서 어떻게 재현되는가?

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md)
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md)
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md)

## 이번 재작성의 근거

- `database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency/problem/README.md`
- `database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency/README.md`
- `database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency/docs/concepts/quorum-read-write.md`
- `database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency/docs/concepts/versioned-register.md`
- `database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency/internal/quorum/quorum.go`
- `database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency/tests/quorum_test.go`
- `database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency/cmd/quorum-demo/main.go`

## 재검증 명령

```bash
GOWORK=off go test ./...
GOWORK=off go run ./cmd/quorum-demo
```

## 보조 문서

- [_evidence-ledger.md](_evidence-ledger.md)
- [_structure-outline.md](_structure-outline.md)

## 이번에 명시적으로 남긴 경계

- write는 quorum 확보 여부를 먼저 검사하고, 실패하면 partial write 없이 즉시 에러를 반환한다.
- quorum이 확보된 write는 `W`개에만 쓰는 게 아니라 살아 있는 replica 전부에 fanout한다.
- read는 latency race가 아니라 `order` 배열 기준 첫 `R`개 responder만 본다.
- read repair, hinted handoff, anti-entropy, vector clock은 없다.
