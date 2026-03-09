# 0x17 Number Theory Lab — 디버깅 기록

## egcd 음수 계수

확장 유클리드 결과 x, y가 음수일 수 있음. modinv에서 `% m` 필수.

## CRT 오버플로

Python은 big integer이므로 걱정 없으나, C/C++에서는 128비트 연산 필요.

## 테스트

```bash
make -C problem test
```

PASS.
