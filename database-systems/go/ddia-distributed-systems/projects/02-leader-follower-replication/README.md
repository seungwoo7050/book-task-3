# 02 Leader-Follower Replication

append-only mutation log와 watermark 기반 incremental sync로 leader-follower replication을 구현합니다.

## 문제

- 순차 offset을 갖는 mutation log를 유지해야 합니다.
- `put`과 `delete`가 복제돼야 합니다.
- follower watermark 기반 incremental sync가 필요합니다.
- 같은 entry를 다시 받아도 결과가 깨지지 않는 idempotent apply가 필요합니다.

## 내 해법

- leader가 local state와 append-only log를 어떻게 함께 유지하는지 익힙니다.
- follower가 watermark 이후 entry만 받아 incremental sync를 수행하는 방식을 이해합니다.
- idempotent apply가 왜 필요한지 확인합니다.

## 검증

```bash
cd go/ddia-distributed-systems/projects/02-leader-follower-replication
GOWORK=off go test ./...
GOWORK=off go run ./cmd/replication
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
- `internal/`와 `tests/`를 함께 읽고, 마지막에 `cmd/replication/`로 동작 예시를 확인합니다.
- `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 한계와 확장

- 현재 범위 밖: automatic leader election과 consensus는 포함하지 않습니다.
- 현재 범위 밖: quorum write나 multi-leader replication은 다루지 않습니다.
- 확장 아이디어: lag metrics, snapshot install, log truncation을 추가하면 replication 설계가 더 깊어집니다.
- 확장 아이디어: 관찰 가능한 replication timeline을 붙이면 포트폴리오 전달력이 높아집니다.
