# 06 Quorum and Consistency

quorum read/write와 versioned register를 이용해 `W + R > N`이 최신 읽기를 어떻게 보장하고, `W + R <= N`일 때 어떤 stale read가 생기는지 재현합니다.

## 이 프로젝트에서 배우는 것

- replica 일부가 뒤처져도 quorum read가 최신 버전을 고르는 조건을 익힙니다.
- write quorum 실패가 왜 version advancement를 막아야 하는지 확인합니다.
- consistency와 availability가 `N/W/R` 조합에 따라 어떻게 달라지는지 작은 register 모델로 봅니다.

## 먼저 알고 있으면 좋은 것

- leader-follower replication과 Raft-lite를 먼저 읽었으면 더 자연스럽습니다.
- 완전한 eventual consistency 시스템이 아니라 학습용 versioned register라는 점을 알고 시작하면 좋습니다.

## 추천 읽기 순서

1. `problem/README.md`로 이번 단계가 무엇을 고정하고 무엇을 일부러 뺐는지 먼저 확인합니다.
2. `docs/README.md`와 개념 메모를 읽어 quorum read/write와 version merge 질문을 맞춥니다.
3. `internal/quorum/`와 `tests/`를 함께 읽고, 마지막에 `cmd/quorum-demo/`로 stale read 데모를 확인합니다.
4. `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 구현 표면

- `problem/`: 현재 프로젝트 문제 해석과 제공 자료
- `docs/`: 개념 메모와 설명형 참고자료 목록
- `internal/quorum/`, `tests/`, `cmd/quorum-demo/`: 실제 구현과 검증 코드
- `notion/`: 현재 공개용 학습 노트
- `notion-archive/`: 이전 세대 문서 보관본

## 검증 명령

```bash
cd go/ddia-distributed-systems/06-quorum-and-consistency
GOWORK=off go test ./...
GOWORK=off go run ./cmd/quorum-demo
```

## 구현에서 집중할 포인트

- read responder가 항상 결정적 순서로 고정되어야 stale read를 재현하기 쉽습니다.
- write quorum 실패 시 replica local state와 cluster version이 함께 멈추는지 확인합니다.
- `W + R > N` 조건이 “항상 모든 replica가 최신”을 뜻하는 것이 아니라, read quorum 안에 최신 replica가 반드시 하나 포함된다는 뜻임을 테스트에서 봅니다.

## 포트폴리오로 발전시키려면

- read repair, hinted handoff, anti-entropy를 추가하면 실제 분산 저장소 운영 질문으로 확장할 수 있습니다.
- latency histogram과 quorum decision trace를 붙이면 consistency trade-off가 더 설득력 있게 보입니다.
