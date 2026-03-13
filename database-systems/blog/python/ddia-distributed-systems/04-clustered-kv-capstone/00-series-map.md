# 04 Clustered KV Capstone — Series Map

이 시리즈는 앞의 세 프로젝트를 실제 write pipeline 하나로 묶는 단계다. routing, replication, disk persistence, API boundary가 따로 존재하는 게 아니라 `Cluster` 안에서 순서대로 연결된다.

## 이 프로젝트가 답하는 질문

- shard 선택 -> leader append -> follower sync를 어디까지 코어에서 책임질 것인가
- FastAPI는 코어를 감추는 계층인가, 아니면 결과를 그대로 노출하는 얇은 경계인가

## 읽는 순서

1. [10-chronology-setup-and-surface.md](10-chronology-setup-and-surface.md)
2. [20-chronology-core-mechanics.md](20-chronology-core-mechanics.md)
3. [30-chronology-integration-and-tradeoffs.md](30-chronology-integration-and-tradeoffs.md)
4. [40-chronology-verification-and-boundaries.md](40-chronology-verification-and-boundaries.md)

## 참조한 실제 파일

- `python/ddia-distributed-systems/projects/04-clustered-kv-capstone/src/clustered_kv/core.py`
- `python/ddia-distributed-systems/projects/04-clustered-kv-capstone/src/clustered_kv/app.py`
- `python/ddia-distributed-systems/projects/04-clustered-kv-capstone/src/clustered_kv/__main__.py`
- `python/ddia-distributed-systems/projects/04-clustered-kv-capstone/tests/test_clustered_kv.py`
- `python/ddia-distributed-systems/projects/04-clustered-kv-capstone/README.md`
- `python/ddia-distributed-systems/projects/04-clustered-kv-capstone/problem/README.md`
- `python/ddia-distributed-systems/projects/04-clustered-kv-capstone/docs/concepts/static-topology.md`
- `python/ddia-distributed-systems/projects/04-clustered-kv-capstone/docs/concepts/replicated-write-pipeline.md`
- `python/ddia-distributed-systems/projects/04-clustered-kv-capstone/pyproject.toml`

## 재검증 명령

```bash
cd python/ddia-distributed-systems/projects/04-clustered-kv-capstone
python3 -m pip install -e '.[dev]'
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m clustered_kv
```

## Git Anchor

- `2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료`
- `2026-03-11 74d5b11 feat: add new project in database-systems`
