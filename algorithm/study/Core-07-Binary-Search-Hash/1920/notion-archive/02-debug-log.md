# BOJ 1920 — 디버깅 기록

## 특이사항

로직이 단순해서 주요 디버깅 이슈 없음.

## 주의점: I/O 속도

**증상**: TLE

**원인**: `input()` 대신 `sys.stdin.readline` 미사용

**해결**: 전역 `input = sys.stdin.readline` 설정

## 확인 과정

```bash
make -C problem test
```

PASS.
