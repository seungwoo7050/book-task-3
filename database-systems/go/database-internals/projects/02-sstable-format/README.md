# 02 SSTable Format

immutable SSTable 파일 형식, sparse key index, footer metadata를 구현해 on-disk lookup의 기본을 고정합니다.

## 문제

- data section은 key 오름차순 record의 연속 바이트 배열이어야 합니다.
- index section은 `(key, offset)` 쌍을 저장해 point lookup 시작 위치를 알려야 합니다.
- footer는 data/index section 크기를 기록해야 합니다.
- tombstone은 value length sentinel 같은 명시적 표현으로 보존해야 합니다.
- file reopen 이후에도 index load와 lookup이 동작해야 합니다.

## 내 해법

- 정렬된 record stream을 immutable file format으로 저장하는 방법을 익힙니다.
- footer와 sparse index가 point lookup 비용을 어떻게 줄이는지 이해합니다.
- tombstone을 디스크 포맷 안에서도 보존해야 하는 이유를 확인합니다.

## 검증

```bash
cd go/database-internals/projects/02-sstable-format
GOWORK=off go test ./...
GOWORK=off go run ./cmd/sstable-format
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
- `internal/`와 `tests/`를 함께 읽고, 마지막에 `cmd/sstable-format/`로 동작 예시를 확인합니다.
- `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 한계와 확장

- 현재 범위 밖: compression, block cache, range tombstone은 포함하지 않습니다.
- 현재 범위 밖: multi-level manifest 관리와 compaction 연결은 다음 프로젝트로 넘깁니다.
- 확장 아이디어: block compression이나 checksum 검증을 더해 포맷 설계 범위를 넓혀 보세요.
- 확장 아이디어: range scan과 block cache를 붙이면 후속 LSM 프로젝트와의 연결이 자연스럽습니다.
