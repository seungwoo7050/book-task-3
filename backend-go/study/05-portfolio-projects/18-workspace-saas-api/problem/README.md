# 문제 정의

웹 백엔드 공고에 제출할 수 있는 대표 포트폴리오용 B2B SaaS API를 만든다.

## 성공 기준

- owner/admin/member RBAC가 있는 조직 단위 SaaS 도메인을 구현한다.
- `POST /v1/auth/register-owner`, 로그인/refresh/logout, invitation, project/issue/comment, notification, dashboard API를 제공한다.
- API와 worker가 별도 바이너리로 동작한다.
- Postgres + Redis 기반으로 `e2e`와 `smoke` 검증이 가능해야 한다.
- 기존 학습 프로젝트를 runtime dependency로 import하지 않는다.

## 제공 자료와 출처

- `study`에서 새로 설계한 대표 포트폴리오 canonical 문제다.
- 이 문서가 공개용 문제 정의다.
- 공개 구현은 [`solution/README.md`](../solution/README.md)와 `solution/go`에 둔다.

## 검증 기준

- `cd solution/go && go test ./...`
- `cd solution/go && make e2e`
- `cd solution/go && make smoke`

## 제외 범위

- Helm/GitOps 배포 자산
- MSA 분리
