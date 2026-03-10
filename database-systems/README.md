# DB Study Archive

이 저장소는 데이터베이스 내부(storage internals)와 분산 시스템(distributed systems)을 함께 공부하는 학습 아카이브입니다. 목표는 완성품을 전시하는 것이 아니라, 구현을 따라가며 개념을 자기 것으로 만들고, 그 결과를 바탕으로 더 나은 공개용 포트폴리오 레포를 설계할 수 있게 돕는 것입니다.

## 이 레포로 배우는 것

- 단일 노드 저장 엔진에서 memtable, SSTable, WAL, compaction, buffer pool, MVCC가 어떻게 이어지는지 배웁니다.
- 분산 시스템에서 RPC, replication, sharding, consensus-lite, clustered KV 흐름이 어떻게 연결되는지 배웁니다.
- 각 프로젝트를 `문제 해석 → 구현 → 개념 문서 → 학습 노트` 순서로 읽으면서, 단순 정답 복제보다 설계 판단을 먼저 이해하도록 돕습니다.

## 어디서 시작하면 좋은가

| 시작점 | 추천 대상 | 이유 |
| --- | --- | --- |
| [python/README.md](python/README.md) | 저장 엔진과 분산 시스템을 처음 연결해 보는 학습자 | 프로젝트 수가 더 적고, self-contained한 입문 경로로 재구성돼 있습니다. |
| [go/README.md](go/README.md) | 세분화된 프로젝트와 심화 주제까지 모두 보고 싶은 학습자 | Go 트랙은 전체 커리큘럼의 정본(superset)입니다. |
| [docs/README.md](docs/README.md) | 왜 이런 순서로 재구성했는지 먼저 알고 싶은 사람 | 커리큘럼 감사, 교차 매핑, 문서 스타일 규칙을 한 번에 볼 수 있습니다. |

## 디렉터리 안내

- [go/README.md](go/README.md): 전체 커리큘럼과 심화 분산 주제를 포함한 정본 트랙
- [python/README.md](python/README.md): 더 적은 프로젝트 수로 핵심 흐름을 먼저 익히는 입문 트랙
- [docs/README.md](docs/README.md): 커리큘럼 설계 근거, 언어 간 대응표, 문서 계약
- 각 프로젝트의 `problem/`: 문제 해석과 제공 자료
- 각 프로젝트의 `docs/`: 개념 메모와 참고자료 설명
- 각 프로젝트의 `notion/`: 현재 공개용 학습 노트
- 각 프로젝트의 `notion-archive/`: 이전 문서 묶음을 보존한 아카이브

## 추천 학습 루프

1. 루트 README와 트랙 README로 전체 경로를 먼저 파악합니다.
2. 프로젝트에 들어가면 `problem/README.md`를 먼저 읽고, 무엇을 구현해야 하는지 스스로 설명해 봅니다.
3. `docs/README.md`와 개념 노트로 핵심 용어를 맞춘 뒤 구현과 테스트를 읽습니다.
4. `notion/` 문서에서 설계 판단, 실패 포인트, 회고를 확인합니다.
5. 마지막으로 “이 프로젝트를 내 포트폴리오에 옮긴다면 무엇을 남길까?”를 각 README의 마지막 섹션으로 정리합니다.

## 빠른 검증 시작

```bash
cd python/database-internals/01-mini-lsm-store
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip pytest
PYTHONPATH=src python -m pytest
PYTHONPATH=src python -m mini_lsm_store

deactivate
cd ../../../go/database-internals/01-memtable-skiplist
GOWORK=off go test ./...
GOWORK=off go run ./cmd/skiplist-demo
```

## 출처와 공개 정책

- 과거 과제군에서 가져온 아이디어는 각 `problem/README.md`와 `docs/references/README.md`에 역사적 출처 설명으로 남겨 둡니다.
- 과거 로컬 경로를 현재 레포 구조처럼 약속하지는 않습니다. 현재 레포에 없는 소스 트리는 설명형 provenance로만 다룹니다.
- `notion/`은 공개 가능한 학습 노트이자 레포 백업 문서입니다. 이전 세대 문서는 `notion-archive/`에 따로 보존합니다.
