# 04 Clustered KV Capstone 시리즈 맵

이 시리즈는 DDIA Distributed Systems 트랙의 4번째 프로젝트 `04 Clustered KV Capstone`를 따라간다. 정적 shard topology와 정적 leader 배치를 가진 작은 clustered KV store로 routing, replication, disk-backed storage를 한 흐름으로 연결합니다. 기능 목록보다 먼저, 어떤 순서로 경계를 고정했는지 읽는 쪽에 무게를 두었다.

## 먼저 보고 갈 질문

- key를 shard로 라우팅하고 shard별 leader/follower group을 선택해야 합니다.
- leader write가 log-backed 또는 disk-backed store에 기록돼야 합니다.

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md) — 테스트 이름과 파일 배치부터 훑으면서 문제의 테두리를 다시 좁히는 글
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md) — 핵심 함수와 상태 전이에서 invariant가 실제로 어디서 잠기는지 따라가는 글
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md) — 테스트와 demo를 다시 돌려 약속 범위와 남는 한계를 정리하는 글

## 재검증 명령

```bash
PYTHONPATH=src .venv/bin/python -m pytest
PYTHONPATH=src .venv/bin/python -m clustered_kv
```

## 이번 시리즈가 근거로 삼은 파일

- `database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/src/clustered_kv/core.py`
- `database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/tests/test_clustered_kv.py`
- `database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/README.md`
- `database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/problem/README.md`
- `database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/docs/README.md`
- `database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/src/clustered_kv/__main__.py`

## 보조 메모

작업 메모가 꼭 필요할 때만 [_evidence-ledger.md](_evidence-ledger.md)와 [_structure-outline.md](_structure-outline.md)를 보면 된다. 공개 시리즈는 `00 -> 10 -> 20 -> 30`만 따라가면 충분하다.

## Git Anchor

- `2026-03-13 abeead6 docs: TRACK 1 에대한 blog/ 작업 1차 완료`
- `2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료`
