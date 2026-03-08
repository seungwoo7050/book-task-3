# Residual Graph and Augmenting Paths

## CLRS Connection

CLRS Ch 26 frames max flow around residual capacity and augmenting paths.

## Study Notes

- residual graph를 명시적으로 관리하면 역간선 업데이트가 자연스럽다.
- Edmonds-Karp는 BFS로 가장 짧은 augmenting path를 선택해 종료성과 complexity reasoning을 단순화한다.
- min-cut proof는 docs reading path에 남기고, 구현은 max-flow 값 계산에 집중한다.
