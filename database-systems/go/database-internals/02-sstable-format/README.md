# 02 SSTable Format

immutable SSTable 파일 형식, sparse key index, footer metadata를 구현해 on-disk lookup의 기본을 고정합니다.

## 이 프로젝트에서 배우는 것

- 정렬된 record stream을 immutable file format으로 저장하는 방법을 익힙니다.
- footer와 sparse index가 point lookup 비용을 어떻게 줄이는지 이해합니다.
- tombstone을 디스크 포맷 안에서도 보존해야 하는 이유를 확인합니다.

## 먼저 알고 있으면 좋은 것

- 정렬된 엔트리를 순회할 수 있는 memtable 개념을 알고 있으면 좋습니다.
- 파일 I/O와 binary encoding의 기본 개념이 있으면 읽기 쉽습니다.

## 추천 읽기 순서

1. `problem/README.md`로 문제 해석과 현재 범위를 먼저 확인합니다.
2. `docs/README.md`와 개념 노트를 읽어, 코드에 들어가기 전 핵심 용어를 맞춥니다.
3. `internal/`와 `tests/`를 함께 읽고, 마지막에 `cmd/sstable-format/`로 동작 예시를 확인합니다.
4. `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 구현 표면

- `problem/`: 현재 프로젝트 문제 해석과 제공 자료
- `docs/`: 개념 메모와 설명형 참고자료 목록
- `internal/sstable/`, `tests/`, `cmd/sstable-format/`: 실제 구현과 검증 코드
- `notion/`: 현재 공개용 학습 노트
- `notion-archive/`: 이전 세대 문서 보관본

## 검증 명령

```bash
cd go/database-internals/02-sstable-format
GOWORK=off go test ./...
GOWORK=off go run ./cmd/sstable-format
```

## 구현에서 집중할 포인트

- data section, index section, footer가 서로 어떤 offset 계약을 맺는지 확인합니다.
- re-open 이후에도 lookup에 필요한 metadata만으로 index를 복원하는 흐름을 봅니다.
- tombstone sentinel을 round-trip 하는 테스트가 충분한지 확인합니다.

## 포트폴리오로 발전시키려면

- block compression이나 checksum 검증을 더해 포맷 설계 범위를 넓혀 보세요.
- range scan과 block cache를 붙이면 후속 LSM 프로젝트와의 연결이 자연스럽습니다.
