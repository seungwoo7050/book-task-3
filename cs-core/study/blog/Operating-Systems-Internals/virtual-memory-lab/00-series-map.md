# Virtual Memory Lab 시리즈 맵

## 프로젝트 개요

FIFO, LRU, Clock, OPT 네 가지 page replacement policy를 Python으로 구현하고,
trace 기반으로 fault 수, dirty eviction을 비교한다.

## 타임라인

| 파일 | 기간 | 핵심 내용 |
|------|------|-----------|
| [1편](10-2026-03-11.md) | 2026-03-11 | Frame 설계, Clock referenced bit, OPT future_uses, dirty_eviction 측정 |

## 검증 경로

```bash
cd python && pip install -e . && pytest tests/ -v
python -m os_virtual_memory trace.txt --frames 4 --policy lru
```
