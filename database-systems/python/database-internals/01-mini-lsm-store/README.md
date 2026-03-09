# 01 Mini LSM Store

## Summary

이 프로젝트는 Python 입문 트랙의 시작점이다. active memtable, flush, newest-first read path를 한 번에 구현해서 `Database Internals`의 초반 저장 엔진 흐름을 빠르게 잡는다. Go 트랙의 `01`, `02`, `03` 개념을 하나로 접었다.

## Status

- 상태: `verified`
- 구현 언어: `Python 3.14`
- 범위: in-memory memtable, immutable SSTable flush, tombstone, reopen

## Commands

```bash
python3 -m pip install -U pytest
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m mini_lsm_store
```
