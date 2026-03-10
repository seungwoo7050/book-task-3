# 접근 로그

> 프로젝트: N-Queen
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 행 단위 백트래킹

퀸을 행 0부터 행 $N-1$까지 순서대로 배치한다. 각 행에서 열 $0 \sim N-1$ 중 하나를 선택하고, 충돌이 없을 때만 다음 행으로 진행한다.

## 충돌 검사의 핵심

세 가지 충돌 조건을 각각 배열로 관리한다:

1. **열 충돌** (`col[c]`): 열 $c$에 이미 퀸이 있는지
2. **↘ 대각선** (`diag1[row - c + n - 1]`): `row - col`이 같은 칸들
3. **↙ 대각선** (`diag2[row + c]`): `row + col`이 같은 칸들

```python
col = [False] * n
diag1 = [False] * (2 * n)
diag2 = [False] * (2 * n)
```

## 배치 함수

```python
def place(row):
    nonlocal count
    if row == n:
        count += 1
        return
    for c in range(n):
        if not col[c] and not diag1[row - c + n - 1] and not diag2[row + c]:
            col[c] = diag1[row - c + n - 1] = diag2[row + c] = True
            place(row + 1)
            col[c] = diag1[row - c + n - 1] = diag2[row + c] = False
```

## 대각선 인덱싱의 수학

- ↘ 대각선: 같은 대각선의 칸들은 `row - col`이 일정. 범위: $-(N-1)$ ~ $N-1$ → `+N-1`로 0-indexed 변환
- ↙ 대각선: `row + col`이 일정. 범위: $0$ ~ $2(N-1)$

## 카운터 관리

`nonlocal count`를 사용했다. 15649에서 순열을 리스트에 모았던 것과 달리, 이 문제는 개수만 세면 되므로 정수 카운터가 적합하다.

## 대안으로 고려한 것

- **비트마스크**: `col`, `diag1`, `diag2`를 정수의 비트로 관리. 비트 연산으로 유망성 판단을 $O(1)$에 가능. $N \leq 15$이면 32비트로 충분
- **1차원 배열**: `queens[row] = col`로 배치 기록, 매번 모든 이전 행과 비교 — $O(N)$ 검사로 느림
