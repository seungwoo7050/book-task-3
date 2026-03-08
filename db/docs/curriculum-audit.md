# Curriculum Audit

## 원래 저장소가 배우려던 것

`legacy/README.md`와 모듈 문서를 보면 이 저장소는 두 축을 함께 배우려 했다.

- `Database Internals`: LSM-Tree, SSTable, WAL, compaction, buffer pool
- `Designing Data-Intensive Applications`: RPC, replication, sharding, Raft

즉 목표는 "디스크에 쓰는 단일 노드 저장 엔진"에서 "네트워크로 묶인 분산 키값 저장소"까지의 학습 흐름을 직접 구현으로 따라가는 것이다.

## 레거시 프로젝트셋 평가

### 강점

- 10개 모듈 모두 `problem/docs/solve/devlog`를 갖고 있어서 provenance 추적이 쉽다.
- Node.js 테스트 스위트는 현재 기준 대부분 통과한다.
- 스토리지, 트랜잭션, 분산 세 영역이 명시적으로 구분되어 있다.

### 약점

- `storage-engine/lsm-tree-core`는 SkipList, SSTable, flush path를 한 슬롯에 몰아 넣어 학습 단위가 너무 크다.
- 분산 파트는 각 모듈이 개별 시뮬레이션으로 끝나서 실제 저장 엔진과 연결되는 다리 프로젝트가 없다.
- `legacy/package.json`의 `start:cluster`, `benchmark`는 실제 파일이 없어 루트 실행 계약이 깨져 있다.
- `legacy/common` 의존이 여러 모듈에 퍼져 있지만, 학습 관점의 공용 라이브러리 표면은 명시돼 있지 않다.

## 새 커리큘럼이 필요한 이유

### 분할

- `lsm-tree-core`는 `memtable-skiplist`, `sstable-format`, `mini-lsm-store`로 나눈다.
- 이유: 자료구조, 저장 형식, 상위 orchestration을 각각 독립 검증 가능한 슬롯으로 만들어야 학습 회수율이 높다.

### 유지

- `wal-recovery`, `leveled-compaction`, `index-filter`, `buffer-pool`, `mvcc`, `rpc-framing`, `leader-follower-replication`, `shard-routing`, `raft-lite`는 개념 단위가 이미 분명하므로 유지한다.

### 추가

- `clustered-kv-capstone`을 새로 넣는다.
- 이유: 레거시에는 RPC, replication, sharding이 실제 저장 엔진과 한 프로세스 흐름으로 연결되는 통합 프로젝트가 없다.

## 새 순서

### Database Internals

1. MemTable SkipList
2. SSTable Format
3. Mini LSM Store
4. WAL Recovery
5. Leveled Compaction
6. Index Filter
7. Buffer Pool
8. MVCC

### DDIA Distributed Systems

1. RPC Framing
2. Leader-Follower Replication
3. Shard Routing
4. Raft Lite
5. Clustered KV Capstone

## Historical Drift

- `[검증됨]` 2026-03-07 기준 `legacy/package.json`의 `start:cluster`는 `distributed-cluster/rpc-network/solve/solution/cluster-bootstrap.js`를 가리키지만 파일이 없다.
- `[검증됨]` 같은 날짜 기준 `benchmark`는 `scripts/benchmark.js`를 가리키지만 파일이 없다.
- 따라서 새 정본은 루트 스크립트가 아니라 프로젝트 로컬 명령만 약속한다.

## Migration Outcome

- 2026-03-07 기준 `study/`의 13개 프로젝트가 모두 Go 구현과 테스트, 데모, 개념 문서를 갖는 `verified` 상태로 정리되었다.
- `clustered-kv-capstone`은 레거시 공백을 메우는 신규 프로젝트로 추가되어 shard routing, replication, disk-backed node store를 한 흐름으로 묶는다.
