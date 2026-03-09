# 08-production-readiness — 개발 타임라인

> 소스 코드에 남지 않는 개발 과정을 시간순으로 기록한다.

---

## Phase 1: 프로젝트 초기화

이 프로젝트부터 NestJS 단일 레인으로 진행한다. Express 레인 없음.

### 1-1. NestJS 프로젝트 설정

```bash
cd 08-production-readiness/nestjs
pnpm init
```

```bash
pnpm add @nestjs/common @nestjs/core @nestjs/platform-express reflect-metadata rxjs
pnpm add -D @nestjs/cli @nestjs/testing typescript @types/node vitest supertest @types/supertest
```

이 프로젝트는 better-sqlite3를 사용하지 않으므로 native 빌드 과정이 필요 없다. 순수 NestJS + 환경설정 + 로깅 + Docker.

### 1-2. 디렉토리 구조

```bash
mkdir -p src/runtime
```

`src/runtime/` — 런타임 설정, 로깅 인터셉터 등 운영 기반 코드를 모아놓는 디렉토리.

---

## Phase 2: 런타임 설정 시스템

### 2-1. RuntimeConfig 타입과 로더

`src/runtime/runtime-config.ts` 생성:

- `LogLevel` 타입: `"debug" | "info" | "warn" | "error"`
- `RuntimeConfig` 타입: `appName`, `environment`, `port`, `ready`, `logLevel`
- `parsePort()`, `parseReady()`, `parseLogLevel()` — 각각 파싱 + 유효성 검증
- `loadRuntimeConfig(env)` — 환경변수 객체를 받아 `RuntimeConfig` 반환

설계 결정: `process.env`를 직접 의존하지 않고 파라미터로 받는다 → 테스트에서 임의 환경변수 주입 가능.

### 2-2. Symbol 토큰

`src/runtime/runtime.constants.ts` 생성:

```typescript
export const RUNTIME_CONFIG = Symbol("RUNTIME_CONFIG");
```

문자열 대신 Symbol을 사용하면 토큰 충돌 위험이 없다.

### 2-3. RuntimeConfigService

`src/runtime/runtime-config.service.ts` 생성:

- `@Injectable()` + `@Inject(RUNTIME_CONFIG)`
- `get snapshot(): RuntimeConfig` — 설정 값 읽기 전용 접근

### 2-4. AppModule에서 provider 등록

`src/app.module.ts`:

```typescript
{
  provide: RUNTIME_CONFIG,
  useFactory: () => loadRuntimeConfig(process.env),
},
RuntimeConfigService,
```

`useFactory`를 쓰는 이유: 앱 시작 시 `loadRuntimeConfig`가 실행되어 fail-fast 검증이 동작한다.

---

## Phase 3: Health Check 엔드포인트

### 3-1. HealthController

`src/health.controller.ts` 생성:

- `GET /health` — 항상 200 반환. `status: "ok"`, `appName`, `environment`, `timestamp`.
- `GET /ready` — `config.ready`가 false이면 503 (`ServiceUnavailableException`).

수동 검증:

```bash
pnpm run start

# health 확인
curl http://localhost:3000/health
# {"status":"ok","appName":"production-readiness-app","environment":"development","timestamp":"..."}

# readiness 확인 (기본값 READY=true)
curl http://localhost:3000/ready
# {"status":"ready","appName":"production-readiness-app","environment":"development"}

# readiness 비활성화
READY=false pnpm run start
curl -v http://localhost:3000/ready
# HTTP 503
```

---

## Phase 4: 구조화된 로깅 인터셉터

### 4-1. StructuredLoggingInterceptor

`src/runtime/structured-logging.interceptor.ts` 생성:

- `NestInterceptor` 구현
- HTTP 요청만 처리 (`context.getType() !== "http"` 체크)
- `x-request-id` 헤더 읽기/전파
- `Date.now()` 기반 응답 시간 측정
- 성공/실패 모두 로깅 (`tap({ next, error })`)
- `process.stdout.write(JSON.stringify(payload) + "\n")` — 한 줄 JSON 출력

### 4-2. 전역 인터셉터 등록

`app.module.ts`에서 `APP_INTERCEPTOR` 토큰으로 등록:

