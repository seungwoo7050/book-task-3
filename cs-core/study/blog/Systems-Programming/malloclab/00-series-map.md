# Malloc Lab 시리즈 맵

## 프로젝트 개요

Implicit explicit free list 기반 동적 메모리 할당기 구현.
`mm_malloc`, `mm_free`, `mm_realloc`을 coalesce와 함께 구현한다.

## 타임라인

| 파일 | 기간 | 핵심 내용 |
|------|------|-----------|
| [1편](10-2026-03-08-to-2026-03-09.md) | 2026-03-08 ~ 03-09 | block layout, header/footer, coalesce, alignment 버그 |
| [2편](20-2026-03-10-to-2026-03-11.md) | 2026-03-10 ~ 03-11 | realloc 최적화, mdriver 결과, explicit free list 고찰 |

## 구조

```
malloclab/
├── problem/          # official mdriver (local-only)
├── c/                # C companion
└── cpp/              # C++ companion
```

## 검증 경로

```bash
cd problem && ./mdriver -v -t traces/
cd ../c && make test
```
