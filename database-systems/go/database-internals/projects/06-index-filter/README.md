# 06 Index Filter

Bloom filter와 sparse index를 붙여 point lookup이 전체 SSTable 스캔으로 떨어지지 않도록 만듭니다.

## 문제

- Bloom filter를 직렬화·복원할 수 있어야 합니다.
- 정렬된 key-offset 스트림에서 sparse index를 생성해야 합니다.
- footer metadata를 읽어 filter와 index 위치를 복원해야 합니다.
- lookup 시 bloom reject와 bounded block scan이 둘 다 드러나야 합니다.

## 내 해법

- Bloom filter가 negative lookup 비용을 어떻게 줄이는지 이해합니다.
- sparse index가 block scan 범위를 좁히는 방식을 익힙니다.
- footer metadata로 filter/index 위치를 복원하는 방법을 확인합니다.

## 검증

```bash
cd go/database-internals/projects/06-index-filter
GOWORK=off go test ./...
GOWORK=off go run ./cmd/index-filter
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
- `internal/`와 `tests/`를 함께 읽고, 마지막에 `cmd/index-filter/`로 동작 예시를 확인합니다.
- `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 한계와 확장

- 현재 범위 밖: learned index와 adaptive filter는 포함하지 않습니다.
- 현재 범위 밖: range query 최적화와 block cache 연동은 다음 단계 확장으로 남깁니다.
- 확장 아이디어: false positive rate 실험과 bit budget 비교표를 추가하면 설계 감각을 드러내기 좋습니다.
- 확장 아이디어: block cache와 range scan을 연결하면 읽기 최적화 이야기로 확장할 수 있습니다.
