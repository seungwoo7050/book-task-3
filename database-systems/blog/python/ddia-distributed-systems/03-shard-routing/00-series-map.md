# 03 Shard Routing — Series Map

이 시리즈는 "어느 노드로 보낼까"보다 "노드 수가 바뀌어도 얼마나 덜 흔들릴까"를 먼저 본다. consistent hash ring과 virtual node는 정답이 아니라, 재배치 비용을 관리하려는 선택이다.

## 이 프로젝트가 답하는 질문

- modulo routing이 아닌 ring 기반 routing이 membership 변경에서 얼마나 유리한가
- `moved_keys`를 통해 재배치 비용을 수치로 볼 수 있는가

## 읽는 순서

1. [10-chronology-setup-and-surface.md](10-chronology-setup-and-surface.md)
2. [20-chronology-core-mechanics.md](20-chronology-core-mechanics.md)
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md)

## 참조한 실제 파일

- `python/ddia-distributed-systems/projects/03-shard-routing/src/shard_routing/core.py`
- `python/ddia-distributed-systems/projects/03-shard-routing/src/shard_routing/__main__.py`
- `python/ddia-distributed-systems/projects/03-shard-routing/tests/test_shard_routing.py`
- `python/ddia-distributed-systems/projects/03-shard-routing/README.md`
- `python/ddia-distributed-systems/projects/03-shard-routing/problem/README.md`
- `python/ddia-distributed-systems/projects/03-shard-routing/docs/concepts/virtual-nodes.md`
- `python/ddia-distributed-systems/projects/03-shard-routing/docs/concepts/rebalance-accounting.md`
- `python/ddia-distributed-systems/projects/03-shard-routing/pyproject.toml`

## 재검증 명령

```bash
cd python/ddia-distributed-systems/projects/03-shard-routing
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m shard_routing
```

## Git Anchor

- `2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료`
- `2026-03-11 74d5b11 feat: add new project in database-systems`
