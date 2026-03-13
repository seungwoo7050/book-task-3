# Data Lab 시리즈 맵

## 프로젝트 개요

비트 연산과 부동소수점 표현을 제한된 연산자 집합으로 구현하는 퍼즐 시리즈.
공식 CSAPP Data Lab을 self-study 방식으로 진행하면서 C와 C++ companion을 함께 작성했다.

## 타임라인

| 파일 | 기간 | 핵심 내용 |
|------|------|-----------|
| [1편](10-2026-03-08-to-2026-03-09.md) | 2026-03-08 ~ 03-09 | 정수 퍼즐 55개, C companion, isTmax/isTmax edge case, floatFloat2Int 분기 |
| [2편](20-2026-03-10-to-2026-03-11.md) | 2026-03-10 ~ 03-11 | C++ mirror, signed shift 가정, floatScale2 denorm→norm, 문서 구조 정리 |

## 구조

```
datalab/
├── problem/          # official starter (local-only)
├── c/                # C companion (공개)
├── cpp/              # C++ companion (공개)
└── docs/
```

## 검증 경로

```bash
cd problem && make verify-official
cd ../c && make test
cd ../cpp && make test
```
