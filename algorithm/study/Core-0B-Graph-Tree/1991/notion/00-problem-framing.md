# 문제 프레이밍

> 프로젝트: 트리 순회
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

이진 트리의 전위(preorder), 중위(inorder), 후위(postorder) 순회를 구현하는 고전 문제. CLRS Ch 12의 트리 순회를 직접 코딩하는 연습.

## 문제 구조

- $N$개의 노드 (알파벳 대문자)
- 각 노드의 왼쪽/오른쪽 자식 주어짐 (없으면 `.`)
- 전위/중위/후위 순회 결과 각각 출력

## 왜 이 문제를 선택했는가

트리 순회의 기초. 재귀 구조를 직접 작성하며 세 가지 순회의 차이를 체화.

## 난이도 평가

Silver. 재귀 구현 자체는 단순하지만, 세 순회의 순서를 정확히 이해해야 함.

## 지금 이 프로젝트에서 먼저 고정할 것

- `트리 순회`에서 실제로 확인하려는 학습 목표는 `트리 구조의 성질을 이용해 탐색과 누적 계산을 재구성하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`traversal-concept.md`](../docs/concepts/traversal-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 앞 프로젝트: [`../../11725/README.md`](../../11725/README.md) (트리의 부모 찾기)
