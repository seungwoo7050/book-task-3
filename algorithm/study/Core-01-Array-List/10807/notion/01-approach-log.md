# 접근 로그

> 프로젝트: 개수 세기
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 가장 직접적인 방법

Python의 `list.count()` 메서드를 쓰면 끝이다.
내부적으로 이 메서드는 배열을 처음부터 끝까지 순회하면서 일치하는 원소를 세는 O(n) 연산이다.

만약 직접 구현한다면:
```python
count = 0
for x in arr:
    if x == v:
        count += 1
```
결과는 동일하다. `count()` 메서드가 이걸 C 레벨에서 해줄 뿐이다.

## 다른 방법이 필요한가?

$N \le 100$이므로 어떤 방법이든 상관없다.
하지만 만약 $N$이 매우 크고 여러 번 질의한다면, `Counter`나 해시맵을 써서 O(1) 조회가 가능하다.
이 문제에서는 질의가 한 번이므로 그런 사전 처리가 불필요하다.

## 복잡도

| 항목 | 값 |
|------|-----|
| 시간 | O(N) |
| 공간 | O(N) (배열 저장) |

## 이 접근에서 꼭 기억할 선택

- `개수 세기`에서 중심이 된 판단은 `순차 자료구조를 선택하고 편집 연산의 비용 모델을 설명하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`array-concept.md`](../docs/concepts/array-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
