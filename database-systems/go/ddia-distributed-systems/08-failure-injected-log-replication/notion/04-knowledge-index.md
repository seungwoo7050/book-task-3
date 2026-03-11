# 지식 인덱스

## 핵심 용어
- `append`: leader가 follower에게 log entry를 보내는 메시지입니다.
- `ack`: follower가 특정 index까지 받았다고 leader에게 알려 주는 메시지입니다.
- `nextIndex`: leader가 각 follower에게 다음으로 보내야 하는 log index입니다.
- `commit index`: quorum ack가 모여 성공으로 인정된 마지막 log index입니다.

## 재현 순서용 파일 맵
- `../internal/replication/replication.go`: `Leader`, `Follower`, `Message`, `NetworkHarness`, `Cluster` 구현 전체가 있습니다.
- `../tests/replication_test.go`: drop, duplicate, pause, recovery를 시나리오별로 검증합니다.
- `../cmd/failure-replication/main.go`: failure injection 타임라인 데모입니다.
- `../docs/concepts/quorum-commit-and-retry.md`: commit과 convergence 관계를 설명합니다.

## 바로 실행할 명령
```bash
cd go/ddia-distributed-systems/08-failure-injected-log-replication
go test ./... -run TestDroppedAppendRetriesUntilFollowerConverges -v
go test ./... -run TestDuplicateAppendIsIdempotent -v
go run ./cmd/failure-replication
```

## 기대 결과
- 첫 tick에서는 한 follower가 drop 때문에 뒤처져도 commit은 진행됩니다.
- duplicate append 뒤에도 follower log length는 1 증가만 보입니다.
- paused follower는 resume 뒤 retry로 leader와 같은 watermark에 도달합니다.

## 검증 앵커
- 확인일: 2026-03-11
- 테스트 파일: `../tests/replication_test.go`
- 데모 파일: `../cmd/failure-replication/main.go`

- 더 긴 이전 기록은 `../notion-archive/`에 남겨 두고, 여기에는 다시 구현할 때 바로 필요한 정보만 남깁니다.
