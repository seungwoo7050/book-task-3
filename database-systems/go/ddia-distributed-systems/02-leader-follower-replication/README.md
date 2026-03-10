# 02 Leader-Follower Replication

append-only mutation log와 watermark 기반 incremental sync로 leader-follower replication을 구현합니다.

## 이 프로젝트에서 배우는 것

- leader가 local state와 append-only log를 어떻게 함께 유지하는지 익힙니다.
- follower가 watermark 이후 entry만 받아 incremental sync를 수행하는 방식을 이해합니다.
- idempotent apply가 왜 필요한지 확인합니다.

## 먼저 알고 있으면 좋은 것

- 기본 RPC/request flow를 이해하고 있으면 좋습니다.
- 단일 노드 key-value update가 어떻게 상태 변화를 만드는지 알고 있으면 읽기 쉽습니다.

## 추천 읽기 순서

1. `problem/README.md`로 문제 해석과 현재 범위를 먼저 확인합니다.
2. `docs/README.md`와 개념 노트를 읽어, 코드에 들어가기 전 핵심 용어를 맞춥니다.
3. `internal/`와 `tests/`를 함께 읽고, 마지막에 `cmd/replication/`로 동작 예시를 확인합니다.
4. `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 구현 표면

- `problem/`: 현재 프로젝트 문제 해석과 제공 자료
- `docs/`: 개념 메모와 설명형 참고자료 목록
- `internal/replication/`, `tests/`, `cmd/replication/`: 실제 구현과 검증 코드
- `notion/`: 현재 공개용 학습 노트
- `notion-archive/`: 이전 세대 문서 보관본

## 검증 명령

```bash
cd go/ddia-distributed-systems/02-leader-follower-replication
GOWORK=off go test ./...
GOWORK=off go run ./cmd/replication
```

## 구현에서 집중할 포인트

- leader write와 log append 순서가 안정적인지 확인합니다.
- follower watermark가 incremental sync 범위를 올바르게 잘라내는지 봅니다.
- 중복 entry 수신 시 상태가 깨지지 않는지 테스트를 확인합니다.

## 포트폴리오로 발전시키려면

- lag metrics, snapshot install, log truncation을 추가하면 replication 설계가 더 깊어집니다.
- 관찰 가능한 replication timeline을 붙이면 포트폴리오 전달력이 높아집니다.
