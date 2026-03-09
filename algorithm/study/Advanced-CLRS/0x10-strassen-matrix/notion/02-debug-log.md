# 0x10 Strassen Matrix — 디버깅 기록

## 함정 1: 패딩

비정방/비2의거듭제곱 크기 → `next_pow2`로 패딩 후 결과 trim.

## 함정 2: 베이스 케이스 임계값

$n=1$이면 단일 원소 곱셈. $n \leq 2$에서 naive로 전환하는 것이 실용적.

## 확인

```bash
make -C problem test
```

PASS.
