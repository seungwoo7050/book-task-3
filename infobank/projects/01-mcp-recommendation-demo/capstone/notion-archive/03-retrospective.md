> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../docs/catalog/path-migration-map.md)를 본다.

# 03 — 회고: 4단계 반복으로 시스템을 키우기

## 잘된 점

### 1. 버전별 독립 실행 가능

v0, v1, v2, v3 각각이 독립적으로 `pnpm install && pnpm dev`로 실행된다.  
이전 버전을 깨뜨리지 않으면서 다음 버전을 추가하는 것이 가능했다.  
이것은 "하나의 코드베이스를 계속 리팩터링"하는 것과 근본적으로 다른 접근이다.

각 버전을 별도 디렉토리로 유지한 것은 비용이 크지만 (코드 중복), 실습·학습 관점에서는 최적이다.  
"v1에서 뭐가 달라졌지?"를 diff로 확인할 수 있다.

### 2. Zod 스키마가 진짜 "단일 진실 소스" 역할을 했다

shared 패키지에 Zod 스키마를 넣고, API와 프론트엔드가 모두 같은 타입을 쓰는 구조는 기대 이상으로 잘 동작했다.  
v3에서 `ReleaseCandidate`에 `owner` 필드를 추가했을 때, shared에만 변경하면 API와 대시보드 모두에서 타입 에러가 즉시 발생한다.

### 3. pg-boss 선택으로 Redis를 제거

BullMQ를 쓰면 Redis가 필요하다.  
pg-boss는 PostgreSQL에 job queue를 저장하므로, 이미 있는 DB 하나로 해결된다.  
인프라 복잡도를 줄이는 것이 self-hosted 시나리오에서는 매우 중요한 결정이었다.

### 4. Docker Compose가 "설치 가이드"를 대체

v3에서 `docker compose up -d --build` 하나로 전체 시스템이 올라간다.  
"PostgreSQL 설치하고, Node.js 버전 맞추고, 환경변수 설정하고…" 같은 설치 가이드가 compose 파일 하나로 줄어든다.

### 5. Audit Log가 회고의 원천 자료

v3의 audit log는 "누가 언제 catalog를 수정했는지, 언제 release gate를 통과했는지"를 자동으로 기록한다.  
이것은 운영 도구이기도 하지만, 이 회고 문서를 작성할 때도 도움이 되었다.

## 개선이 필요한 점

### 1. v0-v3 간 코드 중복이 심하다

shared 패키지의 `catalog.ts`, `contracts.ts`, `eval.ts`가 모든 버전에 복사되어 있다.  
v0에서 버그를 발견하면 v1, v2, v3에서도 같은 수정을 해야 한다.

**개선 방향**: shared를 별도 npm 패키지로 발행하고 각 버전이 의존하는 방식.  
하지만 그렇게 하면 "v0만 따로 실행"이 어려워진다 — 트레이드오프.

### 2. 테스트 커버리지 격차

v0, v1: unit test + integration test가 핵심 로직을 커버.  
v2: e2e test 추가로 대시보드까지 자동 검증.  
v3: auth/RBAC 테스트는 있지만, worker + audit log 조합의 통합 테스트가 부족하다.

"pg-boss job이 실패했을 때 audit log에 실패가 기록되는가?" 같은 시나리오가 수동 확인에 의존한다.

### 3. 환경변수 관리의 산발적 구조

`.env.example`이 있지만, 각 버전마다 필요한 환경변수가 조금씩 다르다.  
v0는 `DATABASE_URL`만 필요하고, v3는 `SESSION_SECRET`, `BOOTSTRAP_OWNER_EMAIL` 등이 추가된다.  
버전별 `.env.example` 차이를 문서화하지 않으면 실행 시 혼란이 생긴다.

### 4. 한국어 하드코딩의 한계

모든 한국어 텍스트(explanationKo, summaryKo, UI 레이블)가 소스 코드에 직접 들어 있다.  
국제화(i18n) 지원이 필요하면 전면 리팩터링이 불가피하다.  
이 프로젝트의 범위에서는 적절하지만, OSS로 공개할 때는 고려 사항이다.

### 5. migration 실행 순서 의존성

Docker Compose에서 api 컨테이너가 부팅 시 migration을 실행한다.  
worker는 api가 started 상태가 되면 시작하지만, migration이 완료되었는지는 보장하지 않는다.  
결과적으로 worker가 아직 없는 테이블에 접근하려다 실패할 수 있다.

**개선 방향**: api 컨테이너의 healthcheck에 "migration 완료" 상태를 포함하거나, worker에 retry 로직을 추가.

## 핵심 교훈

> 시스템은 "처음부터 완벽하게" 만드는 것이 아니라,  
> "동작하는 최소 버전"에서 시작해서 증거 기반으로 개선하는 것이다.  
> v0의 baseline selector가 없었으면 v1의 reranker가 의미 없었고,  
> v1의 compare가 없었으면 v2의 release gate가 무엇을 판단해야 하는지 모른다.

각 버전의 "이전 대비 개선 증거"가 다음 버전의 설계 근거가 되는 피드백 루프가  
이 프로젝트의 가장 큰 성과였다.
