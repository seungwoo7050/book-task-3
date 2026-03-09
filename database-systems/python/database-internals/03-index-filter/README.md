# 03 Index Filter

## Summary

이 프로젝트는 Bloom filter와 sparse index를 붙인 SSTable을 Python으로 구현한다. 존재하지 않는 key는 즉시 거절하고, 존재하는 key는 작은 block 범위만 읽는 read path가 핵심이다.

## Status

- 상태: `verified`
- 구현 언어: `Python 3.14`
- 범위: probabilistic reject, sparse block index, footer metadata, bounded scan stats

## Commands

```bash
python3 -m pip install -U pytest
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m index_filter
```
