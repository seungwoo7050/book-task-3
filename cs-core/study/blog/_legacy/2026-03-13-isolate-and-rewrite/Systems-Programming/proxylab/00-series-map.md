# Proxy Lab 시리즈 맵

## 프로젝트 개요

순차 처리 → 멀티스레드 → LRU 캐시를 순서대로 구현하는 HTTP proxy.
URI 파싱, header 재구성, thread-safe cache를 포함한다.

## 타임라인

| 파일 | 기간 | 핵심 내용 |
|------|------|-----------|
| [1편](10-2026-03-08-to-2026-03-09.md) | 2026-03-08 ~ 03-09 | URI 파싱, User-Agent 교체, thread per connection, LRU cache |
| [2편](20-2026-03-10-to-2026-03-11.md) | 2026-03-10 ~ 03-11 | SIGPIPE, mutex vs rwlock, concurrent 테스트 |

## 검증 경로

```bash
cd problem && make verify-official
cd ../c && make test
```
