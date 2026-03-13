# 02 Leader-Follower Replication — Series Map

이 시리즈의 핵심은 화려한 consensus가 아니다. `offset`과 `watermark` 두 숫자만으로 follower catch-up이 얼마나 멀리 갈 수 있는지를 확인하는 단계다.

## 이 프로젝트가 답하는 질문

- append-only log와 idempotent apply만으로 incremental replication이 성립하는가
- duplicate entry를 받은 follower가 왜 다시 망가지지 않는가

## 읽는 순서

1. [10-chronology-setup-and-surface.md](10-chronology-setup-and-surface.md)
2. [20-chronology-core-mechanics.md](20-chronology-core-mechanics.md)
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md)

## 참조한 실제 파일

- `python/ddia-distributed-systems/projects/02-leader-follower-replication/src/leader_follower/core.py`
- `python/ddia-distributed-systems/projects/02-leader-follower-replication/src/leader_follower/__main__.py`
- `python/ddia-distributed-systems/projects/02-leader-follower-replication/tests/test_replication.py`
- `python/ddia-distributed-systems/projects/02-leader-follower-replication/README.md`
- `python/ddia-distributed-systems/projects/02-leader-follower-replication/problem/README.md`
- `python/ddia-distributed-systems/projects/02-leader-follower-replication/docs/concepts/log-shipping.md`
- `python/ddia-distributed-systems/projects/02-leader-follower-replication/docs/concepts/idempotent-follower.md`
- `python/ddia-distributed-systems/projects/02-leader-follower-replication/pyproject.toml`

## 재검증 명령

```bash
cd python/ddia-distributed-systems/projects/02-leader-follower-replication
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m leader_follower
```

## Git Anchor

- `2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료`
- `2026-03-11 74d5b11 feat: add new project in database-systems`
