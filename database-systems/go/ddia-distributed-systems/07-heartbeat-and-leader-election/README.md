# 07 Heartbeat and Leader Election

heartbeat 기반 failure detector와 majority vote만으로 leader failover를 재현하는 작은 election lab을 구현합니다.

## 이 프로젝트에서 배우는 것

- heartbeat silence가 suspicion으로 바뀌고, 그 다음 election으로 이어지는 흐름을 익힙니다.
- majority vote 없이는 isolated node가 leader가 될 수 없음을 확인합니다.
- higher term heartbeat가 old leader를 follower로 되돌리는 이유를 이해합니다.

## 먼저 알고 있으면 좋은 것

- quorum consistency를 먼저 읽었으면 “누가 최신값을 믿게 만들 것인가” 질문과 자연스럽게 이어집니다.
- full Raft log replication이 아니라 election만 떼어 낸 모델이라는 점을 알고 시작하면 좋습니다.

## 추천 읽기 순서

1. `problem/README.md`로 문제 해석과 현재 범위를 먼저 확인합니다.
2. `docs/README.md`와 개념 노트를 읽어 failure detector와 election term을 맞춥니다.
3. `internal/election/`와 `tests/`를 함께 읽고, 마지막에 `cmd/leader-election/`로 failover 데모를 확인합니다.
4. `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 구현 표면

- `problem/`: 현재 프로젝트 문제 해석과 제공 자료
- `docs/`: 개념 메모와 설명형 참고자료 목록
- `internal/election/`, `tests/`, `cmd/leader-election/`: 실제 구현과 검증 코드
- `notion/`: 현재 공개용 학습 노트
- `notion-archive/`: 이전 세대 문서 보관본

## 검증 명령

```bash
cd go/ddia-distributed-systems/07-heartbeat-and-leader-election
GOWORK=off go test ./...
GOWORK=off go run ./cmd/leader-election
```

## 구현에서 집중할 포인트

- suspicion과 election을 같은 순간으로 합치지 않고 한 tick 분리해야 상태가 읽기 쉽습니다.
- majority 없는 self-promotion이 없는지 isolated node 테스트를 먼저 봅니다.
- recovered old leader가 stale authority를 유지하지 못하도록 higher term step-down을 확인합니다.

## 포트폴리오로 발전시키려면

- randomized timeout, network partition, pre-vote를 추가하면 Raft 전단계 포트폴리오로 확장할 수 있습니다.
- state timeline visualizer를 붙이면 split-brain 방지 로직이 더 잘 보입니다.
