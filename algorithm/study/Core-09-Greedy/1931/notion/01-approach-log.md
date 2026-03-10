# 접근 로그

> 프로젝트: 회의실 배정
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 전략

**종료 시간 기준 오름차순 정렬 → 탐욕적 선택**

```python
meetings.sort(key=lambda x: (x[1], x[0]))

count = 0
last_end = 0
for start, end in meetings:
    if start >= last_end:
        count += 1
        last_end = end
```

## 왜 종료 시간 기준?

일찍 끝나는 회의를 선택하면 남은 시간이 가장 많아져서, 이후 선택할 수 있는 회의가 최대. 이것이 그리디 선택 속성.

## 왜 `(x[1], x[0])` 으로 정렬?

종료 시간이 같은 경우, 시작 시간 기준으로 정렬해야 한다. 예: (1,2)와 (2,2)가 있으면 두 회의 모두 선택 가능. 시작 시간이 같거나 작은 것을 먼저 놓아야 경계 조건 `start >= last_end`가 올바르게 동작.

## 교환 논증 (Exchange Argument)

최적해가 종료 시간이 빠른 회의 $a$를 포함하지 않는다고 가정. 최적해의 첫 회의 $b$를 $a$로 교체해도 나머지 회의와 겹치지 않으므로. 개수 동일 이상. 모순.

## 시간/공간

- $O(N \log N)$ 정렬 + $O(N)$ 스캔

## 이 접근에서 꼭 기억할 선택

- `회의실 배정`에서 중심이 된 판단은 `탐욕 선택의 기준을 말로 설명하고 반례 가능성을 점검하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`activity-selection-concept.md`](../docs/concepts/activity-selection-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
