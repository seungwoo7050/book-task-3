# Problem

## Goal

웹 백엔드 공고에 제출할 수 있는 대표 포트폴리오용 B2B SaaS API를 만든다.

## Product Shape

- 조직 단위 tenant boundary
- owner/admin/member RBAC
- JWT access token과 refresh token rotation
- 프로젝트, 이슈, 댓글, 알림, 대시보드 요약
- Postgres + Redis 기반 로컬 완결형 검증

## Required API Surface

- `POST /v1/auth/register-owner`
- `POST /v1/auth/login`
- `POST /v1/auth/refresh`
- `POST /v1/auth/logout`
- `GET /v1/me`
- `POST /v1/orgs/{orgID}/invitations`
- `POST /v1/invitations/accept`
- `GET /v1/orgs/{orgID}/projects`
- `POST /v1/orgs/{orgID}/projects`
- `GET /v1/projects/{projectID}/issues`
- `POST /v1/projects/{projectID}/issues`
- `PATCH /v1/issues/{issueID}`
- `POST /v1/issues/{issueID}/comments`
- `GET /v1/orgs/{orgID}/notifications`
- `GET /v1/orgs/{orgID}/dashboard/summary`
- `GET /healthz`
- `GET /readyz`
- `GET /metrics`

## Constraints

- 기존 학습 프로젝트를 runtime dependency로 import하지 않는다.
- 필요한 경우 기존 코드는 복사 후 새 프로젝트 내부에서 재소유한다.
- API와 worker는 별도 바이너리여야 한다.
- 대표작 검증은 docker compose + e2e + smoke 기준으로 끝나야 한다.
