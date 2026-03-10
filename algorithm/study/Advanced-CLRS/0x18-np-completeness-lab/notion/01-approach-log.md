# 접근 로그

> 프로젝트: NP-완전성 실습
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## Vertex Cover 검증

입력: 그래프 (정점, 간선), 인증서 (정점 부분집합)
검증: 모든 간선 $(u, v)$에 대해 $u \in S$ 또는 $v \in S$ → YES / NO

```python
cover = set(certificate)
for u, v in edges:
    if u not in cover and v not in cover:
        return "NO"
return "YES"
```

$O(E)$ 시간.

## 3-SAT 검증

입력: 절(clause) 리스트 (각 절에 리터럴 3개), 인증서 (변수 할당)
검증: 모든 절에서 최소 하나의 리터럴이 참 → YES / NO

```python
for clause in clauses:
    if not any(satisfies(lit, assignment) for lit in clause):
        return "NO"
return "YES"
```

$O(C)$ 시간 (C = 절 수).

## 이 접근에서 꼭 기억할 선택

- `NP-완전성 실습`에서 중심이 된 판단은 `NP-완전성 실습의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- CLRS Ch 34의 핵심 아이디어를 입출력과 자동 검증이 가능한 작은 실험으로 바꾸는 과정이 중요했다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`certificate-verifier-concept.md`](../docs/concepts/certificate-verifier-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
