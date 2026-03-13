# Attack Lab 시리즈 맵

## 프로젝트 개요

Code injection(phase 1-3)과 ROP(phase 4-5)로 target 함수를 호출하는 exploit 프로젝트.
raw payload 대신 payload structure validator로 학습 내용을 문서화했다.

## 타임라인

| 파일 | 기간 | 핵심 내용 |
|------|------|-----------|
| [1편](10-2026-03-08-to-2026-03-09.md) | 2026-03-08 ~ 03-09 | code injection phase 1-3, ROP phase 4-5, gadget chain 설계 |
| [2편](20-2026-03-10-to-2026-03-11.md) | 2026-03-10 ~ 03-11 | validator 정교화, byte order 가정, publication policy |

## 공개 경계

- gadget 주소와 payload shape는 설명하되, 외부 target에 직접 쓸 수 있는 raw exploit 배포 금지

## 검증 경로

```bash
cd problem && make verify-official
cd ../c && make test
```