```typescript
{
  provide: APP_INTERCEPTOR,
  inject: [RuntimeConfigService],
  useFactory: (runtimeConfig: RuntimeConfigService) => {
    return new StructuredLoggingInterceptor(runtimeConfig);
  },
}
```

`main.ts`의 `useGlobalInterceptors()` 대신 이 방식을 택한 이유: DI 컨텍스트 내에서 생성되므로 `RuntimeConfigService`를 주입받을 수 있다.

수동 검증:

```bash
pnpm run start

curl http://localhost:3000/health
# stdout에 JSON 로그 출력:
# {"level":"info","appName":"production-readiness-app","environment":"development","requestId":"generated-request-id","method":"GET","path":"/health","statusCode":200,"durationMs":2,"outcome":"ok"}

# x-request-id 전달 테스트
curl -H "x-request-id: my-trace-id" http://localhost:3000/health
# 응답 헤더에 x-request-id: my-trace-id 포함
# 로그에 "requestId":"my-trace-id" 포함
```

---

## Phase 5: Docker 컨테이너화

### 5-1. Dockerfile 작성

`nestjs/Dockerfile` 생성:

멀티스테이지 빌드:
- **빌드 스테이지**: `node:22-alpine`, pnpm 활성화, TypeScript 빌드
- **런타임 스테이지**: `node:22-alpine`, dist/와 node_modules만 복사

```bash
# Docker 이미지 빌드
docker build -t production-readiness .

# 이미지 크기 확인
docker images production-readiness
# ~150MB (alpine)

# 컨테이너 실행
docker run -p 3000:3000 \
  -e NODE_ENV=production \
  -e APP_NAME=my-service \
  -e LOG_LEVEL=info \
  production-readiness

# 외부에서 health check
curl http://localhost:3000/health
```

### 5-2. .dockerignore (권장)

```
node_modules
dist
*.md
```

빌드 컨텍스트에서 불필요한 파일을 제외하여 빌드 속도를 높인다.

---

## Phase 6: 테스트

### 6-1. 단위 테스트 — RuntimeConfig

`tests/unit/runtime-config.test.ts`:

```bash
pnpm run test
```

- 빈 객체로 호출 시 기본값 검증
- 명시적 값 파싱 검증
- 잘못된 PORT 입력 시 예외 발생 검증

### 6-2. E2E 테스트

`tests/e2e/health.e2e.test.ts`:

```bash
pnpm run test:e2e
```

- `process.env` 직접 패치 → 테스트 앱 생성
- `/health` 응답 200 검증
- `READY=false` 시 `/ready` 응답 503 검증
- `stdout` 스파이로 로그 출력 확인
- `afterEach`에서 환경변수 정리 및 `app.close()`

---

## Phase 7: 빌드 및 최종 검증

```bash
cd nestjs/

# 로컬 검증
pnpm install
pnpm run build
pnpm run test
pnpm run test:e2e

# Docker 검증
docker build -t production-readiness .
docker run -d -p 3000:3000 -e NODE_ENV=production production-readiness
curl http://localhost:3000/health
curl http://localhost:3000/ready
docker logs <container_id>  # JSON 구조화 로그 확인
docker stop <container_id>
```

---

## 도구 및 커맨드 요약

| 도구/커맨드 | 용도 |
|-------------|------|
| `pnpm run build` | nest build (TypeScript 컴파일) |
| `pnpm run start` | 앱 실행 |
| `pnpm run test` | 단위 테스트 (Vitest) |
| `pnpm run test:e2e` | E2E 테스트 (Vitest) |
| `docker build` | Docker 이미지 빌드 |
| `docker run` | 컨테이너 실행 |
| `docker logs` | 컨테이너 로그 확인 (JSON 형태) |
| `curl` | health/ready 엔드포인트 수동 검증 |
| `process.stdout.write` | 구조화된 로그 출력 |

## 핵심 파일 생성 순서

```
runtime/runtime-config.ts → runtime/runtime.constants.ts → runtime/runtime-config.service.ts
→ health.controller.ts → runtime/structured-logging.interceptor.ts
→ app.module.ts (provider 등록) → main.ts
→ Dockerfile
→ tests/unit/ → tests/e2e/
```
