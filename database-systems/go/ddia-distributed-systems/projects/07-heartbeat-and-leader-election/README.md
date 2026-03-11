# 07 Heartbeat and Leader Election

heartbeat 기반 failure detector와 majority vote만으로 leader failover를 재현하는 작은 election lab을 구현합니다.

## 문제

- leader가 주기적으로 heartbeat를 보내야 합니다.
- follower는 heartbeat silence가 길어지면 leader를 suspect해야 합니다.
- election은 term을 올리고 majority vote를 받아야만 leader가 될 수 있습니다.
- higher term을 본 old leader는 즉시 follower로 step-down해야 합니다.
- 이 모든 흐름은 tick 기반 결정적 시뮬레이션으로 재현돼야 합니다.

## 내 해법

- heartbeat silence가 suspicion으로 바뀌고, 그 다음 election으로 이어지는 흐름을 익힙니다.
- majority vote 없이는 isolated node가 leader가 될 수 없음을 확인합니다.
- higher term heartbeat가 old leader를 follower로 되돌리는 이유를 이해합니다.

## 검증

```bash
cd go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election
GOWORK=off go test ./...
GOWORK=off go run ./cmd/leader-election
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
- `docs/README.md`와 개념 노트를 읽어 failure detector와 election term을 맞춥니다.
- `internal/election/`와 `tests/`를 함께 읽고, 마지막에 `cmd/leader-election/`로 failover 데모를 확인합니다.
- `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 한계와 확장

- 현재 범위 밖: log replication과 commit rule은 포함하지 않습니다.
- 현재 범위 밖: randomized timeout, network partition, pre-vote도 포함하지 않습니다.
- 현재 범위 밖: membership change와 lease-based leader validation도 포함하지 않습니다.
- 확장 아이디어: randomized timeout, network partition, pre-vote를 추가하면 Raft 전단계 포트폴리오로 확장할 수 있습니다.
- 확장 아이디어: state timeline visualizer를 붙이면 split-brain 방지 로직이 더 잘 보입니다.
