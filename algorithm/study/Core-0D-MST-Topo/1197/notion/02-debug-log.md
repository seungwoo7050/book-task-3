# BOJ 1197 — 디버깅 기록

## 함정 1: 간선 정렬 기준

`(c, a, b)` 형태로 가중치를 첫 번째로 놓아야 자연 정렬 가능. `(a, b, c)` 순서면 별도 key 지정 필요.

## 함정 2: 음의 가중치

MST는 음의 가중치도 허용. 크루스칼은 문제없이 처리.

## 함정 3: Union 반환값

`union` 함수가 `False` 반환 시 같은 집합 → 사이클 → 선택 안 함.

## 확인 과정

```bash
make -C problem test
make -C problem run-cpp
```

PASS.
