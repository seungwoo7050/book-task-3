# 접근 기록

## 읽기 순서 제안
1. `../problem/README.md`에서 요구와 현재 재구성 범위를 먼저 확인합니다.
2. 구현 핵심 파일을 열어 어떤 타입과 함수가 중심인지 확인합니다.
3. `../tests/`를 읽어 이 프로젝트가 실제로 고정한 계약을 확인합니다.
4. 데모를 실행해 테스트가 말하는 계약이 출력으로도 드러나는지 봅니다.
5. 마지막에 개념 문서를 읽으며 용어와 설계 판단을 정리합니다.

## 코드가 택한 분해 방식
### 값 상태를 분리해 tombstone을 명시한다
- 관련 파일: `../internal/skiplist/skiplist.go`
- 판단: `Entry` 안에 value 유무만 두지 않고 `ValueState`를 둬서 live value, tombstone, missing을 명확히 구분했습니다. 이 선택이 다음 단계 on-disk format으로 그대로 이어집니다.

### 학습용 테스트를 위해 level 선택을 결정적으로 만든다
- 관련 파일: `../internal/skiplist/skiplist.go`
- 판단: 랜덤 level 생성은 유지하되 seed를 고정해 테스트와 데모가 매번 같은 구조를 따라가게 했습니다. 학습용 저장소에서는 이 재현성이 설명 비용을 크게 낮춥니다.

### 정렬 순회와 byte size를 flush 전 계약으로 노출한다
- 관련 파일: `../internal/skiplist/skiplist.go`, `../tests/skiplist_test.go`
- 판단: `Entries()`와 `ByteSize()`를 따로 제공해 다음 단계 SSTable flush가 어떤 입력 계약 위에 서는지 드러냈습니다.

## 검증 명령
```bash
cd go/database-internals/01-memtable-skiplist
go test ./...
go run ./cmd/skiplist-demo
```

## 포트폴리오 설명으로 바꿀 때 남길 장면
- ordered entries 출력과 tombstone 표시를 같이 보여 주면 write path invariant를 짧게 설명하기 좋습니다.
- `ValueState` 분리 선택은 missing과 delete를 어떻게 다르게 다뤘는지 보여 주는 좋은 설계 포인트입니다.
- 결정적 seed를 둔 이유를 설명하면 “학습용 구현에서 재현성을 어떻게 확보했는가”를 말할 수 있습니다.
