# 05 Leveled Compaction

L0의 겹치는 SSTable을 병합하고 manifest를 원자적으로 갱신해 leveled compaction의 핵심만 구현합니다.

## 문제

- 입력 source 배열에서 newer-first 우선순위를 유지한 k-way merge를 수행해야 합니다.
- deepest level일 때만 tombstone을 제거해야 합니다.
- 새 SSTable 생성 후 manifest를 atomic write로 갱신해야 합니다.
- compaction이 끝나면 이전 입력 파일을 정리해야 합니다.

## 내 해법

- newest-first 우선순위를 유지한 k-way merge를 구현합니다.
- deepest level에서만 tombstone을 제거하는 이유를 이해합니다.
- compaction 결과 파일과 manifest가 동시에 바뀌어야 하는 이유를 확인합니다.

## 검증

```bash
cd go/database-internals/projects/05-leveled-compaction
GOWORK=off go test ./...
GOWORK=off go run ./cmd/leveled-compaction
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
- `internal/`와 `tests/`를 함께 읽고, 마지막에 `cmd/leveled-compaction/`로 동작 예시를 확인합니다.
- `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 한계와 확장

- 현재 범위 밖: background compaction scheduler와 multi-level balancing 정책은 포함하지 않습니다.
- 현재 범위 밖: compression과 block cache는 후속 확장 범위로 남깁니다.
- 확장 아이디어: size-tiered/leveled 전략 비교와 compaction scheduler를 추가하면 설계 폭이 넓어집니다.
- 확장 아이디어: compaction statistics와 visualizer를 넣으면 포트폴리오 전달력이 좋아집니다.
