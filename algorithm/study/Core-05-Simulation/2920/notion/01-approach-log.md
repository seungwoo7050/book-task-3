# 접근 로그

> 프로젝트: 음계
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 가장 단순한 구현

두 개의 고정 배열과 비교하는 것이 가장 명확하다:

```python
if nums == [1, 2, 3, 4, 5, 6, 7, 8]:
    print("ascending")
elif nums == [8, 7, 6, 5, 4, 3, 2, 1]:
    print("descending")
else:
    print("mixed")
```

## 대안으로 고려한 것

- **인접 원소 차이 검사**: `nums[i+1] - nums[i]`가 모두 1이면 ascending, 모두 -1이면 descending. 더 일반적이지만 이 문제에서는 과한 설계.
- **sorted 비교**: `nums == sorted(nums)` vs `nums == sorted(nums, reverse=True)`. 정렬의 오버헤드가 불필요.
- **all + zip**: `all(a < b for a, b in zip(nums, nums[1:]))`. Pythonic하지만 가독성이 떨어짐.

고정 입력이 8개뿐이므로 직접 비교가 가장 명확하고 효율적이다.

## 이 접근에서 꼭 기억할 선택

- `음계`에서 중심이 된 판단은 `복잡한 설명을 작은 상태 전이 규칙으로 나누어 구현하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`simulation-concept.md`](../docs/concepts/simulation-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
