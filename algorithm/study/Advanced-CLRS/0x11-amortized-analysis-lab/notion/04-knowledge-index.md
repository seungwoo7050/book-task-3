# 지식 인덱스

> 프로젝트: 상각 분석 실습
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

| 개념 | CLRS 참조 | 설명 |
|------|-----------|------|
| 분할 상환 분석 | Ch 17 | 연산 시퀀스의 평균 비용 |
| 집합체 분석 | Ch 17.1 | 총 비용 / 연산 수 |
| 회계법 | Ch 17.2 | 각 연산에 amortized cost 배정 |
| 퍼텐셜법 | Ch 17.3 | 자료구조 상태의 퍼텐셜 함수 |

## 다시 연결해 볼 질문

- `상각 분석 실습`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `상각 분석 실습의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `상각 분석 실습`를 다시 설명할 때는 문제 이름보다 `상각 분석 실습의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 앞 프로젝트: [`../../0x10-strassen-matrix/README.md`](../../0x10-strassen-matrix/README.md) (Strassen 행렬 곱셈)
- 다음 프로젝트: [`../../0x12-red-black-tree/README.md`](../../0x12-red-black-tree/README.md) (레드-블랙 트리 삽입과 검증)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`amortized-concept.md`](../docs/concepts/amortized-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
