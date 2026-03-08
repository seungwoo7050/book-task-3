# Edge Cases — BOJ 1753 Shortest Path

## 1. 시작점에서 도달 불가
`INF` 출력.

## 2. 자기 자신
거리 0.

## 3. 같은 간선 여러 개
최소 가중치가 선택됨 (다익스트라가 자동 처리).

## 핵심 주의점
- $V \le 20000, E \le 300000$ → $O((V+E)\log V)$ 필요
- `sys.stdin.readline` 필수
