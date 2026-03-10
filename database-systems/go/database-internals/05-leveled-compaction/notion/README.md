# 학습 노트 안내

이 노트 묶음은 `05-leveled-compaction`을 처음부터 다시 만드는 사람을 위한 재현용 안내서입니다. 이 프로젝트는 05번 단계답게 규모는 작지만, merge 규칙, tombstone 처리, manifest 원자성까지 한 번에 드러나서 “읽고 그대로 다시 만든다”는 목적에 특히 적합합니다.

## 왜 05가 재현성에 좋은가
- 핵심 구현이 사실상 `../internal/compaction/compaction.go` 하나에 모여 있어 읽기 경로가 짧습니다.
- 테스트 4개가 각각 하나의 규칙을 거의 1:1로 검증합니다.
- 데모 출력이 결정적이라, 구현이 맞는지 눈으로도 바로 확인할 수 있습니다.

## 권장 재현 순서
1. `../problem/README.md`와 `../docs/concepts/merge-ordering.md`를 읽어 compaction이 해결하려는 문제를 먼저 맞춥니다.
2. `../internal/sstable/sstable.go`를 열어 입력과 출력이 어떤 파일 포맷을 쓰는지 확인합니다.
3. `../internal/compaction/compaction.go`에서 `KWayMerge`, `CompactL0ToL1`, `SaveManifest` 순서로 읽습니다.
4. `../tests/compaction_test.go`를 보며 규칙별 기대 결과를 정리합니다.
5. `../cmd/leveled-compaction/main.go`를 실행해 실제 출력이 기대와 맞는지 확인합니다.

## 이번 노트가 담는 것
- `00-problem-framing.md`: 재현 목표, 입력 데이터셋, 성공 기준, 범위 밖 항목을 정리합니다.
- `01-approach-log.md`: 어떤 순서로 구현을 쌓으면 재현이 쉬운지 단계별로 설명합니다.
- `02-debug-log.md`: 가장 자주 틀리는 지점과 그때 어떤 출력이 나오는지를 기록합니다.
- `03-retrospective.md`: 왜 이 단계가 재현성 학습에 좋은지, 어디까지가 학습용 단순화인지 정리합니다.
- `04-knowledge-index.md`: 용어, 핵심 파일, 바로 실행할 명령, 기대 출력, 다음 단계 연결점을 모아 둡니다.

## 바로 확인할 명령
```bash
cd go/database-internals/05-leveled-compaction
go test ./... -run 'TestKWayMergeKeepsNewerValue|TestCompactL0ToL1|TestManifestRoundTrip' -v
go run ./cmd/leveled-compaction
```

## 기대 출력
```text
apple=red
banana=gold
pear=green
```

## 검증 앵커
- 테스트: `TestKWayMergeKeepsNewerValue`, `TestKWayMergeDropsTombstonesAtDeepestLevel`, `TestCompactL0ToL1`, `TestManifestRoundTrip`
- 데모 경로: `../cmd/leveled-compaction/main.go`
- 개념 문서: `../docs/concepts/manifest-atomicity.md`, `../docs/concepts/merge-ordering.md`

- 이전 장문 기록은 `../notion-archive/`에 보존돼 있고, 여기서는 재현에 바로 필요한 정보만 남깁니다.
