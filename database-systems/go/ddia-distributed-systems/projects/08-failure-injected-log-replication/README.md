# 08 Failure-Injected Log Replication

drop, duplicate, pause가 들어가는 작은 네트워크 하네스 위에서 append/ack 로그 복제와 quorum commit, follower catch-up을 재현합니다.

## 문제

- single leader가 append-only log를 가지고 follower에게 entry를 보낼 수 있어야 합니다.
- 메시지는 `append`와 `ack` 두 종류로 명시돼야 합니다.
- 네트워크 하네스는 drop, duplicate, pause를 스크립트로 주입할 수 있어야 합니다.
- leader는 retry로 lagging follower를 따라잡게 만들어야 합니다.
- commit index는 quorum ack를 기준으로만 올라가야 합니다.

## 내 해법

- dropped append가 retry로 수렴하는 흐름을 익힙니다.
- duplicate delivery가 follower 상태를 두 번 바꾸면 안 된다는 점을 확인합니다.
- follower 하나가 멈춰도 quorum commit은 유지되지만, 복구 전까지 lag는 남는다는 사실을 봅니다.

## 검증

```bash
cd go/ddia-distributed-systems/projects/08-failure-injected-log-replication
GOWORK=off go test ./...
GOWORK=off go run ./cmd/failure-replication
```

## 코드 지도

- `problem/README.md`: 문제 정의, 제약, 제공 자료, provenance를 확인하는 시작점입니다.
- `docs/README.md`: 개념 메모와 참고자료 인덱스를 먼저 훑는 문서입니다.
- `internal/`: 핵심 구현이 들어 있는 패키지입니다.
- `tests/`: 회귀 테스트와 검증 시나리오를 모아 둔 위치입니다.
- `cmd/`: 직접 실행해 흐름을 확인하는 demo entry point입니다.
- `notion/README.md`: 현재 공개용 학습 노트와 설계 로그의 입구입니다.
- `notion-archive/README.md`: 이전 세대 문서를 보존하는 아카이브입니다.

## 읽는 순서

- `problem/README.md`로 문제 해석과 현재 범위를 먼저 확인합니다.
- `docs/README.md`와 개념 노트를 읽어 failure injection과 quorum commit 질문을 맞춥니다.
- `internal/replication/`와 `tests/`를 함께 읽고, 마지막에 `cmd/failure-replication/`로 convergence 데모를 확인합니다.
- `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 한계와 확장

- 현재 범위 밖: full Raft term과 vote rule은 포함하지 않습니다.
- 현재 범위 밖: rebalancing, dynamic membership, snapshotting도 포함하지 않습니다.
- 현재 범위 밖: cross-shard routing이나 disk persistence는 다루지 않습니다.
- 확장 아이디어: ack drop, out-of-order delivery, backoff 정책을 추가하면 더 현실적인 replication harness가 됩니다.
- 확장 아이디어: timeline trace와 metrics를 붙이면 장애 재현 포트폴리오로 확장하기 좋습니다.
