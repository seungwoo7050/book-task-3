# 06 Quorum and Consistency 시리즈 맵

이 시리즈는 DDIA Distributed Systems 트랙의 6번째 프로젝트 `06 Quorum and Consistency`를 따라간다. quorum read/write와 versioned register를 이용해 `W + R > N`이 최신 읽기를 어떻게 보장하고, `W + R <= N`일 때 어떤 stale read가 생기는지 재현합니다. 기능 목록보다 먼저, 어떤 순서로 경계를 고정했는지 읽는 쪽에 무게를 두었다.

## 먼저 보고 갈 질문

- replica 3개를 가진 versioned register를 구현해야 합니다.
- `N/W/R` 정책에 따라 write quorum과 read quorum을 검증해야 합니다.

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md) — 테스트 이름과 파일 배치부터 훑으면서 문제의 테두리를 다시 좁히는 글
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md) — 핵심 함수와 상태 전이에서 invariant가 실제로 어디서 잠기는지 따라가는 글
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md) — 테스트와 demo를 다시 돌려 약속 범위와 남는 한계를 정리하는 글

## 재검증 명령

```bash
GOWORK=off go test ./...
GOWORK=off go run ./cmd/quorum-demo
```

## 이번 시리즈가 근거로 삼은 파일

- `database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency/internal/quorum/quorum.go`
- `database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency/tests/quorum_test.go`
- `database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency/README.md`
- `database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency/problem/README.md`
- `database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency/docs/README.md`
- `database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency/cmd/quorum-demo/main.go`

## 보조 메모

작업 메모가 꼭 필요할 때만 [_evidence-ledger.md](_evidence-ledger.md)와 [_structure-outline.md](_structure-outline.md)를 보면 된다. 공개 시리즈는 `00 -> 10 -> 20 -> 30`만 따라가면 충분하다.

## Git Anchor

- `2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료`
