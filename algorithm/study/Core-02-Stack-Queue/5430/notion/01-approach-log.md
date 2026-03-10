# 접근 로그

> 프로젝트: AC
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 아이디어: R을 플래그로 처리

`is_reversed` 불리언 변수를 토글한다.
D를 만나면:
- `is_reversed == False`: `dq.popleft()` (앞에서 삭제)
- `is_reversed == True`: `dq.pop()` (뒤에서 삭제 = 논리적으로 앞에서 삭제)

이렇게 하면 R은 O(1), D도 O(1)이다.

## 입력 파싱의 함정

배열이 `[1,2,3,4]` 형태의 문자열로 주어진다.
`arr_str[1:-1].split(',')` 으로 파싱하되, 빈 배열 `[]`일 때 `split(',')`이 `['']`을 반환하는 문제가 있다.
그래서 `n == 0`일 때는 별도로 빈 deque를 만들어야 한다.

## 최종 출력 형식

결과도 `[x1,x2,...]` 형태로 출력해야 한다.
`is_reversed`가 True인 채로 끝나면, 마지막에 `dq.reverse()`를 수행해야 한다.
이 부분은 deque가 비어 있는 경우에도 안전하다 (빈 deque의 reverse는 무해).

## 복잡도

| 항목 | 값 |
|------|-----|
| 시간 | O(\|p\| + n) per test case |
| 공간 | O(n) |

## 이 접근에서 꼭 기억할 선택

- `AC`에서 중심이 된 판단은 `명령 기반 자료구조 문제를 상태 전이 규칙으로 정리하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`deque-lazy-concept.md`](../docs/concepts/deque-lazy-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
