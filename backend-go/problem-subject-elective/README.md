# backend-go 서버 개발 비필수 문제지

여기서 `비필수`는 중요하지 않다는 뜻이 아니라, 서버 공통 필수보다 Go 웹 백엔드 문맥 의존성이 더 강하다는 뜻입니다.
이 트랙의 종합 과제는 [`../problem-subject-capstone/README.md`](../problem-subject-capstone/README.md)로 분리합니다.

## Go Fundamentals

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [01-go-syntax-and-tooling-go](01-go-syntax-and-tooling-go.md) | 시작 위치의 구현을 완성해 입력 문자열을 소문자 단어 목록으로 정규화한다, 단어 빈도를 계산한다, 가장 많이 나온 단어를 찾는다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-go/study/00-go-fundamentals/01-go-syntax-and-tooling/solution/go && GOWORK=off go test ./...` |
| [02-types-errors-interfaces-go](02-types-errors-interfaces-go.md) | 시작 위치의 구현을 완성해 SKU 중복 추가를 막는다, 존재하지 않는 상품 조회 시 custom error를 반환한다, 할인 규칙을 interface로 분리한다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-go/study/00-go-fundamentals/02-types-errors-interfaces/solution/go && GOWORK=off go test ./...` |
| [03-testing-and-debugging-go](03-testing-and-debugging-go.md) | 시작 위치의 구현을 완성해 "category,duration_ms" 형식의 라인을 파싱한다, category별 평균 지연 시간을 계산한다, concurrent append가 가능한 recorder를 만든다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-go/study/00-go-fundamentals/03-testing-and-debugging/solution/go && GOWORK=off go test ./...` |
| [04-sql-and-data-modeling-go](04-sql-and-data-modeling-go.md) | 시작 위치의 구현을 완성해 players, items, inventory 테이블을 만든다, FK와 unique constraint를 사용한다, join query로 플레이어 인벤토리를 조회한다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/04-sql-and-data-modeling/solution/go && GOWORK=off go test ./...` |
| [05-http-rest-basics-go](05-http-rest-basics-go.md) | 시작 위치의 구현을 완성해 GET /v1/healthcheck, POST /v1/tasks, GET /v1/tasks를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/05-http-rest-basics/solution/go && GOWORK=off go test ./...` |
| [06-go-api-standard-go](06-go-api-standard-go.md) | 시작 위치의 구현을 완성해 GET /v1/healthcheck와 Movie CRUD API를 제공한다, 모든 응답이 일관된 JSON envelope 구조를 따른다, 입력 검증, pagination, request logging, panic recovery, CORS를 포함한다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/06-go-api-standard/problem test` |
| [07-auth-session-jwt-go](07-auth-session-jwt-go.md) | 시작 위치의 구현을 완성해 비밀번호는 평문으로 저장하지 않는다, 세션 로그인 후 보호 리소스 접근이 가능해야 한다, JWT 로그인 후 보호 리소스 접근이 가능해야 한다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/07-auth-session-jwt/solution/go && GOWORK=off go test ./...` |
| [08-sql-store-api-go](08-sql-store-api-go.md) | 시작 위치의 구현을 완성해 migration up/down 파일을 둔다, POST /v1/products, GET /v1/products를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/08-sql-store-api/solution/go && GOWORK=off go test ./...` |
| [09-cache-migrations-observability-go](09-cache-migrations-observability-go.md) | 시작 위치의 구현을 완성해 migration up/down이 가능해야 한다, GET /v1/items/{id}와 PUT /v1/items/{id}를 제공한다, /metrics를 노출한다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/09-cache-migrations-observability/solution/go && GOWORK=off go test ./...` |
| [11-rate-limiter-go](11-rate-limiter-go.md) | 시작 위치의 구현을 완성해 Token Bucket이 refill rate와 burst를 지원한다, Allow()가 thread-safe하게 동작한다, per-client limiter가 IP 기준으로 분리된다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/11-rate-limiter/problem test` |
| [12-grpc-microservices-go](12-grpc-microservices-go.md) | 시작 위치의 구현을 완성해 Product CRUD와 리스트/가격 감시용 RPC를 정의한다, logging interceptor와 auth interceptor를 구현한다, client retry interceptor와 round-robin 예제를 제공한다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/backend-go/study/02-distributed-systems/12-grpc-microservices/problem test` |
| [13-distributed-log-core-go](13-distributed-log-core-go.md) | 시작 위치의 구현을 완성해 length-prefixed record store를 구현한다, offset -> position을 매핑하는 fixed-width mmap index를 구현한다, segment가 base offset과 next offset을 관리하며 full 상태를 판정한다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/backend-go/study/02-distributed-systems/13-distributed-log-core/problem test` |
| [14-cockroach-tx-go](14-cockroach-tx-go.md) | 시작 위치의 구현을 완성해 players, inventory, idempotency_keys, audit_log 중심 스키마를 구성한다, 잔액 차감이 optimistic locking으로 동작한다, idempotency key가 이전 응답을 재사용한다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/backend-go/study/03-platform-engineering/14-cockroach-tx/problem test` |
| [16-gitops-deploy](16-gitops-deploy.md) | 시작 위치의 구현을 완성해 multi-stage Dockerfile을 작성한다, Helm chart에 Deployment, Service, ConfigMap, Secret, HPA 등을 포함한다, ArgoCD Application manifest를 제공한다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/backend-go/study/03-platform-engineering/16-gitops-deploy/problem helm-lint` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
