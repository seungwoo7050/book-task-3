# 01 MemTable SkipList

LSM-Tree의 active memtable을 독립적인 SkipList로 구현해 정렬된 쓰기 경로와 tombstone semantics를 먼저 고정합니다.

## 문제

- `Put(key, value)`는 새 키를 삽입하거나 기존 키를 갱신하면서 key 오름차순을 유지해야 합니다.
- `Get(key)`는 존재하는 값, tombstone, 미존재를 구분해야 합니다.
- `Delete(key)`는 엔트리를 없애지 않고 tombstone으로 바꿔야 합니다.
- 전체 엔트리를 key 오름차순으로 순회할 수 있어야 합니다.
- flush threshold 판단을 위해 대략적인 byte size를 추적해야 합니다.

## 내 해법

- 정렬된 문자열 키-값 엔트리를 유지하는 in-memory write structure를 설계합니다.
- 삭제를 physical remove가 아니라 tombstone으로 표현하는 이유를 이해합니다.
- ordered iteration과 byte-size accounting이 다음 flush 단계에 왜 필요한지 확인합니다.

## 검증

```bash
cd go/database-internals/projects/01-memtable-skiplist
GOWORK=off go test ./...
GOWORK=off go run ./cmd/skiplist-demo
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
- `problem/code/`의 보조 스타터나 스켈레톤을 보고 어떤 API를 구현해야 하는지 확인합니다.
- `problem/data/`가 있다면 fixture나 입력 메모를 먼저 확인합니다.
- `problem/script/`가 있다면 검증 방식이나 실행 메모를 확인합니다.
- `docs/README.md`와 개념 노트를 읽어, 코드에 들어가기 전 핵심 용어를 맞춥니다.
- `internal/`와 `tests/`를 함께 읽고, 마지막에 `cmd/skiplist-demo/`로 동작 예시를 확인합니다.
- `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 한계와 확장

- 현재 범위 밖: 동시성 제어와 lock-free 자료구조는 다루지 않습니다.
- 현재 범위 밖: 확률적 level tuning과 고급 benchmark는 후속 확장 범위로 남깁니다.
- 확장 아이디어: skip list random level 정책과 benchmark를 추가해 자료구조 선택 근거를 보여 주세요.
- 확장 아이디어: iterator API와 range scan 예시를 더하면 저장 엔진 다음 단계와의 연결이 선명해집니다.
