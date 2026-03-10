# 접근 로그

> 프로젝트: 정수론 실습
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## Extended GCD

```python
def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y
```

$ax + by = \gcd(a, b)$ 의 해 $(x, y)$ 반환.

## 모듈러 역원

`modinv(a, m)`: $a \cdot x \equiv 1 \pmod{m}$ 인 $x$. `egcd(a, m)` 에서 gcd=1이면 `x % m`.

## CRT (중국인 나머지 정리)

합동식 $(r_1, m_1), (r_2, m_2), \ldots$ 를 반복적으로 병합:

$$x \equiv r_1 \pmod{m_1}, \quad x \equiv r_2 \pmod{m_2}$$

$\to$ $x \equiv r \pmod{\text{lcm}(m_1, m_2)}$

## Toy RSA

1. $n = p \times q$
2. $\phi = (p-1)(q-1)$
3. $d = e^{-1} \bmod \phi$
4. cipher = $m^e \bmod n$
5. plain = $\text{cipher}^d \bmod n$

Python `pow(m, e, n)` 으로 모듈러 거듭제곱.

## 이 접근에서 꼭 기억할 선택

- `정수론 실습`에서 중심이 된 판단은 `정수론 실습의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- CLRS Ch 31의 핵심 아이디어를 입출력과 자동 검증이 가능한 작은 실험으로 바꾸는 과정이 중요했다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`number-theory-concept.md`](../docs/concepts/number-theory-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
