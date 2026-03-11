# Problem Guide

이 문서는 08 Failure-Injected Log Replication 프로젝트에서 “무엇을 구현해야 하는가”를 현재 기준으로 다시 설명합니다.

## 문제 핵심

- single leader가 append-only log를 가지고 follower에게 entry를 보낼 수 있어야 합니다.
- 메시지는 `append`와 `ack` 두 종류로 명시돼야 합니다.
- 네트워크 하네스는 drop, duplicate, pause를 스크립트로 주입할 수 있어야 합니다.
- leader는 retry로 lagging follower를 따라잡게 만들어야 합니다.
- commit index는 quorum ack를 기준으로만 올라가야 합니다.

## 이번 범위에서 일부러 뺀 것

- full Raft term과 vote rule은 포함하지 않습니다.
- rebalancing, dynamic membership, snapshotting도 포함하지 않습니다.
- cross-shard routing이나 disk persistence는 다루지 않습니다.

## 제공 자료

- 별도 starter artifact는 없고, `problem/README.md` 자체가 요구사항 문서 역할을 합니다.

## 역사적 출처와 현재 재구성

- 원래 속한 학습 주제: log replication, partial failure, retry, idempotency
- 원래 구현 형태: 교재에서는 replication 흐름과 failure mode를 서술형으로 설명하는 경우가 많고, 실제 구현은 production consensus 코드 안에 섞여 있습니다.
- 현재 프로젝트에서의 재구성: `database-systems` Go 분산 트랙에서는 election 다음 단계로 두어, leader authority가 있다고 가정한 뒤 retry, duplicate handling, quorum commit만 따로 재현합니다.
- 원본 소스 트리는 현재 레포에 포함돼 있지 않으며, 이 문서는 현재 공개 레포 기준으로 다시 정리한 설명입니다.
