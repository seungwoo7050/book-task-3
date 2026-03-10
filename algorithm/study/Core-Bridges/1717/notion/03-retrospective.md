# 회고

> 프로젝트: 집합의 표현
> 아래 내용은 `notion-archive/03-retrospective.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 배운 것

Union-Find는 단순하지만 최적화가 중요한 자료구조. 경로 압축 하나로 $O(N)$ → $O(\alpha(N))$ 개선. 이 차이가 TLE와 AC의 경계.

## 1197 크루스칼과의 연결

이 문제의 Union-Find가 크루스칼의 핵심 부품. 독립적으로 연습한 후 MST에 적용하면 이해가 깊어진다.

## Path Splitting vs Path Halving vs Full Compression

- Full compression (재귀): 모든 노드를 루트 직속으로 → Python에서 스택 문제
- Path splitting (반복): 각 노드를 할아버지로 → 안전하고 충분히 빠름
- Path halving: 짝수 번째 노드만 → splitting과 비슷

## 이번 프로젝트가 남긴 기준

- `집합의 표현`를 통해 `다음 트랙에서 필요한 선행 개념을 별도 실습으로 고정하는 연습`를 코드와 문장으로 같이 설명하는 감각을 다시 확인했다.
- 짧은 정답 코드보다, 왜 이 선택이 안전했는지 적어 둔 문장이 나중에 더 오래 남는다.
- 다음 트랙에서 다시 만나게 될 선행 개념을 지금 확실히 고정해 두는 것이 핵심이었다.

## 다음 프로젝트로 가져갈 것

- 구현을 시작하기 전에 핵심 상태와 종료 조건을 먼저 적는다.
- 자동 검증이 통과한 뒤에야 문서 문장을 확정한다.
- 포트폴리오용 README로 옮길 때는 "선택 이유"와 "실수 포인트"를 먼저 보여 준다.
- `05-development-timeline.md`처럼 실행 순서와 검증 순서를 남기면, 시간이 지난 뒤에도 학습 과정을 다시 밟기 쉬워진다.

## 트랙 안에서 이어지는 연결

- 같은 트랙의 큰 흐름은 [`../../README.md`](../../README.md)에서 다시 확인한다.
- 현재 프로젝트를 다시 설명할 때는 같은 트랙의 앞뒤 프로젝트와 무엇이 달라졌는지 한 문장으로 비교해 두는 편이 좋다.

## 다시 확인할 경로

- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
- [`disjoint-set-union.md`](../docs/concepts/disjoint-set-union.md)
