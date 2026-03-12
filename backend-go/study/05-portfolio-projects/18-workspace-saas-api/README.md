# 18 Workspace SaaS API

## 한 줄 요약

JWT auth, 조직 단위 RBAC, async notification, Redis cache를 한 제품형 API로 묶은 대표 포트폴리오 과제다.

## 이 프로젝트가 푸는 문제

- 채용 제출용 B2B SaaS API를 로컬에서 완결형으로 재현할 수 있어야 한다.
- JWT access/refresh, 조직 단위 RBAC, invitation, issue workflow, notification을 한 제품형 흐름으로 연결해야 한다.
- 기존 학습 프로젝트를 runtime dependency로 import하지 않고 새 프로젝트 내부에서 재소유해야 한다.

## 내가 만든 답

- API server, worker, Postgres repository, Redis cache/session store, OpenAPI, e2e, smoke를 `solution/go`에 구현했다.
- owner/admin/member RBAC와 invitation, project/issue/comment 흐름을 제품형 도메인으로 묶었다.
- Postgres + Redis 기반 local reproducibility와 smoke script를 README 표면에 올렸다.

## 핵심 설계 선택

- 이전 과제 코드를 의존성으로 가져오지 않고 대표작 내부에서 다시 소유해 제출용 완성도를 높였다.
- worker와 API를 바이너리 수준에서 분리해 async notification과 web request 경계를 명확히 했다.

## 검증

- `cd solution/go && go test ./...`
- `cd solution/go && make e2e`
- `cd solution/go && make smoke`
- `make -C study test-portfolio-unit`
- `make -C study test-portfolio-repro`

## 제외 범위

- Helm/GitOps 배포 자산
- microservice 분리

## 읽는 순서

1. [problem/README.md](problem/README.md)에서 canonical 문제 정의와 성공 기준을 읽는다.
2. [solution/README.md](solution/README.md)에서 구현 범위와 검증 진입점을 확인한다.
3. [docs/README.md](docs/README.md)에서 개념 설명과 참고 문서를 따라간다.
4. [notion/README.md](notion/README.md)에서 접근 로그, 디버그 기록, 회고를 확인한다.

## 상태

- 상태: `verified`
- 제공 자료와 provenance: `study`에서 새로 추가한 대표 포트폴리오 과제
