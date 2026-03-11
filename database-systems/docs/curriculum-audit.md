# Curriculum Audit

## 이 저장소가 겨냥하는 학습 목표

이 레포는 두 개의 큰 흐름을 한 저장소 안에서 연결해 배우도록 설계돼 있습니다.

- `Database Internals`: memtable, SSTable, WAL, compaction, buffer pool, MVCC
- `DDIA Distributed Systems`: RPC, replication, sharding, consensus-lite, clustered KV, quorum consistency, leader election, failure-injected replication

핵심 목표는 “단일 노드 저장 엔진”과 “네트워크로 연결된 분산 저장소”를 별개의 주제로 끝내지 않고, 구현 관점에서 하나의 학습 경로로 묶는 것입니다.

## 왜 재구성이 필요했는가

과거 과제군은 주제 자체는 좋았지만, 학습 순서와 프로젝트 크기 면에서 몇 가지 문제가 있었습니다.

- 저장 엔진 초반부가 한 슬롯에 너무 많이 묶여 있어 입문자가 진입하기 어려웠습니다.
- 분산 파트는 개별 시뮬레이션으로 끝나기 쉬워, 실제 저장 엔진과 연결되는 마지막 단계가 약했습니다.
- 일부 설명은 과거 로컬 경로와 스크립트 존재를 전제로 쓰여 있어 현재 기준으로는 정확하지 않았습니다.

## 현재 커리큘럼이 해결한 것

### Python-first 경로

- 프로젝트 수를 줄여 핵심 흐름을 더 빨리 잡도록 만들었습니다.
- memtable + SSTable + mini LSM store를 하나의 시작 프로젝트로 접었습니다.
- Raft는 제외하고, clustered KV capstone까지 이어지는 입문용 분산 경로를 제공합니다.

### Go-second 경로

- 저장 엔진 초반부를 더 세밀하게 쪼개어 자료구조, 파일 포맷, orchestration을 단계별로 다룹니다.
- Raft-lite와 compaction 같은 심화 슬롯을 포함합니다.
- clustered KV capstone 뒤에는 quorum consistency, heartbeat/election, failure-injected replication 같은 Go-only deep dive가 이어집니다.
- 전체 커리큘럼의 정본(superset) 역할을 맡습니다.

## 이 커리큘럼이 학생에게 주는 장점

- 같은 주제를 Python과 Go 두 관점에서 비교할 수 있습니다.
- 문제 문서와 개념 문서, 학습 노트가 분리되어 있어 “정답 복사”보다 “판단 근거 읽기”가 쉬워집니다.
- 각 프로젝트 README가 포트폴리오 확장 힌트를 포함하므로, 학습 레포를 그대로 답안집으로 공개하는 대신 자신의 프로젝트로 재구성할 수 있습니다.

## 의도적으로 남겨 둔 빈칸

이 레포는 모든 DBMS 주제를 한 번에 다루지 않습니다. 다음 주제는 후속 확장 후보로 남깁니다.

- query executor, planner, B-Tree 같은 상위 DBMS 주제
- dynamic membership, snapshotting, deployment automation 같은 운영 심화 주제
- production-grade observability, benchmarking, large-scale chaos automation

이 빈칸은 단점이 아니라 다음 포트폴리오 주제를 설계할 여지를 남기는 장치입니다.
