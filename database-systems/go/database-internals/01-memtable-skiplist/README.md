# 01 MemTable SkipList

LSM-Tree의 active memtable을 독립적인 SkipList로 구현해 정렬된 쓰기 경로와 tombstone semantics를 먼저 고정합니다.

## 이 프로젝트에서 배우는 것

- 정렬된 문자열 키-값 엔트리를 유지하는 in-memory write structure를 설계합니다.
- 삭제를 physical remove가 아니라 tombstone으로 표현하는 이유를 이해합니다.
- ordered iteration과 byte-size accounting이 다음 flush 단계에 왜 필요한지 확인합니다.

## 먼저 알고 있으면 좋은 것

- 정렬 자료구조와 linked list/skip list의 기본 동작을 알고 있으면 읽기 쉽습니다.
- 아직 SSTable이나 flush를 몰라도 시작할 수 있는 첫 프로젝트입니다.

## 추천 읽기 순서

1. `problem/README.md`로 문제 해석과 현재 범위를 먼저 확인합니다.
2. `problem/code/`의 보조 스타터나 스켈레톤을 보고 어떤 API를 구현해야 하는지 확인합니다.
3. `problem/data/`가 있다면 fixture나 입력 메모를 먼저 확인합니다.
4. `problem/script/`가 있다면 검증 방식이나 실행 메모를 확인합니다.
5. `docs/README.md`와 개념 노트를 읽어, 코드에 들어가기 전 핵심 용어를 맞춥니다.
6. `internal/`와 `tests/`를 함께 읽고, 마지막에 `cmd/skiplist-demo/`로 동작 예시를 확인합니다.
7. `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 구현 표면

- `problem/`: 현재 프로젝트 문제 해석과 제공 자료
- `docs/`: 개념 메모와 설명형 참고자료 목록
- `internal/skiplist/`, `tests/`, `cmd/skiplist-demo/`: 실제 구현과 검증 코드
- `notion/`: 현재 공개용 학습 노트
- `notion-archive/`: 이전 세대 문서 보관본

## 검증 명령

```bash
cd go/database-internals/01-memtable-skiplist
GOWORK=off go test ./...
GOWORK=off go run ./cmd/skiplist-demo
```

## 구현에서 집중할 포인트

- 삽입·갱신·삭제가 모두 key 순서를 깨지 않는지 확인합니다.
- tombstone과 missing state를 구분하는 API가 이후 상위 계층에 어떤 이점을 주는지 봅니다.
- 테스트와 demo가 같은 ordering 가정을 공유하는지 확인합니다.

## 포트폴리오로 발전시키려면

- skip list random level 정책과 benchmark를 추가해 자료구조 선택 근거를 보여 주세요.
- iterator API와 range scan 예시를 더하면 저장 엔진 다음 단계와의 연결이 선명해집니다.
