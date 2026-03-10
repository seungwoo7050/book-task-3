# Problem Guide

이 문서는 03 Shard Routing 프로젝트에서 “무엇을 구현해야 하는가”를 현재 기준으로 다시 설명합니다. 과거 과제군에서 출발한 아이디어는 남기되, 현재 레포에 없는 로컬 경로를 전제로 설명하지는 않습니다.

## 문제 핵심

- deterministic consistent hash ring을 구현해야 합니다.
- batch routing이 가능해야 합니다.
- add/remove 이후 reassignment count를 계산해야 합니다.
- empty ring, single node, multi-node 분산을 검증해야 합니다.

## 이번 범위에서 일부러 뺀 것

- dynamic membership protocol과 gossip은 포함하지 않습니다.
- 실제 데이터 이동과 rebalancing execution은 capstone 이후 확장 범위입니다.

## 제공 자료

- 이 프로젝트는 별도 starter artifact 없이 `problem/README.md` 자체가 요구사항 문서 역할을 합니다.

## 역사적 출처와 현재 재구성

- 원래 속한 학습 주제: Sharding
- 원래 구현 형태: JavaScript 기반 distributed-cluster 과제로, consistent hashing과 redistribution 측정에 집중한 형태였습니다.
- 현재 프로젝트에서의 재구성: 현재 레포에서는 capstone 앞 단계로 배치해, shard routing이 실제 write path와 어떻게 이어질지 예고하도록 구성했습니다.
- 원본 소스 트리는 현재 레포에 포함돼 있지 않으며, 이 문서는 현재 공개 레포 기준으로 다시 정리한 설명입니다.
