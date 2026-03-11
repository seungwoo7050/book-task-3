# Problem Guide

이 문서는 05 Leveled Compaction 프로젝트에서 “무엇을 구현해야 하는가”를 현재 기준으로 다시 설명합니다. 과거 과제군에서 출발한 아이디어는 남기되, 현재 레포에 없는 로컬 경로를 전제로 설명하지는 않습니다.

## 문제 핵심

- 입력 source 배열에서 newer-first 우선순위를 유지한 k-way merge를 수행해야 합니다.
- deepest level일 때만 tombstone을 제거해야 합니다.
- 새 SSTable 생성 후 manifest를 atomic write로 갱신해야 합니다.
- compaction이 끝나면 이전 입력 파일을 정리해야 합니다.

## 이번 범위에서 일부러 뺀 것

- background compaction scheduler와 multi-level balancing 정책은 포함하지 않습니다.
- compression과 block cache는 후속 확장 범위로 남깁니다.

## 제공 자료

- 이 프로젝트는 별도 starter artifact 없이 `problem/README.md` 자체가 요구사항 문서 역할을 합니다.

## 역사적 출처와 현재 재구성

- 원래 속한 학습 주제: Compaction
- 원래 구현 형태: JavaScript 기반 storage-engine compaction 과제로, merge와 level manager가 분리돼 있었습니다.
- 현재 프로젝트에서의 재구성: 현재 레포에서는 Go SSTable 구현을 직접 사용해 compaction과 manifest atomicity를 같은 흐름에서 설명합니다.
- 원본 소스 트리는 현재 레포에 포함돼 있지 않으며, 이 문서는 현재 공개 레포 기준으로 다시 정리한 설명입니다.
