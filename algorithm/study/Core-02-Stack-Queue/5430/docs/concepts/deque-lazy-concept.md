# 덱(Deque)과 Lazy Reversal 개념 정리

## 덱(Double-Ended Queue)이란?

**덱(Deque)**은 양쪽 끝에서 삽입과 삭제가 모두 $O(1)$인 자료구조이다.
스택과 큐의 기능을 동시에 지원한다.

## CLRS 연결

CLRS Ch 10.1 연습문제 10.1-5에서 덱을 다룬다:
> "Whereas a stack allows insertion and deletion of elements at only one end,
> and a queue allows insertion at one end and deletion at the other end,
> a deque allows insertion and deletion at both ends."

## Lazy Reversal 기법

### 문제
R 연산(배열 뒤집기)마다 실제로 뒤집으면 $O(N)$.
$|p| \le 100{,}000$이면 최악 $O(|p| \cdot N) \approx 10^{10}$ → TLE.

### 해결
방향 플래그 `is_reversed`만 토글:

```python
if cmd == 'R':
    is_reversed = not is_reversed
elif cmd == 'D':
    if is_reversed:
        dq.pop()       # 논리적 앞 = 물리적 뒤
    else:
        dq.popleft()   # 논리적 앞 = 물리적 앞
```

### 핵심 아이디어
- **실제 뒤집기 비용**: $O(N)$
- **플래그 토글 비용**: $O(1)$
- D 연산 시 플래그에 따라 pop 방향만 바꿈
- 최종 출력 시에만 필요하면 한 번 뒤집음

## Lazy 기법의 일반화

| 문제 영역 | Lazy 기법 적용 |
|-----------|---------------|
| AC (이 문제) | 배열 뒤집기 지연 |
| 세그먼트 트리 | Lazy Propagation |
| 가비지 컬렉션 | 지연 해제 |
| Copy-on-Write | 쓸 때만 복사 |

"비싼 연산을 최대한 미루고, 꼭 필요할 때만 수행한다."

## 배열 파싱 주의점

입력이 `[1,2,3,4]` 형태의 문자열이므로:
1. 대괄호 제거: `arr_str[1:-1]`
2. 콤마 분리: `.split(',')`
3. **빈 배열 처리**: `n=0`일 때 `"[]"` → `split(',')`하면 `['']` 발생 주의
