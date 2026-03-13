# Shell Lab 시리즈 맵

## 프로젝트 개요

SIGCHLD, SIGINT, SIGTSTP를 처리하는 tiny shell(tsh) 구현.
foreground/background job, job table, signal handler를 올바르게 연결한다.

## 타임라인

| 파일 | 기간 | 핵심 내용 |
|------|------|-----------|
| [1편](10-2026-03-08-to-2026-03-09.md) | 2026-03-08 ~ 03-09 | SIGCHLD handler, sigsuspend waitfg, do_bgfg %jid/pid 파싱 |
| [2편](20-2026-03-10-to-2026-03-11.md) | 2026-03-10 ~ 03-11 | process group kill, fork-addjob race, signal block |

## 검증 경로

```bash
cd problem && make verify-official
cd ../c && make test
```
