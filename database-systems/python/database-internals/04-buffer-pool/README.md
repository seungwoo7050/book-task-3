# 04 Buffer Pool

## Summary

이 프로젝트는 disk-backed page를 메모리에 올리고, LRU eviction, pin/unpin, dirty write-back을 Python으로 구현한다. 웹 백엔드 관점에서 파일 기반 페이지 캐시가 어떻게 동작하는지 파악하기 좋은 단계다.

## Status

- 상태: `verified`
- 구현 언어: `Python 3.14`
- 범위: O(1) LRU cache, fixed-size page fetch, dirty flush

## Commands

```bash
python3 -m pip install -U pytest
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m buffer_pool
```
