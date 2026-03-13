# 07 Heartbeat and Leader Election 시리즈 맵

이 시리즈는 DDIA Distributed Systems 트랙의 7번째 프로젝트 `07 Heartbeat and Leader Election`를 따라간다. heartbeat 기반 failure detector와 majority vote만으로 leader failover를 재현하는 작은 election lab을 구현합니다. 기능 목록보다 먼저, 어떤 순서로 경계를 고정했는지 읽는 쪽에 무게를 두었다.

## 먼저 보고 갈 질문

- leader가 주기적으로 heartbeat를 보내야 합니다.
- follower는 heartbeat silence가 길어지면 leader를 suspect해야 합니다.

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md) — 테스트 이름과 파일 배치부터 훑으면서 문제의 테두리를 다시 좁히는 글
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md) — 핵심 함수와 상태 전이에서 invariant가 실제로 어디서 잠기는지 따라가는 글
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md) — 테스트와 demo를 다시 돌려 약속 범위와 남는 한계를 정리하는 글

## 재검증 명령

```bash
GOWORK=off go test ./...
GOWORK=off go run ./cmd/leader-election
```

## 이번 시리즈가 근거로 삼은 파일

- `database-systems/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/internal/election/election.go`
- `database-systems/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/tests/election_test.go`
- `database-systems/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/README.md`
- `database-systems/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/problem/README.md`
- `database-systems/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/docs/README.md`
- `database-systems/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/cmd/leader-election/main.go`

## 보조 메모

작업 메모가 꼭 필요할 때만 [_evidence-ledger.md](_evidence-ledger.md)와 [_structure-outline.md](_structure-outline.md)를 보면 된다. 공개 시리즈는 `00 -> 10 -> 20 -> 30`만 따라가면 충분하다.

## Git Anchor

- `2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료`
