# 0x15 String Matching — 개발 타임라인

## Phase 1: KMP 구현

prefix function 전처리 + 매칭 루프.

## Phase 2: Rabin-Karp 구현

rolling hash + 문자열 검증.

## Phase 3: CLI 통합

모드 분기 (KMP / RABIN).

## Phase 4: 테스트

```bash
make -C problem test
```

PASS.

## 사용 도구

- Python 3
- GNU Make
