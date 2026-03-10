# Problem Guide

이 문서는 02 SSTable Format 프로젝트에서 “무엇을 구현해야 하는가”를 현재 기준으로 다시 설명합니다. 과거 과제군에서 출발한 아이디어는 남기되, 현재 레포에 없는 로컬 경로를 전제로 설명하지는 않습니다.

## 문제 핵심

- data section은 key 오름차순 record의 연속 바이트 배열이어야 합니다.
- index section은 `(key, offset)` 쌍을 저장해 point lookup 시작 위치를 알려야 합니다.
- footer는 data/index section 크기를 기록해야 합니다.
- tombstone은 value length sentinel 같은 명시적 표현으로 보존해야 합니다.
- file reopen 이후에도 index load와 lookup이 동작해야 합니다.

## 이번 범위에서 일부러 뺀 것

- compression, block cache, range tombstone은 포함하지 않습니다.
- multi-level manifest 관리와 compaction 연결은 다음 프로젝트로 넘깁니다.

## 제공 자료

- 이 프로젝트는 별도 starter artifact 없이 `problem/README.md` 자체가 요구사항 문서 역할을 합니다.

## 역사적 출처와 현재 재구성

- 원래 속한 학습 주제: LSM Tree Core
- 원래 구현 형태: JavaScript 기반 저장 엔진 과제 안에서 memtable과 함께 설명되던 SSTable 포맷 파트였습니다.
- 현재 프로젝트에서의 재구성: 현재 레포에서는 file format 자체를 별도 프로젝트로 떼어, memtable과 flush orchestration을 분리해 이해할 수 있게 했습니다.
- 원본 소스 트리는 현재 레포에 포함돼 있지 않으며, 이 문서는 현재 공개 레포 기준으로 다시 정리한 설명입니다.
