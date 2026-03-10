# 03 Mini LSM Store

active memtable, immutable flush, newest-first read path를 연결해 최소 LSM store를 완성합니다.

## 이 프로젝트에서 배우는 것

- active memtable이 threshold를 넘을 때 immutable swap과 flush가 어떻게 이어지는지 익힙니다.
- active/immutable/SSTable을 newest-first로 읽는 read path를 구성합니다.
- close 이후 re-open 시 persisted metadata를 다시 적재하는 흐름을 확인합니다.

## 먼저 알고 있으면 좋은 것

- memtable과 SSTable이 각각 어떤 책임을 맡는지 알고 있으면 좋습니다.
- flush와 reopen이 저장 엔진 전체에서 어떤 의미인지 익힐 준비가 되어 있으면 좋습니다.

## 추천 읽기 순서

1. `problem/README.md`로 문제 해석과 현재 범위를 먼저 확인합니다.
2. `docs/README.md`와 개념 노트를 읽어, 코드에 들어가기 전 핵심 용어를 맞춥니다.
3. `internal/`와 `tests/`를 함께 읽고, 마지막에 `cmd/mini-lsm-store/`로 동작 예시를 확인합니다.
4. `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 구현 표면

- `problem/`: 현재 프로젝트 문제 해석과 제공 자료
- `docs/`: 개념 메모와 설명형 참고자료 목록
- `internal/lsmstore/`, `internal/skiplist/`, `internal/sstable/`, `tests/`, `cmd/mini-lsm-store/`: 실제 구현과 검증 코드
- `notion/`: 현재 공개용 학습 노트
- `notion-archive/`: 이전 세대 문서 보관본

## 검증 명령

```bash
cd go/database-internals/03-mini-lsm-store
GOWORK=off go test ./...
GOWORK=off go run ./cmd/mini-lsm-store
```

## 구현에서 집중할 포인트

- 쓰기 경로와 읽기 경로가 tombstone semantics를 동일하게 해석하는지 확인합니다.
- flush 시점에 active와 immutable 상태가 뒤섞이지 않도록 경계를 명확히 봅니다.
- 테스트가 reopen 이후에도 같은 lookup 결과를 보장하는지 확인합니다.

## 포트폴리오로 발전시키려면

- manifest 파일과 background compaction을 추가하면 더 현실적인 mini storage engine으로 확장할 수 있습니다.
- flush/lookup 지표를 수집해 성능 관찰 포인트를 넣으면 포트폴리오 설득력이 높아집니다.
