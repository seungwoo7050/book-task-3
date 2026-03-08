# 스택(Stack) 개념 정리

## 정의

**스택(Stack)**은 LIFO(Last-In, First-Out) 원칙을 따르는 선형 자료구조이다.
가장 최근에 삽입된 원소가 가장 먼저 제거된다.

## CLRS 연결

CLRS Ch 10.1 (pp. 232–233)에서 배열 기반 스택을 다음과 같이 정의한다:

- `S.top`: 가장 최근에 삽입된 원소의 인덱스
- `S.top == 0`: 스택이 비어 있음 (underflow 조건)
- `S.top == n`: 스택이 꽉 참 (overflow 조건)

### CLRS 의사코드

```
STACK-EMPTY(S)
  if S.top == 0
    return TRUE
  else return FALSE

PUSH(S, x)
  S.top = S.top + 1
  S[S.top] = x

POP(S)
  if STACK-EMPTY(S)
    error "underflow"
  else S.top = S.top - 1
    return S[S.top + 1]
```

## 핵심 연산과 복잡도

| 연산 | 설명 | 시간 복잡도 |
|------|------|------------|
| `push(x)` | 스택 꼭대기에 x 삽입 | $O(1)$ |
| `pop()` | 꼭대기 원소 제거 및 반환 | $O(1)$ |
| `top()` | 꼭대기 원소 조회 (제거 X) | $O(1)$ |
| `size()` | 원소 개수 반환 | $O(1)$ |
| `empty()` | 비어 있는지 확인 | $O(1)$ |

## 언어별 구현 매핑

### Python
```python
stack = []
stack.append(x)   # push
stack.pop()        # pop
stack[-1]          # top
len(stack)         # size
not stack          # empty
```

### C++
```cpp
std::stack<int> st;
st.push(x);       // push
st.pop();          // pop (반환 X)
st.top();          // top
st.size();         // size
st.empty();        // empty
```

## 활용 분야

- 함수 호출 스택 (재귀)
- 괄호 매칭
- 후위 표기법 계산
- DFS 비재귀 구현
- Undo/Redo 기능
