# Edge Cases — BOJ 1916 Minimum Cost

## 1. 직행 노선이 최적
출발→도착 직행.

## 2. 같은 구간 여러 노선
최소 비용만 사용.

## 3. 출발 = 도착
비용 0.

## 핵심 주의점
- 방향 그래프 — `adj[u].append((v, w))`만
- "lazy deletion" 패턴: `if d > dist[u]: continue`
