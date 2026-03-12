# backend-go

이 저장소는 Go 백엔드 학습 결과물을 단순 코드 묶음이 아니라 `문제 정의 -> 답안 구현 -> 설계 근거 -> 재현 기록` 순서로 읽히게 정리한 study-first 공개 레포다. 목표는 “무슨 문제를 풀었고, 어떻게 풀었고, 어디까지 검증했는지”를 GitHub 첫 화면에서 바로 이해할 수 있게 만드는 것이다.

## 이 레포가 푸는 문제

- Go 문법부터 백엔드 코어, 분산 시스템, 플랫폼 엔지니어링, capstone, 포트폴리오까지를 한 저장소 안에서 길을 잃지 않고 읽기 어렵다는 문제
- 학습 레포가 시간이 지나면 “그래서 무슨 문제를 풀었고 답이 뭔데?”가 흐려진다는 문제
- 코드만 있고 검증 경로와 학습 근거가 분리돼 있지 않아 재진입과 포트폴리오 활용이 동시에 어려운 문제

## 내가 만든 답

- 상위 커리큘럼은 `study/<track>/<project>`로 유지하고, 각 프로젝트 내부를 `problem/`, `solution/`, `docs/`, `notion/`으로 다시 정렬했다.
- 각 프로젝트는 `README -> problem -> solution -> docs -> notion` 순서로 읽히게 만들었다.
- 구현 경로는 `solution/go` 또는 `solution/infra`로 통일했고, 문제 정의와 답안 요약을 폴더 수준에서 분리했다.
- 루트와 트랙 README는 포트폴리오 우선 시선으로 다시 작성해 대표작, 전체 커리큘럼, 검증 진입점을 바로 드러낸다.

## 대표작

| 프로젝트 | 푸는 문제 | 답안 표면 | 대표 검증 |
| --- | --- | --- | --- |
| [13 Distributed Log Core](study/02-distributed-systems/13-distributed-log-core/README.md) | length-prefixed store와 fixed-width index를 직접 구현해야 한다. | [`solution/README.md`](study/02-distributed-systems/13-distributed-log-core/solution/README.md) | `cd solution/go && go test ./log/... -bench=.`, `make -C problem test` |
| [15 Event Pipeline](study/03-platform-engineering/15-event-pipeline/README.md) | DB write와 Kafka publish 사이의 정합성 문제를 outbox로 해결해야 한다. | [`solution/README.md`](study/03-platform-engineering/15-event-pipeline/solution/README.md) | `make -C problem build`, `make -C problem test` |
| [17 Game Store Capstone](study/04-capstone/17-game-store-capstone/README.md) | 잔액 차감, 인벤토리 반영, 구매 기록 저장, outbox 기록을 하나의 흐름으로 묶어야 한다. | [`solution/README.md`](study/04-capstone/17-game-store-capstone/solution/README.md) | `cd solution/go && mkdir -p ./bin && go build -o ./bin/api ./cmd/api`, `cd solution/go && go test ./...` |
| [18 Workspace SaaS API](study/05-portfolio-projects/18-workspace-saas-api/README.md) | 채용 제출용 B2B SaaS API를 로컬에서 완결형으로 재현할 수 있어야 한다. | [`solution/README.md`](study/05-portfolio-projects/18-workspace-saas-api/solution/README.md) | `cd solution/go && go test ./...`, `cd solution/go && make e2e` |

## 전체 커리큘럼

