# Problem Guide

이 문서는 08 MVCC 프로젝트에서 “무엇을 구현해야 하는가”를 현재 기준으로 다시 설명합니다. 과거 과제군에서 출발한 아이디어는 남기되, 현재 레포에 없는 로컬 경로를 전제로 설명하지는 않습니다.

## 문제 핵심

- snapshot isolation 하에서 읽기 스냅샷과 write-write conflict를 관리해야 합니다.
- read-your-own-write를 보장해야 합니다.
- first-committer-wins conflict detection이 필요합니다.
- aborted version cleanup과 stale version GC가 동작해야 합니다.

## 이번 범위에서 일부러 뺀 것

- predicate locking, phantom read 제어, distributed transaction은 포함하지 않습니다.
- full SQL transaction manager나 lock table은 후속 확장 범위입니다.

## 제공 자료

- 이 프로젝트는 별도 starter artifact 없이 `problem/README.md` 자체가 요구사항 문서 역할을 합니다.

## 역사적 출처와 현재 재구성

- 원래 속한 학습 주제: MVCC
- 원래 구현 형태: JavaScript 기반 transaction-engine 과제로, version chain과 conflict check를 중심으로 구성돼 있었습니다.
- 현재 프로젝트에서의 재구성: 현재 레포에서는 snapshot visibility와 conflict 판정을 concept note와 테스트 흐름으로 더 분명히 연결했습니다.
- 원본 소스 트리는 현재 레포에 포함돼 있지 않으며, 이 문서는 현재 공개 레포 기준으로 다시 정리한 설명입니다.
