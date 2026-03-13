# Bomb Lab 시리즈 맵

## 프로젝트 개요

역공학으로 6개 phase + secret phase를 해제하는 CTF형 프로젝트.
정답 문자열 대신 phase 패턴을 C/C++ companion으로 표현했다.

## 타임라인

| 파일 | 기간 | 핵심 내용 |
|------|------|-----------|
| [1편](10-2026-03-08-to-2026-03-09.md) | 2026-03-08 ~ 03-09 | phase 1-6, secret phase, companion mini-bomb 설계 |
| [2편](20-2026-03-10-to-2026-03-11.md) | 2026-03-10 ~ 03-11 | fun7 path code 설명, publication policy |

## 공개 경계

- 정답 문자열은 최소한만 문서화, companion 코드가 패턴을 설명
- official binary answers: local-only

## 검증 경로

```bash
cd problem && make verify-official
cd ../c && make test
```
