# Filesystem Mini-Lab 시리즈 맵

## 프로젝트 개요

Write-ahead logging(WAL)을 사용한 JSON 기반 미니 파일시스템.
prepare → commit → apply 세 단계와 crash injection으로 recovery를 테스트한다.

## 타임라인

| 파일 | 기간 | 핵심 내용 |
|------|------|-----------|
| [1편](10-2026-03-11.md) | 2026-03-11 | WAL 구조, crash_stage, recovery(committed but not applied), applied 플래그 |

## 검증 경로

```bash
cd python && pip install -e . && pytest tests/ -v
python -m os_mini_fs demo.img mkfs 8 16 && python -m os_mini_fs demo.img describe
```
