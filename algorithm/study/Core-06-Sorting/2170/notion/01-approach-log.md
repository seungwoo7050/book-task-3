# 접근 로그

> 프로젝트: 선 긋기
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 아이디어

선분을 **시작점 기준으로 정렬**하면, 겹치는 선분끼리 연속으로 나타난다. 정렬된 선분을 하나씩 훑으면서(sweep) 현재 구간과 합칠 수 있으면 확장, 아니면 확정하고 새 구간 시작.

## 구현

```python
segments.sort()
cur_start, cur_end = segments[0]

for s, e in segments[1:]:
    if s <= cur_end:
        cur_end = max(cur_end, e)  # 확장
    else:
        total += cur_end - cur_start  # 확정
        cur_start, cur_end = s, e

total += cur_end - cur_start  # 마지막 구간
```

## 정렬 키

`(시작점, 끝점)` 튜플로 정렬. 시작점이 같으면 끝점 순서는 결과에 영향을 주지 않지만 (어차피 `max(cur_end, e)`로 처리), 기본 튜플 비교가 자연스럽다.

## 대안으로 고려한 것

- **좌표 압축 + 배열**: 좌표를 압축한 뒤 스위프. 값 범위가 $-10^9 \sim 10^9$이므로 직접 배열은 불가능, 압축이 필요하지만 과한 설계.
- **이벤트 포인트 방식**: 각 선분의 시작/끝을 (+1, -1) 이벤트로 저장, 정렬 후 누적합. 동일 결과지만 코드가 더 복잡.

구간 합치기가 가장 직관적이고 효율적.

## I/O 최적화

$N \leq 10^6$이므로 `sys.stdin.readline`이 필수. `input()` 사용 시 TLE.

## 이 접근에서 꼭 기억할 선택

- `선 긋기`에서 중심이 된 판단은 `정렬 기준을 설계하고, 정렬 이후의 후처리 로직을 분리해 설명하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`interval-merge-concept.md`](../docs/concepts/interval-merge-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
