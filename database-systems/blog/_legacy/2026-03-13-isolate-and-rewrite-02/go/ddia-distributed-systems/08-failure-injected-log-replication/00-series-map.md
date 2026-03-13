# 08 Failure-Injected Log Replication — Series Map

drop, duplicate, pause가 들어가는 작은 네트워크 하네스 위에서 append/ack 로그 복제와 quorum commit, follower catch-up을 재현합니다. 이 시리즈는 기존 초안의 말투를 따라가지 않고, 실제 코드와 검증 신호를 다시 읽으면서 판단이 어디서 바뀌는지에만 집중한다.

## 이 프로젝트가 답하는 질문

- single leader가 append-only log를 가지고 follower에게 entry를 보낼 수 있어야 합니다.
- 메시지는 `append`와 `ack` 두 종류로 명시돼야 합니다.

## 작업 산출물

- [_evidence-ledger.md](_evidence-ledger.md)
- [_structure-outline.md](_structure-outline.md)

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md) — 파일 구조와 테스트 이름으로 범위를 다시 잡는 구간
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md) — 핵심 invariant를 코드 조각으로 고정하는 구간
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md) — 실제 pass 신호와 남은 경계를 정리하는 구간

## 참조한 실제 파일

- `database-systems/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/internal/replication/replication.go`
- `database-systems/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/tests/replication_test.go`
- `database-systems/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/README.md`
- `database-systems/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/problem/README.md`
- `database-systems/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/docs/README.md`
- `database-systems/go/ddia-distributed-systems/projects/08-failure-injected-log-replication/cmd/failure-replication/main.go`

## 재검증 명령

```bash
GOWORK=off go test ./...
GOWORK=off go run ./cmd/failure-replication
```

## Git Anchor

- `2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료`
