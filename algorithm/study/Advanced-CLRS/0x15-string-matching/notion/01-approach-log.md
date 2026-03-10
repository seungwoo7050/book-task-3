# 접근 로그

> 프로젝트: 고급 문자열 매칭
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## KMP: Prefix Function

```python
pi = [0] * m
k = 0
for i in range(1, m):
    while k and pattern[k] != pattern[i]:
        k = pi[k-1]
    if pattern[k] == pattern[i]:
        k += 1
    pi[i] = k
```

`pi[i]` = pattern[0..i]의 최장 proper prefix-suffix 길이. 불일치 시 `pi[k-1]`로 점프하여 중복 비교 회피.

## KMP: 매칭

텍스트를 순회하며 패턴과 비교. 불일치 시 `pi[]` 활용 — 처음부터 다시 비교하지 않음.

## Rabin-Karp: Rolling Hash

- base = 257, mod = $10^9 + 7$
- 패턴 해시값 미리 계산
- 텍스트 윈도우 해시를 슬라이딩: `h = (h - ord(t[i]) * high) * base + ord(t[i+m])`
- 해시 충돌 시 실제 문자열 비교로 검증

```python
high = pow(base, m - 1, mod)
```

## 이 접근에서 꼭 기억할 선택

- `고급 문자열 매칭`에서 중심이 된 판단은 `고급 문자열 매칭의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- CLRS Ch 32의 핵심 아이디어를 입출력과 자동 검증이 가능한 작은 실험으로 바꾸는 과정이 중요했다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`string-matching-concept.md`](../docs/concepts/string-matching-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
