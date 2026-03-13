# Architecture Lab 시리즈 맵

## 프로젝트 개요

Y86 어셈블리(Part A), SEQ HCL 확장(Part B), ncopy 성능 최적화(Part C).
공식 toolchain은 local-only. 공개 저장소에는 C/C++ companion과 검증 경로를 둔다.

## 타임라인

| 파일 | 기간 | 핵심 내용 |
|------|------|-----------|
| [1편](10-2026-03-08-to-2026-03-09.md) | 2026-03-08 ~ 03-09 | Part A-C, iaddq HCL, 4-way unroll, pseudo-CPE 모델 |
| [2편](20-2026-03-10-to-2026-03-11.md) | 2026-03-10 ~ 03-11 | 공식 benchmark (CPE 9.16), 8-way 제한, C++ companion |

## 구조

```
archlab/
├── problem/          # official starter (local-only)
├── c/                # C companion
├── cpp/              # C++ companion
└── docs/
```

## 검증 경로

```bash
cd problem && make verify-official
cd ../c && make test
cd ../cpp && make test
```
