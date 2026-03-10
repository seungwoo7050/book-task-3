# 지식 인덱스

> 프로젝트: 근사 알고리즘 실습
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

| 개념 | CLRS 참조 | 설명 |
|------|-----------|------|
| 근사 알고리즘 | Ch 35 | NP-hard에 대한 다항 시간 근사해 |
| 근사 비율 $\rho$ | Ch 35.1 | 해 / 최적해 ≤ $\rho$ |
| Greedy Set Cover | Ch 35.3 | $O(\ln n)$-근사 |
| 2-Approx Vertex Cover | Ch 35.1 | 간선 양끝점 동시 선택 |

## 다시 연결해 볼 질문

- `근사 알고리즘 실습`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `근사 알고리즘 실습의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `근사 알고리즘 실습`를 다시 설명할 때는 문제 이름보다 `근사 알고리즘 실습의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 앞 프로젝트: [`../../0x18-np-completeness-lab/README.md`](../../0x18-np-completeness-lab/README.md) (NP-완전성 실습)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`approximation-concept.md`](../docs/concepts/approximation-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
