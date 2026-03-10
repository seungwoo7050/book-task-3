# Problem Guide

이 문서는 07 Buffer Pool 프로젝트에서 “무엇을 구현해야 하는가”를 현재 기준으로 다시 설명합니다. 과거 과제군에서 출발한 아이디어는 남기되, 현재 레포에 없는 로컬 경로를 전제로 설명하지는 않습니다.

## 문제 핵심

- page id로 file path와 page number를 안정적으로 분리해야 합니다.
- fetch 시 cache hit면 pin count를 올리고, miss면 disk read 후 캐시에 올려야 합니다.
- dirty page는 eviction이나 explicit flush 때 write-back해야 합니다.
- pinned page는 eviction하면 안 됩니다.

## 이번 범위에서 일부러 뺀 것

- concurrent latch, lock manager, asynchronous IO는 포함하지 않습니다.
- buffer pool을 B-tree나 query executor와 연결하는 단계는 후속 범위로 남깁니다.

## 제공 자료

- 이 프로젝트는 별도 starter artifact 없이 `problem/README.md` 자체가 요구사항 문서 역할을 합니다.

## 역사적 출처와 현재 재구성

- 원래 속한 학습 주제: Buffer Pool
- 원래 구현 형태: JavaScript 기반 transaction-engine 과제로, LRU cache와 buffer pool manager가 함께 제공되던 형태였습니다.
- 현재 프로젝트에서의 재구성: 현재 레포에서는 page identity, replacer, dirty flush를 Go 패키지 구조 안에서 더 명확히 분리했습니다.
- 원본 소스 트리는 현재 레포에 포함돼 있지 않으며, 이 문서는 현재 공개 레포 기준으로 다시 정리한 설명입니다.
