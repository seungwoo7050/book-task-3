# 접근 기록

## 읽기 순서 제안
1. `../problem/README.md`에서 요구와 현재 재구성 범위를 먼저 확인합니다.
2. 구현 핵심 파일을 열어 어떤 타입과 함수가 중심인지 확인합니다.
3. `../tests/`를 읽어 이 프로젝트가 실제로 고정한 계약을 확인합니다.
4. 데모를 실행해 테스트가 말하는 계약이 출력으로도 드러나는지 봅니다.
5. 마지막에 개념 문서를 읽으며 용어와 설계 판단을 정리합니다.

## 코드가 택한 분해 방식
### footer에서 index 시작점을 거꾸로 찾는다
- 관련 파일: `../internal/sstable/sstable.go`
- 판단: 파일 끝에서 footer 하나만 읽으면 index를 찾을 수 있게 해 metadata 위치를 고정했습니다. 이 방식이 학습용 포맷에서 가장 설명하기 쉽습니다.

### index는 한 번 읽어 메모리에 올리고 lookup은 그 위에서 시작한다
- 관련 파일: `../internal/sstable/sstable.go`
- 판단: `LoadIndex`로 index를 먼저 읽고, point lookup은 해당 구간만 다시 읽게 했습니다. 전체 파일 scan과 lookup 경로를 분리하려는 선택입니다.

### `ReadAll`을 남겨 디버깅 경로를 따로 확보한다
- 관련 파일: `../internal/sstable/sstable.go`, `../tests/sstable_test.go`
- 판단: production path는 lookup이지만, 학습 단계에서는 파일 전체를 눈으로 확인하는 도구가 있어야 footer/index 문제를 빨리 찾을 수 있습니다.

## 검증 명령
```bash
cd go/database-internals/02-sstable-format
go test ./...
go run ./cmd/sstable-format
```

## 포트폴리오 설명으로 바꿀 때 남길 장면
- SSTable layout 그림과 malformed footer test를 함께 보여 주면 파일 포맷 설명이 짧고 강해집니다.
- `Lookup`과 `ReadAll`을 둘 다 남긴 이유를 설명하면 runtime path와 inspection path를 어떻게 나눴는지 전달할 수 있습니다.
- tombstone이 serialization 이후에도 살아남는다는 점은 이후 compaction 설명의 발판이 됩니다.
