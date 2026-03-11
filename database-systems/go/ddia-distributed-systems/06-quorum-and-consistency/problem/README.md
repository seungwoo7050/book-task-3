# Problem Guide

이 문서는 06 Quorum and Consistency 프로젝트에서 “무엇을 구현해야 하는가”를 현재 기준으로 다시 설명합니다.

## 문제 핵심

- replica 3개를 가진 versioned register를 구현해야 합니다.
- `N/W/R` 정책에 따라 write quorum과 read quorum을 검증해야 합니다.
- write는 quorum이 확보될 때만 version을 올려야 합니다.
- read는 responder 집합 안에서 가장 높은 version을 골라 반환해야 합니다.
- `W + R > N`과 `W + R <= N`의 차이를 고정 fixture로 재현해야 합니다.

## 이번 범위에서 일부러 뺀 것

- read repair, hinted handoff, anti-entropy는 포함하지 않습니다.
- vector clock, sibling merge, multi-key transaction도 포함하지 않습니다.
- membership change와 failure detector는 다음 프로젝트로 남깁니다.

## 제공 자료

- 별도 starter artifact는 없고, `problem/README.md` 자체가 요구사항 문서 역할을 합니다.

## 역사적 출처와 현재 재구성

- 원래 속한 학습 주제: quorum consistency, sloppy quorum, Dynamo-style replica reads
- 원래 구현 형태: 교재와 강의에서 read/write quorum을 도식으로 설명하는 경우가 많았고, 작은 register 실습은 보조 예제로만 다뤄졌습니다.
- 현재 프로젝트에서의 재구성: `database-systems` Go 분산 트랙에서는 replication 이후, leader election 이전 단계로 두어 consistency trade-off를 먼저 분리해 설명합니다.
- 원본 소스 트리는 현재 레포에 포함돼 있지 않으며, 이 문서는 현재 공개 레포 기준으로 다시 정리한 설명입니다.
