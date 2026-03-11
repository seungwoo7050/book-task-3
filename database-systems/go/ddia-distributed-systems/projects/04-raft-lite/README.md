# 04 Raft Lite

leader election, vote rule, AppendEntries consistency, majority commit이 드러나는 작은 동기 Raft 시뮬레이터를 구현합니다.

## 문제

- leader election과 단일 leader 보장을 재현해야 합니다.
- up-to-date log vote rule을 구현해야 합니다.
- AppendEntries consistency check가 필요합니다.
- majority replicated entry만 commit해야 합니다.
- higher term 발견 시 leader가 step-down해야 합니다.

## 내 해법

- term과 election cycle이 leader 교체를 어떻게 제어하는지 익힙니다.
- AppendEntries consistency와 commit rule을 이해합니다.
- higher term 발견 시 step-down이 왜 필요한지 확인합니다.

## 검증

```bash
cd go/ddia-distributed-systems/projects/04-raft-lite
GOWORK=off go test ./...
GOWORK=off go run ./cmd/raft-lite
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
- `docs/README.md`와 개념 노트를 읽어, 코드에 들어가기 전 핵심 용어를 맞춥니다.
- `internal/`와 `tests/`를 함께 읽고, 마지막에 `cmd/raft-lite/`로 동작 예시를 확인합니다.
- `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 한계와 확장

- 현재 범위 밖: production-grade persistence, membership change, snapshotting은 포함하지 않습니다.
- 현재 범위 밖: 실제 네트워크 transport와 disk-backed log는 후속 확장으로 남깁니다.
- 확장 아이디어: persistent log, snapshotting, InstallSnapshot RPC를 추가하면 진짜 Raft 학습 레포로 확장할 수 있습니다.
- 확장 아이디어: fault injection과 timeline visualizer를 붙이면 학습용 포트폴리오로 강해집니다.
