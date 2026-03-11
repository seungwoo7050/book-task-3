# Problem Guide

이 문서는 02 Leader-Follower Replication 프로젝트에서 “무엇을 구현해야 하는가”를 현재 기준으로 다시 설명합니다. 과거 과제군에서 출발한 아이디어는 남기되, 현재 레포에 없는 로컬 경로를 전제로 설명하지는 않습니다.

## 문제 핵심

- 순차 offset을 갖는 mutation log를 유지해야 합니다.
- `put`과 `delete`가 복제돼야 합니다.
- follower watermark 기반 incremental sync가 필요합니다.
- 같은 entry를 다시 받아도 결과가 깨지지 않는 idempotent apply가 필요합니다.

## 이번 범위에서 일부러 뺀 것

- automatic leader election과 consensus는 포함하지 않습니다.
- quorum write나 multi-leader replication은 다루지 않습니다.

## 제공 자료

- 이 프로젝트는 별도 starter artifact 없이 `problem/README.md` 자체가 요구사항 문서 역할을 합니다.

## 역사적 출처와 현재 재구성

- 원래 속한 학습 주제: Replication
- 원래 구현 형태: JavaScript 기반 distributed-cluster 과제로, leader/follower state sync를 작은 시뮬레이션으로 다루던 형태였습니다.
- 현재 프로젝트에서의 재구성: 현재 레포에서는 이후 shard routing과 capstone으로 이어질 수 있게 log shipping과 follower apply 의미를 더 분명히 설명합니다.
- 원본 소스 트리는 현재 레포에 포함돼 있지 않으며, 이 문서는 현재 공개 레포 기준으로 다시 정리한 설명입니다.
