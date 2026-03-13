# 02 Leader-Follower Replication — Series Map

append-only mutation log와 watermark 기반 incremental sync로 leader-follower replication을 구현합니다. 이 시리즈는 기존 초안의 말투를 따라가지 않고, 실제 코드와 검증 신호를 다시 읽으면서 판단이 어디서 바뀌는지에만 집중한다.

## 이 프로젝트가 답하는 질문

- 순차 offset을 갖는 mutation log를 유지해야 합니다.
- `put`과 `delete`가 복제돼야 합니다.

## 작업 산출물

- [_evidence-ledger.md](_evidence-ledger.md)
- [_structure-outline.md](_structure-outline.md)

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md) — 파일 구조와 테스트 이름으로 범위를 다시 잡는 구간
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md) — 핵심 invariant를 코드 조각으로 고정하는 구간
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md) — 실제 pass 신호와 남은 경계를 정리하는 구간

## 참조한 실제 파일

- `database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/src/leader_follower/core.py`
- `database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/tests/test_replication.py`
- `database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/README.md`
- `database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/problem/README.md`
- `database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/docs/README.md`
- `database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/src/leader_follower/__main__.py`

## 재검증 명령

```bash
PYTHONPATH=src .venv/bin/python -m pytest
PYTHONPATH=src .venv/bin/python -m leader_follower
```

## Git Anchor

- `2026-03-13 abeead6 docs: TRACK 1 에대한 blog/ 작업 1차 완료`
- `2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료`
