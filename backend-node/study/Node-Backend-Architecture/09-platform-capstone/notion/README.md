# 09-platform-capstone — 읽기 가이드

## 이 폴더의 구성

| 파일 | 설명 | 추천 독자 |
|------|------|-----------|
| **essay.md** | REST + Pipeline + Auth + Persistence + Events를 단일 NestJS 서비스로 통합하는 과정과 설계 판단 | 개별 프로젝트를 학습한 뒤 전체 아키텍처를 조감하고 싶은 독자 |
| **timeline.md** | 모듈 통합, 전체 E2E 테스트 설계, 검증 흐름을 시간순 정리 | 통합 과정의 순서와 접착 코드를 이해하고 싶은 독자 |

## 추천 읽기 순서

1. **essay.md** — 각 프로젝트(03~08)에서 만든 모듈이 어떻게 하나로 합쳐지는지, 통합 시 발생하는 설계 결정을 먼저 파악한다.
2. **timeline.md** — 모듈별 통합 순서, RBAC + 이벤트 확장, 캡스톤 E2E 테스트 시나리오를 확인한다.
3. **소스 코드** — `app.module.ts`에서 전체 모듈 의존성 그래프를 확인하고, `capstone.e2e.test.ts`에서 통합 시나리오를 읽는다.

## 관련 프로젝트

- **03~08**: 이 프로젝트에 통합된 개별 프로젝트들
- **10-shippable-backend-service**: 다음 프로젝트, Postgres + Redis + Docker Compose로 확장한 최종 버전
