# BOJ 1717 — 디버깅 기록

## 함정 1: 경로 압축 없이 TLE

$M \leq 100,000$, $N \leq 1,000,000$. 경로 압축 없으면 find가 $O(N)$이 되어 TLE.

## 함정 2: 재귀 경로 압축 → RecursionError

Python에서 재귀적 `find`는 깊은 트리에서 스택 오버플로. 반복적 path splitting 사용.

## 주의점: 출력

`sys.stdout.write` + `'\n'.join` 사용. `print` 반복은 느림.

## 확인 과정

```bash
make -C problem test
```

PASS.
