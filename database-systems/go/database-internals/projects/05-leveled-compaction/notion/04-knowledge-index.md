# 지식 인덱스

## 핵심 용어
- `compaction`: 여러 SSTable을 병합해 새 파일 집합으로 재구성하는 작업입니다.
- `manifest`: 현재 level별 파일 집합과 다음 sequence를 기록하는 metadata입니다.
- `sequence ordering`: 같은 key 충돌 시 어느 record가 더 최신인지 판단하는 기준입니다.
- `deepest level`: tombstone을 더 내려보낼 필요가 없다고 가정할 수 있는 최하위 level입니다.
- `L0 reverse`: flush 순서로 쌓인 L0 파일을 merge 직전에 newest-first로 뒤집는 규칙입니다.

## 재현 순서용 파일 맵
- `../internal/sstable/sstable.go`: 결과 파일을 읽고 검증하는 포맷입니다.
- `../internal/compaction/compaction.go`: merge, file rewrite, manifest 저장, 입력 파일 삭제가 모두 있습니다.
- `../tests/compaction_test.go`: 각 규칙이 깨졌을 때 어디서 잡히는지 알려 주는 기준입니다.
- `../cmd/leveled-compaction/main.go`: 가장 짧은 end-to-end 확인 경로입니다.

## 바로 실행할 명령
```bash
cd go/database-internals/projects/05-leveled-compaction
go test ./... -run TestKWayMergeKeepsNewerValue -v
go test ./... -run TestCompactL0ToL1 -v
go test ./... -run TestManifestRoundTrip -v
go run ./cmd/leveled-compaction
```

## 기대 결과
### 데모 출력
```text
apple=red
banana=gold
pear=green
```

### 통합 테스트가 확인하는 값
- `a`는 `1-newer`
- `b`는 `2-new`
- `c`는 deepest level tombstone drop 때문에 조회되지 않음
- removed 파일 4개는 실제 디스크에서 사라짐

## 개념 문서
- `../docs/concepts/manifest-atomicity.md`: 파일과 metadata를 왜 함께 갱신해야 하는지 설명합니다.
- `../docs/concepts/merge-ordering.md`: newest-first source 규칙과 same key 충돌 해결 방식을 설명합니다.

## 다음 단계 연결
- `06-index-filter`에서는 compaction으로 정리된 파일을 더 빠르게 읽는 방법을 다룹니다.
- 이 단계에서 고정한 전제는 “파일 집합은 정리됐지만, `Get`은 아직 읽기 비용이 크다”입니다.

## 검증 앵커
- 확인일: 2026-03-11
- 테스트 파일: `../tests/compaction_test.go`
- 다시 돌릴 테스트 이름: `TestKWayMergeKeepsNewerValue`, `TestKWayMergeDropsTombstonesAtDeepestLevel`, `TestCompactL0ToL1`, `TestManifestRoundTrip`

- 더 긴 이전 기록은 `../notion-archive/`에 남겨 두고, 여기에는 다시 구현할 때 바로 필요한 정보만 남깁니다.
