# 접근 로그

> 프로젝트: Strassen 행렬 곱셈
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## Naive vs Strassen

- Naive: 3중 루프, $O(n^3)$
- Strassen: 행렬을 4개 부분으로 분할, 7번 곱셈 + 18번 덧셈/뺄셈

## 핵심 구현

1. **split**: 행렬을 4개 사분면으로 분할
2. **P1~P7**: 7개 보조 곱셈 (Strassen의 공식)
3. **combine**: 결과 조합
4. **pad**: 2의 거듭제곱으로 패딩
5. **베이스 케이스**: $n \leq 2$이면 naive

```python
p1 = strassen(add(a11, a22), add(b11, b22))
# ... p2~p7
c11 = add(sub(add(p1, p4), p5), p7)
```

## 시간 복잡도

$$T(n) = 7T(n/2) + O(n^2) = O(n^{\log_2 7}) \approx O(n^{2.807})$$

## 이 접근에서 꼭 기억할 선택

- `Strassen 행렬 곱셈`에서 중심이 된 판단은 `Strassen 행렬 곱셈의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- CLRS Ch 4의 핵심 아이디어를 입출력과 자동 검증이 가능한 작은 실험으로 바꾸는 과정이 중요했다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`strassen-concept.md`](../docs/concepts/strassen-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
