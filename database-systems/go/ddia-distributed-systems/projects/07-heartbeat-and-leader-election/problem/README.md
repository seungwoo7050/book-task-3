# Problem Guide

이 문서는 07 Heartbeat and Leader Election 프로젝트에서 “무엇을 구현해야 하는가”를 현재 기준으로 다시 설명합니다.

## 문제 핵심

- leader가 주기적으로 heartbeat를 보내야 합니다.
- follower는 heartbeat silence가 길어지면 leader를 suspect해야 합니다.
- election은 term을 올리고 majority vote를 받아야만 leader가 될 수 있습니다.
- higher term을 본 old leader는 즉시 follower로 step-down해야 합니다.
- 이 모든 흐름은 tick 기반 결정적 시뮬레이션으로 재현돼야 합니다.

## 이번 범위에서 일부러 뺀 것

- log replication과 commit rule은 포함하지 않습니다.
- randomized timeout, network partition, pre-vote도 포함하지 않습니다.
- membership change와 lease-based leader validation도 포함하지 않습니다.

## 제공 자료

- 별도 starter artifact는 없고, `problem/README.md` 자체가 요구사항 문서 역할을 합니다.

## 역사적 출처와 현재 재구성

- 원래 속한 학습 주제: failure detector, heartbeat, leader election
- 원래 구현 형태: consensus 설명에서 election 일부만 발췌하거나, production Raft 구현 안에 섞여 나오는 경우가 많았습니다.
- 현재 프로젝트에서의 재구성: `database-systems` Go 분산 트랙에서는 quorum consistency 다음 단계로 leader authority 문제만 분리해, full log replication 이전에 election을 따로 이해하게 만듭니다.
- 원본 소스 트리는 현재 레포에 포함돼 있지 않으며, 이 문서는 현재 공개 레포 기준으로 다시 정리한 설명입니다.
