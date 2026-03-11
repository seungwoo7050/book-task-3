# Problem Guide

이 문서는 03 Mini LSM Store 프로젝트에서 “무엇을 구현해야 하는가”를 현재 기준으로 다시 설명합니다. 과거 과제군에서 출발한 아이디어는 남기되, 현재 레포에 없는 로컬 경로를 전제로 설명하지는 않습니다.

## 문제 핵심

- active memtable이 threshold를 넘으면 immutable swap 후 SSTable로 flush해야 합니다.
- read path는 active memtable, immutable memtable, newest SSTable부터 순서대로 조회해야 합니다.
- tombstone은 cross-level read에서도 삭제 의미를 유지해야 합니다.
- close 이후 re-open 시 기존 SSTable index를 다시 적재해야 합니다.

## 이번 범위에서 일부러 뺀 것

- background compaction과 concurrent flush는 다루지 않습니다.
- range query와 compression 같은 production 기능은 후속 확장 항목으로 남깁니다.

## 제공 자료

- 이 프로젝트는 별도 starter artifact 없이 `problem/README.md` 자체가 요구사항 문서 역할을 합니다.

## 역사적 출처와 현재 재구성

- 원래 속한 학습 주제: LSM Tree Core
- 원래 구현 형태: JavaScript 기반 단일 저장 엔진 과제였습니다.
- 현재 프로젝트에서의 재구성: Go 트랙에서는 memtable과 SSTable을 각각 선행 프로젝트로 분리한 뒤, 이 단계에서 orchestration을 다시 묶습니다.
- 원본 소스 트리는 현재 레포에 포함돼 있지 않으며, 이 문서는 현재 공개 레포 기준으로 다시 정리한 설명입니다.
