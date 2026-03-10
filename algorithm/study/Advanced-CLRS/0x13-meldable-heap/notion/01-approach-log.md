# 접근 로그

> 프로젝트: 합칠 수 있는 힙 브리지
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## merge(a, b)

두 루트 중 작은 쪽을 루트로 삼고, 큰 쪽을 루트의 child 리스트 맨 앞에 연결.

## merge_pairs(node)

Pairing Heap의 핵심. Child 리스트를 두 개씩 짝지어 merge하고(left-to-right), 그 결과를 역순으로 다시 merge(right-to-left). 2-pass 방식.

```python
def merge_pairs(node):
    if node is None or node.sibling is None:
        return node
    a, b, rest = node, node.sibling, node.sibling.sibling
    a.sibling = b.sibling = None
    return merge(merge(a, b), merge_pairs(rest))
```

## PairingHeap 클래스

- `push(key)`: 새 Node 생성 후 root와 merge
- `pop()`: root 제거 후 children을 merge_pairs로 합침
- `meld(other)`: 두 힙의 root를 merge

## 다중 힙 관리

`heaps = {}` 딕셔너리로 이름별 힙 관리.

## 이 접근에서 꼭 기억할 선택

- `합칠 수 있는 힙 브리지`에서 중심이 된 판단은 `합칠 수 있는 힙 브리지의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- CLRS Ch 19의 핵심 아이디어를 입출력과 자동 검증이 가능한 작은 실험으로 바꾸는 과정이 중요했다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`meldable-heap-concept.md`](../docs/concepts/meldable-heap-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
