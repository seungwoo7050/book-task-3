# Synchronization Contention Lab 시리즈 맵

## 프로젝트 개요

mutex counter, semaphore gate, bounded buffer producer-consumer 세 가지 contention scenario를
C와 pthread로 구현하고 wait_events로 경쟁 정도를 측정한다.

## 타임라인

| 파일 | 기간 | 핵심 내용 |
|------|------|-----------|
| [1편](10-2026-03-11.md) | 2026-03-11 | trylock + wait_events, condition variable 분리, overflow/underflow 검증 |

## 검증 경로

```bash
cd c && make clean && make
./contention_lab counter 4 1000
./contention_lab gate 6 3 500
./contention_lab buffer 3 2 200
```
