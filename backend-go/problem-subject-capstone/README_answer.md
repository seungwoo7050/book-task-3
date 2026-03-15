# backend-go 서버 캡스톤 답안지

이 문서는 Go 트랙의 capstone 두 개를 실제 통합 소스 기준으로 정리한 답안지다. 첫 capstone은 게임 상점 구매 흐름 하나에 transaction retry, idempotency, outbox relay를 통합한 기준선이고, 두 번째 capstone은 JWT auth, RBAC, Postgres, Redis, async worker를 갖춘 SaaS API를 포트폴리오 수준 표면으로 끌어올린다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [17-game-store-capstone-go](17-game-store-capstone-go_answer.md) | 시작 위치의 구현을 완성해 GET /v1/healthcheck, POST /v1/purchases, 구매 조회, 인벤토리 조회 API를 제공한다, Idempotency-Key 기반 중복 요청 안전 처리와 낙관적 잠금을 구현한다, purchase 성공 시 outbox row를 기록하고 relay가 발행을 이어받는다를 한 흐름으로 설명하고 검증한다. 핵심은 main와 Load, getEnv 흐름을 구현하고 테스트를 통과시키는 것이다. | `make -C /Users/woopinbell/work/book-task-3/backend-go/study/04-capstone/17-game-store-capstone/solution/go test` |
| [18-workspace-saas-api-go](18-workspace-saas-api-go_answer.md) | 시작 위치의 구현을 완성해 owner/admin/member RBAC가 있는 조직 단위 SaaS 도메인을 구현한다, POST /v1/auth/register-owner, 로그인/refresh/logout, invitation, project/issue/comment, notification, dashboard API를 제공한다, API와 worker가 별도 바이너리로 동작한다를 한 흐름으로 설명하고 검증한다. 핵심은 main와 applyFiles, SignAccessToken 흐름을 구현하고 테스트를 통과시키는 것이다. | `make -C /Users/woopinbell/work/book-task-3/backend-go/study/05-portfolio-projects/18-workspace-saas-api/solution/go test` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
