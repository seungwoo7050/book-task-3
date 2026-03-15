# backend-go 서버 캡스톤 문제지

`backend-go`의 capstone은 backend core와 platform 학습을 각각 끝내는 데서 멈추지 않고, 거래 일관성과 제품형 SaaS 흐름을 실제 제출 가능한 표면으로 다시 조합하게 만드는 종합 과제입니다.

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [17-game-store-capstone-go](17-game-store-capstone-go.md) | 시작 위치의 구현을 완성해 GET /v1/healthcheck, POST /v1/purchases, 구매 조회, 인벤토리 조회 API를 제공한다, Idempotency-Key 기반 중복 요청 안전 처리와 낙관적 잠금을 구현한다, purchase 성공 시 outbox row를 기록하고 relay가 발행을 이어받는다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/backend-go/study/04-capstone/17-game-store-capstone/solution/go test` |
| [18-workspace-saas-api-go](18-workspace-saas-api-go.md) | 시작 위치의 구현을 완성해 owner/admin/member RBAC가 있는 조직 단위 SaaS 도메인을 구현한다, POST /v1/auth/register-owner, 로그인/refresh/logout, invitation, project/issue/comment, notification, dashboard API를 제공한다, API와 worker가 별도 바이너리로 동작한다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/backend-go/study/05-portfolio-projects/18-workspace-saas-api/solution/go test` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
