# 06 Quorum and Consistency

quorum read/write와 versioned register를 이용해 `W + R > N`이 최신 읽기를 어떻게 보장하고, `W + R <= N`일 때 어떤 stale read가 생기는지 재현합니다.

## 문제

- replica 3개를 가진 versioned register를 구현해야 합니다.
- `N/W/R` 정책에 따라 write quorum과 read quorum을 검증해야 합니다.
- write는 quorum이 확보될 때만 version을 올려야 합니다.
- read는 responder 집합 안에서 가장 높은 version을 골라 반환해야 합니다.
- `W + R > N`과 `W + R <= N`의 차이를 고정 fixture로 재현해야 합니다.

## 내 해법

- replica 일부가 뒤처져도 quorum read가 최신 버전을 고르는 조건을 익힙니다.
- write quorum 실패가 왜 version advancement를 막아야 하는지 확인합니다.
- consistency와 availability가 `N/W/R` 조합에 따라 어떻게 달라지는지 작은 register 모델로 봅니다.

## 검증

```bash
cd go/ddia-distributed-systems/projects/06-quorum-and-consistency
GOWORK=off go test ./...
GOWORK=off go run ./cmd/quorum-demo
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

- `problem/README.md`로 이번 단계가 무엇을 고정하고 무엇을 일부러 뺐는지 먼저 확인합니다.
- `docs/README.md`와 개념 메모를 읽어 quorum read/write와 version merge 질문을 맞춥니다.
- `internal/quorum/`와 `tests/`를 함께 읽고, 마지막에 `cmd/quorum-demo/`로 stale read 데모를 확인합니다.
- `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 한계와 확장

- 현재 범위 밖: read repair, hinted handoff, anti-entropy는 포함하지 않습니다.
- 현재 범위 밖: vector clock, sibling merge, multi-key transaction도 포함하지 않습니다.
- 현재 범위 밖: membership change와 failure detector는 다음 프로젝트로 남깁니다.
- 확장 아이디어: read repair, hinted handoff, anti-entropy를 추가하면 실제 분산 저장소 운영 질문으로 확장할 수 있습니다.
- 확장 아이디어: latency histogram과 quorum decision trace를 붙이면 consistency trade-off가 더 설득력 있게 보입니다.
