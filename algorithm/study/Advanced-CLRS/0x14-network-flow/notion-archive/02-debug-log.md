# 0x14 Network Flow — 디버깅 기록

## 역간선 누락

adj에 역간선을 추가하지 않으면 BFS가 잔여 그래프를 제대로 탐색하지 못함. 양방향 추가 필수.

## parent 추적

BFS 후 `parent[]` 배열로 경로 역추적. `parent[t]`부터 `s`까지 거슬러 올라감.

## 테스트

```bash
make -C problem test
```

PASS.
