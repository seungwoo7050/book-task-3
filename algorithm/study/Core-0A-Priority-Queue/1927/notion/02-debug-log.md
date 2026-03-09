# BOJ 1927 — 디버깅 기록

## 주의점: 빈 힙 처리

`heappop` 전 `if heap` 검사 필수. 비어있으면 IndexError.

## 주의점: I/O 속도

`sys.stdin.readline` + `sys.stdout.write` 조합. `input()` + `print()` 조합은 $N = 10^5$에서 TLE 위험.

## 확인 과정

```bash
make -C problem test
```

PASS.
