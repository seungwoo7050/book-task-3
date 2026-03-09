# 02 WAL Recovery

## Summary

이 프로젝트는 append-only WAL, CRC32 검증, replay 기반 복구를 Python으로 구현한다. Python 트랙에서는 `mini-lsm-store` 위에 durability를 추가하는 단계다.

## Status

- 상태: `verified`
- 구현 언어: `Python 3.14`
- 범위: append-before-apply, stop-on-corruption replay, flush 후 WAL rotation

## Commands

```bash
python3 -m pip install -U pytest
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m wal_recovery
```
