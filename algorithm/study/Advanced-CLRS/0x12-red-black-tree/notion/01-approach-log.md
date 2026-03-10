# 접근 로그

> 프로젝트: 레드-블랙 트리 삽입과 검증
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## RB-Tree 성질

1. 모든 노드는 RED 또는 BLACK
2. 루트는 BLACK
3. NIL(센티넬)은 BLACK
4. RED 노드의 자식은 모두 BLACK (연속 RED 불가)
5. 모든 경로의 black-height 동일

## 삽입 전략

새 노드를 RED로 삽입 후 `insert_fixup` 호출:
- **Case 1**: 삼촌이 RED → 부모·삼촌 BLACK, 조부모 RED, 조부모로 올라감
- **Case 2**: 삼촌 BLACK, 꺾인 형태 → 회전으로 Case 3 변환
- **Case 3**: 삼촌 BLACK, 직선 형태 → 부모 BLACK, 조부모 RED, 회전

## 회전

```python
def left_rotate(self, x):
    y = x.right
    x.right = y.left
    ...
```

포인터 5개 갱신. 대칭적 right_rotate도 동일 패턴.

## 중복 키 처리

이미 존재하면 삽입 스킵 — 집합 의미론.

## 이 접근에서 꼭 기억할 선택

- `레드-블랙 트리 삽입과 검증`에서 중심이 된 판단은 `레드-블랙 트리 삽입과 검증의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- CLRS Ch 13, 18의 핵심 아이디어를 입출력과 자동 검증이 가능한 작은 실험으로 바꾸는 과정이 중요했다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`red-black-invariants.md`](../docs/concepts/red-black-invariants.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
