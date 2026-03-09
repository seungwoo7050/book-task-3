# BOJ 2252 — 디버깅 기록

## 주의점 1: 사이클

이 문제에서는 사이클 없음이 보장. 만약 사이클이 있으면 result의 크기 < N으로 탐지 가능.

## 주의점 2: 비유일 해

여러 정답이 가능. 아무거나 출력하면 됨.

## 확인 과정

```bash
make -C problem test
make -C problem run-cpp
```

PASS.
