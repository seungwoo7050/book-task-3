# 접근 로그

> 프로젝트: 계산 기하 실습
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## Cross Product (방향 판정)

```python
def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
```

- 양수: 반시계 방향 (CCW)
- 음수: 시계 방향 (CW)
- 0: 일직선 (collinear)

## Convex Hull: Andrew's Monotone Chain

1. 점들을 x좌표 기준 정렬
2. Lower hull: 왼쪽→오른쪽, CW가 아닌 점 제거
3. Upper hull: 오른쪽→왼쪽, 동일 로직
4. 합치기

$O(n \log n)$ — 정렬이 지배적.

## Segment Intersection

두 선분 $(a,b)$, $(c,d)$의 교차:
1. `cross(a,b,c)` × `cross(a,b,d)` ≤ 0 AND `cross(c,d,a)` × `cross(c,d,b)` ≤ 0
2. Collinear인 경우 `on_segment` 검사로 겹침 확인

## 이 접근에서 꼭 기억할 선택

- `계산 기하 실습`에서 중심이 된 판단은 `계산 기하 실습의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- CLRS Ch 33의 핵심 아이디어를 입출력과 자동 검증이 가능한 작은 실험으로 바꾸는 과정이 중요했다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`geometry-primitives.md`](../docs/concepts/geometry-primitives.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
