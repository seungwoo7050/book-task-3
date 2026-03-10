# BOJ 1181 — 접근 과정: set + sorted

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
