# BOJ 1753 — 디버깅 기록

## 함정 1: 중복 간선

같은 $(u, v)$ 쌍에 여러 간선이 있을 수 있음. 인접 리스트에 모두 넣으면 자연스럽게 처리.

## 함정 2: Lazy deletion 빼먹기

`if d > dist[u]: continue`를 빼면 이미 확정된 노드를 다시 처리 → TLE.

## 주의점: INF 값

Python에서 `float('inf')` 사용. 출력 시 문자열 `'INF'`로 변환 필요.

## 확인 과정

```bash
make -C problem test
make -C problem run-cpp
```

PASS.