| 번호 | 프로젝트 | 트랙 | 한 줄 설명 | 상태 |
| --- | --- | --- | --- | --- |
| 01 | [01-go-syntax-and-tooling](study/00-go-fundamentals/01-go-syntax-and-tooling/README.md) | 00 Go Fundamentals | Go 문법과 `go run` / `go test` 루프를 가장 작은 문자열 처리 과제로 익히는 시작점이다. | `verified` |
| 02 | [02-types-errors-interfaces](study/00-go-fundamentals/02-types-errors-interfaces/README.md) | 00 Go Fundamentals | struct, method, interface, custom error를 작은 상품 카탈로그로 묶어 타입 감각을 붙이는 과제다. | `verified` |
| 03 | [03-testing-and-debugging](study/00-go-fundamentals/03-testing-and-debugging/README.md) | 00 Go Fundamentals | table-driven test, subtest, benchmark, race detector를 로그 파서와 recorder 구현으로 익히는 입문 심화 과제다. | `verified` |
| 04 | [04-sql-and-data-modeling](study/01-backend-core/04-sql-and-data-modeling/README.md) | 01 Backend Core | 스키마 설계, join, transaction을 게임 상점 예제로 묶어 SQL 기초를 백엔드 문맥에서 익히는 브리지 과제다. | `verified` |
| 05 | [05-http-rest-basics](study/01-backend-core/05-http-rest-basics/README.md) | 01 Backend Core | 작은 JSON API를 통해 상태 코드, validation, pagination, idempotency 기본 감각을 익히는 브리지 과제다. | `verified` |
| 06 | [06-go-api-standard](study/01-backend-core/06-go-api-standard/README.md) | 01 Backend Core | 표준 라이브러리만으로 REST API, middleware, JSON envelope, graceful shutdown을 정리하는 본선 과제다. | `verified` |
| 07 | [07-auth-session-jwt](study/01-backend-core/07-auth-session-jwt/README.md) | 01 Backend Core | session login과 JWT login을 함께 구현해 인증 방식과 인가 경계를 비교하는 브리지 과제다. | `verified` |
| 08 | [08-sql-store-api](study/01-backend-core/08-sql-store-api/README.md) | 01 Backend Core | SQLite 기반 CRUD API에 migration, optimistic update, transaction rollback을 결합한 백엔드 코어 중심 과제다. | `verified` |
| 09 | [09-cache-migrations-observability](study/01-backend-core/09-cache-migrations-observability/README.md) | 01 Backend Core | cache-aside, cache invalidation, migration, metrics, trace header를 한 API로 묶어 운영 기본기를 붙이는 과제다. | `verified` |
| 10 | [10-concurrency-patterns](study/01-backend-core/10-concurrency-patterns/README.md) | 01 Backend Core | worker pool과 pipeline을 통해 goroutine lifecycle, channel, cancellation을 직접 다루는 본선 과제다. | `verified` |
| 11 | [11-rate-limiter](study/01-backend-core/11-rate-limiter/README.md) | 01 Backend Core | Token Bucket과 per-client limiter를 HTTP middleware까지 연결해 백엔드 보호 기초를 익히는 과제다. | `verified` |
| 12 | [12-grpc-microservices](study/02-distributed-systems/12-grpc-microservices/README.md) | 02 Distributed Systems | Protocol Buffers, unary/streaming RPC, interceptor를 작은 Product Catalog 서비스로 묶어 contract-first 감각을 익히는 과제다. | `verified` |
| 13 | [13-distributed-log-core](study/02-distributed-systems/13-distributed-log-core/README.md) | 02 Distributed Systems | append-only store, mmap index, segment rotation, log abstraction을 직접 구현해 commit log 핵심을 익히는 대표 과제다. | `verified` |
| 14 | [14-cockroach-tx](study/03-platform-engineering/14-cockroach-tx/README.md) | 03 Platform Engineering | idempotency key, optimistic locking, transaction retry를 CockroachDB 호환 흐름으로 묶어 정합성 기초를 다지는 과제다. | `verified` |
| 15 | [15-event-pipeline](study/03-platform-engineering/15-event-pipeline/README.md) | 03 Platform Engineering | outbox pattern, relay, idempotent consumer를 통해 DB 정합성과 비동기 전달 경계를 함께 다루는 대표 과제다. | `verified` |
| 16 | [16-gitops-deploy](study/03-platform-engineering/16-gitops-deploy/README.md) | 03 Platform Engineering | Docker multi-stage build, Helm chart, ArgoCD manifest를 통해 코드 자산을 배포 자산으로 번역하는 인프라 과제다. | `verified` |
| 17 | [17-game-store-capstone](study/04-capstone/17-game-store-capstone/README.md) | 04 Capstone | 거래 일관성, outbox, 운영 기본 요소를 하나의 게임 상점 API로 통합한 필수 capstone이다. | `verified` |
| 18 | [18-workspace-saas-api](study/05-portfolio-projects/18-workspace-saas-api/README.md) | 05 Portfolio Projects | JWT auth, 조직 단위 RBAC, async notification, Redis cache를 한 제품형 API로 묶은 대표 포트폴리오 과제다. | `verified` |

## 검증 상태

- 현재 18개 프로젝트의 공개 상태 표시는 모두 `verified` 기준으로 정리했다.
- 루트 기준 재검증 진입점은 `study/Makefile`에 모아 둔다.
- 대표 명령은 아래와 같다.

```bash
cd study
make test-new
make test-migrated
make test-infra
make test-runtime
make test-portfolio-unit
make test-portfolio-repro
```

## 읽는 순서

1. [docs/README.md](docs/README.md)에서 저장소 규칙과 템플릿을 확인한다.
2. [study/README.md](study/README.md)에서 전체 트랙 지도를 읽는다.
3. 대표작 네 개 중 관심 있는 프로젝트의 `README.md`를 먼저 읽는다.
4. 같은 프로젝트의 `problem/README.md`에서 canonical 문제 정의를 확인한다.
5. `solution/README.md`, `docs/README.md`, `notion/README.md` 순서로 구현, 개념, 시행착오를 따라간다.

## 의도적으로 제외한 범위

- 운영 환경에서의 대규모 멀티 리전 설계
- 서비스 메시, 고급 분산 트레이싱, 복잡한 OAuth federation
- product-scale SRE 운영 절차 전부
- 무분별한 프로젝트 수 확장과 중복 과제 추가
