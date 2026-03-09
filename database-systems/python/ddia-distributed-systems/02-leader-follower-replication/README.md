# 02 Leader-Follower Replication

## Summary

leader가 append-only mutation log를 만들고 follower가 watermark 이후 entry만 idempotent하게 적용한다. Python 트랙에서는 분산 쓰기 경로의 가장 작은 복제 단위를 본다.

## Status

- 상태: `verified`
- 구현 언어: `Python 3.14`
- 범위: leader store, replication log, follower apply, incremental sync helper

## Commands

```bash
python3 -m pip install -U pytest
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m leader_follower
```
