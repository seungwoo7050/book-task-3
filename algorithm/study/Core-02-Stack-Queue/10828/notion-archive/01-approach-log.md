# 접근 과정 — Python list가 곧 스택이다

## 구현 전략

Python list를 그대로 스택으로 사용한다.
- `push X` → `stack.append(X)`
- `pop` → `stack.pop()` (비면 -1)
- `size` → `len(stack)`
- `empty` → `1 if not stack else 0`
- `top` → `stack[-1]` (비면 -1)

## 출력 최적화

명령마다 `print()`를 호출하는 대신, 결과를 리스트 `out`에 모아서 마지막에 `'\n'.join(out)`으로 한 번에 출력했다.
$N \le 10\,000$ 수준에서는 큰 차이가 없지만, 출력 횟수를 줄이는 습관은 유지하는 게 좋다.

## 명령 파싱

`cmd = input().split()` 후 `cmd[0]`으로 분기.
`push`만 인자가 있으므로 `cmd[1]`을 정수로 변환한다.

## 복잡도

| 항목 | 값 |
|------|-----|
| 시간 | O(N) — 각 명령 O(1) |
| 공간 | O(N) — push된 원소 저장 |
