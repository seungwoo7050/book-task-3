# BOJ 11279 — 디버깅 기록

## 주의점 1: 부호 빼먹기

`heappop` 결과를 바로 출력하면 음수가 나옴. `-heapq.heappop(heap)` 필수.

## 주의점 2: 빈 힙 처리

`x = 0`인데 힙이 비어있으면 0을 출력해야 함. `if heap:` 검사 필요.

## 확인 과정

```bash
make -C problem test
```

PASS.
