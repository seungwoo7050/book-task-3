# 지식 인덱스

## 핵심 용어
- `quorum`: 어떤 작업을 성공으로 인정하는 최소 replica 수입니다.
- `overlap`: read quorum과 write quorum이 적어도 하나의 replica를 공유하는 조건입니다.
- `stale read`: read quorum이 최신 write를 보지 못해 오래된 version을 반환하는 상황입니다.
- `versioned register`: `(version, data)`만 가진 아주 작은 key-value 모델입니다.

## 재현 순서용 파일 맵
- `../internal/quorum/quorum.go`: `Replica`, `Cluster`, `Policy`, `ReadResult` 구현 전체가 있습니다.
- `../tests/quorum_test.go`: overlap, stale read, quorum failure를 시나리오별로 검증합니다.
- `../cmd/quorum-demo/main.go`: `W=2/R=2`와 `W=1/R=1`을 나란히 보여 주는 데모입니다.
- `../docs/concepts/quorum-read-write.md`: quorum overlap을 설명합니다.

## 바로 실행할 명령
```bash
cd go/ddia-distributed-systems/projects/06-quorum-and-consistency
go test ./... -run TestReadReturnsLatestWhenQuorumsOverlap -v
go test ./... -run TestStaleReadAppearsWhenQuorumsDoNotOverlap -v
go run ./cmd/quorum-demo
```

## 기대 결과
- `W=2, R=2`에서는 responder 중 하나가 stale여도 최신 version이 선택됩니다.
- `W=1, R=1`에서는 stale responder만 고르면 오래된 version이 읽힙니다.
- quorum 실패 write는 version을 올리지 않습니다.

## 검증 앵커
- 확인일: 2026-03-11
- 테스트 파일: `../tests/quorum_test.go`
- 데모 파일: `../cmd/quorum-demo/main.go`

- 더 긴 이전 기록은 `../notion-archive/`에 남겨 두고, 여기에는 다시 구현할 때 바로 필요한 정보만 남깁니다.
