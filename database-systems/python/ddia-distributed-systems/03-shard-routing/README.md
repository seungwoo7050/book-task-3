# 03 Shard Routing

## Summary

virtual node를 가진 consistent hash ring으로 key를 node에 배치하고, node 추가/제거 시 얼마나 적은 key만 재배치되는지 측정한다.

## Status

- 상태: `verified`
- 구현 언어: `Python 3.14`
- 범위: consistent hash ring, router, reassignment accounting

## Commands

```bash
python3 -m pip install -U pytest
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m shard_routing
```
