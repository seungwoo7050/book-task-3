# 접근 로그

> 프로젝트: 집합의 표현
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## Union-Find 구현

```python
def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]  # path splitting
        x = parent[x]
    return x

def union(parent, a, b):
    ra = find(parent, a)
    rb = find(parent, b)
    if ra == rb:
        return
    if ra < rb:
        parent[rb] = ra
    else:
        parent[ra] = rb
```

## 경로 압축: Path Splitting

`parent[x] = parent[parent[x]]` — 할아버지를 부모로 변경. 재귀적 경로 압축보다 Python에서 안전(스택 오버플로 없음).

## Union 전략

이 코드에서는 번호가 작은 쪽을 루트로 유지. 랭크 기반은 아니지만 실용적으로 충분.

## 시간/공간

- 각 연산 거의 $O(\alpha(N)) \approx O(1)$

## 이 접근에서 꼭 기억할 선택

- `집합의 표현`에서 중심이 된 판단은 `다음 트랙에서 필요한 선행 개념을 별도 실습으로 고정하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 다음 트랙에서 다시 만나게 될 선행 개념을 지금 확실히 고정해 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`disjoint-set-union.md`](../docs/concepts/disjoint-set-union.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
- 같은 트랙의 큰 흐름은 [`../../README.md`](../../README.md)에서 다시 확인한다.
