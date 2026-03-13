# Database Systems Study Archive

이 레포는 `무슨 문제를 풀었는가`, `내 해법이 무엇인가`, `어떻게 다시 검증하는가`를 바로 찾을 수 있게 정리한 데이터베이스 시스템 학습 아카이브입니다.

## 이 레포가 푸는 문제

- 단일 노드 저장 엔진에서 memtable, SSTable, WAL, compaction, buffer pool, MVCC가 어떤 순서와 책임 분리로 이어지는가
- 분산 저장소에서 RPC, replication, sharding, consensus-lite, clustered KV, quorum consistency, leader election, failure handling을 어떤 실험 단위로 나눠 이해할 것인가
- 같은 주제를 Python 입문 경로와 Go 정본 경로로 어떻게 대응해 읽을 것인가

## 추천 시작 경로

- [Python Track](python/README.md): 프로젝트 수를 줄인 입문 경로입니다. 저장 엔진과 분산 시스템의 큰 흐름을 먼저 잡고 싶을 때 시작합니다.
- [Go Track](go/README.md): 더 잘게 나눈 정본 경로입니다. 자료구조, 포맷, recovery, compaction, consensus-lite를 더 세밀하게 추적하고 싶을 때 시작합니다.
- [전체 카탈로그](docs/catalog/project-catalog.md): 언어, 트랙, 문제, 내 해법, 검증 명령을 한 번에 보는 단일 인덱스입니다.
- [문서 인덱스](docs/README.md): 커리큘럼 설계 근거, 언어 대응표, 문서 정책을 확인하는 위치입니다.
- [Blog Index](blog/README.md): `src/`, `tests`, `README`, 실제 재검증 CLI만으로 다시 읽은 source-first blog 시리즈입니다.

## 대표 프로젝트

- [01 Mini LSM Store](python/database-internals/projects/01-mini-lsm-store/README.md): write path와 read path를 가장 적은 구성으로 한 번에 연결하는 저장 엔진 입문입니다.
- [04 WAL Recovery](go/database-internals/projects/04-wal-recovery/README.md): append-before-apply 순서로 durability와 crash recovery를 분리해 검증합니다.
- [05 Clustered KV Capstone](go/ddia-distributed-systems/projects/05-clustered-kv-capstone/README.md): routing, replication, local store를 하나의 write pipeline으로 묶는 분산 저장소 캡스톤입니다.
- [08 Failure-Injected Log Replication](go/ddia-distributed-systems/projects/08-failure-injected-log-replication/README.md): partial failure 아래에서 retry와 convergence를 실험하는 심화 슬롯입니다.

## 빠른 검증

```bash
cd python/database-internals/projects/01-mini-lsm-store
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip pytest
PYTHONPATH=src python -m pytest
PYTHONPATH=src python -m mini_lsm_store

deactivate
cd ../../../../go
go test ./database-internals/projects/01-memtable-skiplist/...
go run ./database-internals/projects/01-memtable-skiplist/cmd/skiplist-demo
```

## 읽는 규칙

- 루트나 트랙 README에서는 먼저 `문제 / 내 해법 / 검증`을 확인하고, 더 자세한 세부는 개별 프로젝트로 내려갑니다.
- 프로젝트를 읽을 때는 `README -> problem/README -> docs/README -> 구현과 tests -> notion/README` 순서를 기본 경로로 삼습니다.
- source-first 재구성 흐름이 필요하면 `blog/README.md`와 각 프로젝트의 `00-series-map.md`로 이동합니다.
- 전역 문구와 검증 명령의 기준점은 [docs/catalog/project-catalog.md](docs/catalog/project-catalog.md)입니다.
- 긴 커리큘럼 설명은 `docs/`, 현재 학습 로그는 `notion/`, 이전 장문 기록은 `notion-archive/`에 둡니다.
