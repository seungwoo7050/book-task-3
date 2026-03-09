# 0x14 Network Flow — 문제 프레이밍

## 첫인상

CLRS Ch 26 네트워크 유량. Edmonds-Karp 알고리즘 (Ford-Fulkerson + BFS). 최대 유량 문제.

## 프로젝트 구조

용량 행렬 `cap[u][v]`, 인접 리스트 `adj[]`. BFS로 증가 경로 탐색, 잔여 그래프 갱신.

## 왜 이 프로젝트인가

이분 매칭, 최소 컷, 순환 제거 등 조합 최적화의 핵심 도구. Edmonds-Karp는 $O(VE^2)$ 보장.
