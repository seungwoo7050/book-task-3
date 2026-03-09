# Problem Framing

겹치는 L0 SSTable 여러 개를 읽어서 최신 값이 남도록 병합하고, 결과를 L1 SSTable 하나로 재작성한다. compaction 이후에는 manifest와 파일 집합이 서로 어긋나지 않아야 하며, deepest level일 때만 tombstone을 제거할 수 있다.

## Success Criteria

- 입력 source 배열에서 newer-first 우선순위를 유지한 `k-way merge`
- L2가 비어 있을 때만 tombstone 제거
- 새 L1 SSTable 생성 후 manifest를 atomic write로 갱신
- compaction이 끝나면 이전 입력 파일이 제거됨

## Source Provenance

- 원본 문제: `legacy/storage-engine/compaction/problem/README.md`
- 원본 테스트 의미: `legacy/storage-engine/compaction/solve/test/merge.test.js`
- 원본 테스트 의미: `legacy/storage-engine/compaction/solve/test/level-manager.test.js`
- 원본 구현 참고: `legacy/storage-engine/compaction/solve/solution/merge.js`
- 원본 구현 참고: `legacy/storage-engine/compaction/solve/solution/level-manager.js`

## Normalization Notes

- JS의 `SSTable` 의존성은 이 프로젝트 내부 Go 구현으로 치환했다.
- 레거시의 설명을 따라 `sources[0]`을 newest로 해석하되, 실제 L0 file list는 flush 순서라서 compaction 시 reverse 처리한다.
- manifest는 JSON 유지하되 저장 방식은 `fileio.AtomicWrite`로 정규화했다.
