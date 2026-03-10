# 0x15 String Matching — 디버깅 기록

## Rabin-Karp 음수 해시

`(h - ord(t[i]) * high)` 결과가 음수일 수 있음. `% mod` 적용 필수.

## KMP pi 배열 off-by-one

`range(1, m)` 시작. i=0은 항상 0.

## 테스트

```bash
make -C problem test
```

PASS. 두 모드 모두 동일한 매칭 위치 반환 확인.
