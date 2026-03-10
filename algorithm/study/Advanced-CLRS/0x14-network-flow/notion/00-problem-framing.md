# 문제 프레이밍

> 프로젝트: 네트워크 플로우
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

CLRS Ch 26 네트워크 유량. Edmonds-Karp 알고리즘 (Ford-Fulkerson + BFS). 최대 유량 문제.

## 프로젝트 구조

용량 행렬 `cap[u][v]`, 인접 리스트 `adj[]`. BFS로 증가 경로 탐색, 잔여 그래프 갱신.

## 왜 이 프로젝트인가

이분 매칭, 최소 컷, 순환 제거 등 조합 최적화의 핵심 도구. Edmonds-Karp는 $O(VE^2)$ 보장.

## 지금 이 프로젝트에서 먼저 고정할 것

- `네트워크 플로우`에서 실제로 확인하려는 학습 목표는 `네트워크 플로우의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- CLRS Ch 26의 핵심 아이디어를 입출력과 자동 검증이 가능한 작은 실험으로 바꾸는 과정이 중요했다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`residual-graph-concept.md`](../docs/concepts/residual-graph-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 앞 프로젝트: [`../../0x13-meldable-heap/README.md`](../../0x13-meldable-heap/README.md) (합칠 수 있는 힙 브리지)
