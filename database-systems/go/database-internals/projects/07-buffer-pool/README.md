# 07 Buffer Pool

disk-backed page를 메모리에 캐시하고 pin count와 dirty write-back 정책을 포함한 buffer pool manager를 구현합니다.

## 문제

- page id로 file path와 page number를 안정적으로 분리해야 합니다.
- fetch 시 cache hit면 pin count를 올리고, miss면 disk read 후 캐시에 올려야 합니다.
- dirty page는 eviction이나 explicit flush 때 write-back해야 합니다.
- pinned page는 eviction하면 안 됩니다.

## 내 해법

- 고정 크기 page를 메모리에 캐시하는 기본 구조를 익힙니다.
- pin/unpin이 eviction 가능 여부를 어떻게 바꾸는지 이해합니다.
- dirty page를 flush하거나 write-back하는 시점을 설계합니다.

## 검증

```bash
cd go/database-internals/projects/07-buffer-pool
GOWORK=off go test ./...
GOWORK=off go run ./cmd/buffer-pool
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
- `internal/`와 `tests/`를 함께 읽고, 마지막에 `cmd/buffer-pool/`로 동작 예시를 확인합니다.
- `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 한계와 확장

- 현재 범위 밖: concurrent latch, lock manager, asynchronous IO는 포함하지 않습니다.
- 현재 범위 밖: buffer pool을 B-tree나 query executor와 연결하는 단계는 후속 범위로 남깁니다.
- 확장 아이디어: Clock replacer나 async flush worker를 추가하면 시스템 설계 폭이 넓어집니다.
- 확장 아이디어: cache hit ratio, flush 횟수, pin 대기 같은 지표를 넣으면 운영 관점 이야기가 생깁니다.
