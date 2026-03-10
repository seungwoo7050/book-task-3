# 04 Raft Lite

leader election, vote rule, AppendEntries consistency, majority commit이 드러나는 작은 동기 Raft 시뮬레이터를 구현합니다.

## 이 프로젝트에서 배우는 것

- term과 election cycle이 leader 교체를 어떻게 제어하는지 익힙니다.
- AppendEntries consistency와 commit rule을 이해합니다.
- higher term 발견 시 step-down이 왜 필요한지 확인합니다.

## 먼저 알고 있으면 좋은 것

- leader/follower replication 개념을 이해하고 있어야 합니다.
- 분산 시스템에서 consensus가 왜 필요한지 큰 그림을 알고 있으면 좋습니다.

## 추천 읽기 순서

1. `problem/README.md`로 문제 해석과 현재 범위를 먼저 확인합니다.
2. `docs/README.md`와 개념 노트를 읽어, 코드에 들어가기 전 핵심 용어를 맞춥니다.
3. `internal/`와 `tests/`를 함께 읽고, 마지막에 `cmd/raft-lite/`로 동작 예시를 확인합니다.
4. `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 구현 표면

- `problem/`: 현재 프로젝트 문제 해석과 제공 자료
- `docs/`: 개념 메모와 설명형 참고자료 목록
- `internal/raft/`, `tests/`, `cmd/raft-lite/`: 실제 구현과 검증 코드
- `notion/`: 현재 공개용 학습 노트
- `notion-archive/`: 이전 세대 문서 보관본

## 검증 명령

```bash
cd go/ddia-distributed-systems/04-raft-lite
GOWORK=off go test ./...
GOWORK=off go run ./cmd/raft-lite
```

## 구현에서 집중할 포인트

- 단일 leader 보장이 테스트에서 어떻게 드러나는지 확인합니다.
- up-to-date log를 가진 candidate만 승리하는 vote rule을 봅니다.
- majority replicated entry만 commit하는 규칙이 깨지지 않는지 확인합니다.

## 포트폴리오로 발전시키려면

- persistent log, snapshotting, InstallSnapshot RPC를 추가하면 진짜 Raft 학습 레포로 확장할 수 있습니다.
- fault injection과 timeline visualizer를 붙이면 학습용 포트폴리오로 강해집니다.
