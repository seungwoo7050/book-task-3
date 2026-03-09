# BOJ 10816 — 디버깅 기록

## 함정: 없는 카드에 대한 쿼리

**증상**: KeyError

**원인**: 일반 딕셔너리에서 존재하지 않는 키 접근

**해결**: `Counter`는 존재하지 않는 키에 0을 자동 반환하므로 문제 없음. 또는 `dict.get(q, 0)` 사용.

## 확인 과정

```bash
make -C problem test
```

PASS.
