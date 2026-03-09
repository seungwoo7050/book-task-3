# 05 MVCC

## Summary

이 프로젝트는 snapshot isolation, version chain, write-write conflict 검사를 Python으로 구현한다. Python 입문 트랙의 마지막 슬롯으로 트랜잭션 가시성과 GC까지 묶는다.

## Status

- 상태: `verified`
- 구현 언어: `Python 3.14`
- 범위: read-your-own-write, snapshot visibility, first-committer-wins, stale version GC

## Commands

```bash
python3 -m pip install -U pytest
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m mvcc_lab
```
