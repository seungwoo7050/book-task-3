# 지식 인덱스

> 프로젝트: NP-완전성 실습
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

| 개념 | CLRS 참조 | 설명 |
|------|-----------|------|
| NP | Ch 34.1 | 다항 시간 검증 가능 문제 |
| NP-완전 | Ch 34.3 | NP이면서 NP-hard |
| Vertex Cover | Ch 34.5.2 | 모든 간선 커버하는 최소 정점 집합 |
| 3-SAT | Ch 34.4 | 3-리터럴 절의 논리식 만족성 |
| 인증서 (certificate) | Ch 34.1 | 검증기에 제공되는 해 후보 |

## 다시 연결해 볼 질문

- `NP-완전성 실습`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `NP-완전성 실습의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `NP-완전성 실습`를 다시 설명할 때는 문제 이름보다 `NP-완전성 실습의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 앞 프로젝트: [`../../0x17-number-theory-lab/README.md`](../../0x17-number-theory-lab/README.md) (정수론 실습)
- 다음 프로젝트: [`../../0x19-approximation-lab/README.md`](../../0x19-approximation-lab/README.md) (근사 알고리즘 실습)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`certificate-verifier-concept.md`](../docs/concepts/certificate-verifier-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
