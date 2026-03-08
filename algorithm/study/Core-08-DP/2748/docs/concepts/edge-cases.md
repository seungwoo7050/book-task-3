# Edge Cases — BOJ 2748 Fibonacci 2

## 1. n = 0
$F(0) = 0$.

## 2. n = 1
$F(1) = 1$.

## 3. n = 90
$F(90) = 2880067194370816120$ — 64비트 초과, Python은 자동 처리.

## 핵심 주의점
- C++에서는 `long long` 필수 (64비트까지), 90이면 넘을 수 있음
- Python은 BigInt 자동 지원
