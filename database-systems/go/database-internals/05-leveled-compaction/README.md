# 05 Leveled Compaction

L0의 겹치는 SSTable을 병합하고 manifest를 원자적으로 갱신해 leveled compaction의 핵심만 구현합니다.

## 이 프로젝트에서 배우는 것

- newest-first 우선순위를 유지한 k-way merge를 구현합니다.
- deepest level에서만 tombstone을 제거하는 이유를 이해합니다.
- compaction 결과 파일과 manifest가 동시에 바뀌어야 하는 이유를 확인합니다.

## 먼저 알고 있으면 좋은 것

- SSTable과 mini LSM store의 flush/read 흐름을 알고 있어야 합니다.
- immutable file 집합을 새 파일 집합으로 교체하는 배경을 이해하고 있으면 좋습니다.

## 추천 읽기 순서

1. `problem/README.md`로 문제 해석과 현재 범위를 먼저 확인합니다.
2. `docs/README.md`와 개념 노트를 읽어, 코드에 들어가기 전 핵심 용어를 맞춥니다.
3. `internal/`와 `tests/`를 함께 읽고, 마지막에 `cmd/leveled-compaction/`로 동작 예시를 확인합니다.
4. `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 구현 표면

- `problem/`: 현재 프로젝트 문제 해석과 제공 자료
- `docs/`: 개념 메모와 설명형 참고자료 목록
- `internal/compaction/`, `internal/sstable/`, `tests/`, `cmd/leveled-compaction/`: 실제 구현과 검증 코드
- `notion/`: 현재 공개용 학습 노트
- `notion-archive/`: 이전 세대 문서 보관본

## 검증 명령

```bash
cd go/database-internals/05-leveled-compaction
GOWORK=off go test ./...
GOWORK=off go run ./cmd/leveled-compaction
```

## 구현에서 집중할 포인트

- newer-first source ordering이 merge 결과에 그대로 반영되는지 봅니다.
- manifest write가 중간 실패 시에도 이전 상태를 유지하도록 만드는 방법을 확인합니다.
- 입력 파일 정리와 결과 파일 생성의 순서가 안전한지 확인합니다.

## 포트폴리오로 발전시키려면

- size-tiered/leveled 전략 비교와 compaction scheduler를 추가하면 설계 폭이 넓어집니다.
- compaction statistics와 visualizer를 넣으면 포트폴리오 전달력이 좋아집니다.
