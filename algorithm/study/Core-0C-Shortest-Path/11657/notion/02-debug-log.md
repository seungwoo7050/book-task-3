# BOJ 11657 — 디버깅 기록

## 함정 1: V번째 반복 위치

**증상**: 음의 사이클을 탐지 못함

**원인**: `i == n - 1` 검사를 루프 밖에서 하면 놓침

**해결**: relaxation 내부에서 `if i == n - 1: print(-1); return`

## 함정 2: INF에서 출발하는 relaxation

**증상**: INF + 음수값이 유한한 값이 됨

**원인**: `dist[a] = INF`인데 `dist[a] + c`를 계산

**해결**: `if dist[a] != INF` 조건 추가

## 함정 3: 도달 불가 정점

최단 경로가 없는 정점은 `-1` 출력 (음의 사이클의 `-1`과 구분).

## 확인 과정

```bash
make -C problem test
make -C problem run-cpp
```

PASS.
