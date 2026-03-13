# Scheduling Simulator 시리즈 맵

## 프로젝트 개요

FCFS, SJF, RR, MLFQ 네 가지 CPU scheduling policy를 Python으로 구현하고 비교한다.
fixture 기반 결정론적 replay와 metric(waiting/response/turnaround) 비교가 핵심.

## 타임라인

| 파일 | 기간 | 핵심 내용 |
|------|------|-----------|
| [1편](10-2026-03-11.md) | 2026-03-11 | ProcessState 설계, MLFQ boost 타이밍, load_fixture 검증 |

## 검증 경로

```bash
cd python && pip install -e . && pytest tests/ -v
python -m os_scheduling convoy.json --policy mlfq
```
