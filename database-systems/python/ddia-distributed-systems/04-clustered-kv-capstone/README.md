# 04 Clustered KV Capstone

## Summary

정적 shard topology와 정적 leader 배치를 가진 작은 clustered KV store를 구현해서, shard routing, leader-follower replication, disk-backed node store를 한 흐름으로 연결한다. Python 트랙에서는 FastAPI를 외부 서비스 경계에만 사용한다.

## Status

- 상태: `verified`
- 구현 언어: `Python 3.14`
- 범위: static topology, synchronous follower catch-up, disk-backed node store, FastAPI boundary
- 의도적 축소: Go 트랙의 Raft/합의 심화는 포함하지 않는다.

## Commands

```bash
python3 -m pip install -e .[dev]
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m clustered_kv
```
