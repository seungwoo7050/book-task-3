# 접근 로그

> 프로젝트: 단어 정렬
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 중복 제거

`set`으로 중복 단어를 제거한다:
```python
words = set(input().strip() for _ in range(N))
```

## 다중 키 정렬

Python의 `sorted`에 key 함수를 전달:
```python
result = sorted(words, key=lambda w: (len(w), w))
```

`(len(w), w)` 튜플이 비교 키. Python은 튜플을 사전순으로 비교하므로, 길이가 같으면 문자열의 사전순으로 자동 정렬된다.

## 출력

```python
print('\n'.join(result))
```

## 대안으로 고려한 것

- **`sorted` 두 번**: 안정 정렬의 성질을 이용해, 먼저 사전순 정렬 → 다시 길이순 정렬. 동작하지만 비효율적.
- **딕셔너리**: 중복 제거에 `dict.fromkeys()` 사용. 삽입 순서를 유지하지만 이 문제에서는 불필요.
- **C++ `set<string>` + custom comparator**: C++에서는 비교 함수를 직접 정의해야 해서 코드가 길어짐.

## 이 접근에서 꼭 기억할 선택

- `단어 정렬`에서 중심이 된 판단은 `정렬 기준을 설계하고, 정렬 이후의 후처리 로직을 분리해 설명하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`multikey-sort-concept.md`](../docs/concepts/multikey-sort-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
