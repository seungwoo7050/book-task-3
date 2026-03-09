# BOJ 1717 — 집합의 표현: Union-Find

## 첫인상

CLRS Ch 21 Disjoint Set Union의 직접 구현 문제. 합집합(Union)과 같은 집합 판별(Find) 연산만 수행하는 순수한 자료구조 문제.

## 문제 구조

- $N+1$개 원소 (0부터 N)
- $M$개 연산: 합치기(0) 또는 같은 집합인지 확인(1)
- 확인 연산마다 YES/NO 출력

## 왜 이 문제를 선택했는가

Core-Bridges 프로젝트. 크루스칼(BOJ 1197)에서 사용한 Union-Find를 독립적으로 훈련하기 위한 브릿지.

## 난이도 평가

Gold. Union-Find 최적화(경로 압축)가 없으면 TLE.
