# 지식 인덱스

> 프로젝트: Strassen 행렬 곱셈
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

| 개념 | CLRS 참조 | 설명 |
|------|-----------|------|
| 분할 정복 | Ch 4 | 문제를 재귀적 부분 문제로 분할 |
| Strassen | Ch 4.2 | 7번 곱셈 + 18번 덧뺄셈 |
| 마스터 정리 | Ch 4.5 | $T(n)=7T(n/2)+O(n^2)$ |

## 연결 문제

- CLRS Ch 4 전반

## 다시 연결해 볼 질문

- `Strassen 행렬 곱셈`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `Strassen 행렬 곱셈의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `Strassen 행렬 곱셈`를 다시 설명할 때는 문제 이름보다 `Strassen 행렬 곱셈의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 다음 프로젝트: [`../../0x11-amortized-analysis-lab/README.md`](../../0x11-amortized-analysis-lab/README.md) (상각 분석 실습)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`strassen-concept.md`](../docs/concepts/strassen-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
