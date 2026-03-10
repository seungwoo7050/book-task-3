# 지식 인덱스

> 프로젝트: 합칠 수 있는 힙 브리지
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

| 개념 | CLRS 참조 | 설명 |
|------|-----------|------|
| Mergeable Heap | Ch 19 | meld 연산 지원 힙 |
| Pairing Heap | — | 실용적 mergeable min-heap |
| merge_pairs | — | 2-pass pairing 합침 |
| child-sibling 표현 | — | 다원 트리의 이진 표현 |

## 다시 연결해 볼 질문

- `합칠 수 있는 힙 브리지`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `합칠 수 있는 힙 브리지의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `합칠 수 있는 힙 브리지`를 다시 설명할 때는 문제 이름보다 `합칠 수 있는 힙 브리지의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 앞 프로젝트: [`../../0x12-red-black-tree/README.md`](../../0x12-red-black-tree/README.md) (레드-블랙 트리 삽입과 검증)
- 다음 프로젝트: [`../../0x14-network-flow/README.md`](../../0x14-network-flow/README.md) (네트워크 플로우)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`meldable-heap-concept.md`](../docs/concepts/meldable-heap-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
