# 08-production-readiness — 읽기 가이드

## 이 폴더의 구성

| 파일 | 설명 | 추천 독자 |
|------|------|-----------|
| **essay.md** | "코드 완성"에서 "운영 가능"까지의 간극을 다룬 에세이 — config, health check, structured logging, Docker | 운영 관점의 설계 판단을 이해하고 싶은 독자 |
| **timeline.md** | RuntimeConfig부터 Dockerfile까지의 개발 과정을 시간순 정리 | 직접 따라 만들거나, Docker 빌드·CI 설정 등 소스 코드 밖 작업을 알고 싶은 독자 |

## 추천 읽기 순서

1. **essay.md** — 왜 config를 fail-fast로 검증하는지, health/ready 엔드포인트의 차이, 구조화된 로깅의 필요성을 먼저 파악한다.
2. **timeline.md** — Dockerfile 멀티스테이지 빌드, 환경변수 주입, CI 초안 등 소스 밖 과정을 확인한다.
3. **소스 코드** — `runtime/` 디렉토리와 `health.controller.ts`를 중심으로 읽는다.

## 관련 프로젝트

- **07-domain-events**: 이전 프로젝트, 이벤트 시스템 위에 운영 계층을 쌓음
- **09-platform-capstone**: 다음 프로젝트, 지금까지의 모든 것을 통합하는 캡스톤
- **10-shippable-backend-service**: Docker Compose, Postgres, Redis를 사용하는 최종 프로젝트
