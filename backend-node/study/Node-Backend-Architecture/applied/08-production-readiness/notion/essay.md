# 코드 완성은 시작일 뿐 — 운영 가능한 서비스로의 전환

## 프롤로그: "동작하는 코드"와 "배포 가능한 서비스"의 거리

프로젝트 07까지 만든 것은 기능적으로 완전한 애플리케이션이다. CRUD, 인증, 영속, 이벤트 — 개발자의 노트북에서는 잘 돌아간다. 하지만 이것을 서버에 올려서 실제 사용자에게 제공하려면, 코드 바깥에서 해결해야 할 문제들이 산적해 있다.

서버가 시작했는데 어떤 포트를 쓰는지 환경변수가 없다면? 로드밸런서가 이 인스턴스가 트래픽을 받을 준비가 되었는지 어떻게 판단하는가? 에러가 발생했을 때 로그가 `console.log`로 찍히면 로그 수집 시스템이 파싱할 수 있는가? 컨테이너로 패키징하지 않으면 배포 파이프라인에 어떻게 올리는가?

이 프로젝트는 이 모든 질문에 답한다. 그리고 NestJS 단일 레인으로 진행한다. 운영 관점의 문제는 프레임워크 비교가 아니라 아키텍처 패턴의 이해가 핵심이기 때문이다.

---

## 1. Config — Fail-Fast 원칙

### 환경변수가 아니라 "검증된 설정 객체"

`loadRuntimeConfig` 함수는 `process.env`를 받아서 `RuntimeConfig` 타입의 객체를 반환한다. 단순히 값을 읽는 것이 아니다. 각 값을 파싱하고, 유효하지 않으면 즉시 에러를 던진다.

```typescript
function parsePort(value: string | undefined): number {
  const rawPort = value ?? "3000";
  const port = Number(rawPort);
  if (!Number.isInteger(port) || port <= 0) {
    throw new Error(`PORT must be a positive integer. Received: ${rawPort}`);
  }
  return port;
}
```

`PORT`가 "abc"이면 앱이 시작되지 않는다. `READY`가 "maybe"이면 시작되지 않는다. `LOG_LEVEL`이 "verbose"이면 시작되지 않는다.

이것이 **fail-fast** 원칙이다. 잘못된 설정으로 앱이 시작되어 예측 불가능하게 동작하는 것보다, 시작 자체를 거부하는 것이 안전하다. 프로덕션에서 2시간 후에 NaN 때문에 장애가 나는 것과, 배포 직후 "PORT must be a positive integer"라는 메시지와 함께 컨테이너가 종료되는 것 — 후자가 압도적으로 낫다.

### Symbol 기반 주입 토큰

```typescript
export const RUNTIME_CONFIG = Symbol("RUNTIME_CONFIG");
```

`RuntimeConfig` 객체를 NestJS DI에 등록할 때 문자열 대신 `Symbol`을 토큰으로 사용한다. 이유는 명확하다 — 문자열은 충돌 가능성이 있지만 `Symbol`은 고유하기 때문이다. `AppModule`에서 `useFactory`로 `loadRuntimeConfig(process.env)`를 호출하고, 결과를 `RUNTIME_CONFIG` 토큰에 바인딩한다.

`RuntimeConfigService`는 이 토큰을 `@Inject(RUNTIME_CONFIG)`로 받아서 `snapshot` 게터를 통해 나머지 코드에 노출한다. Config 접근이 한 곳(서비스)으로 모이므로 테스트에서 쉽게 교체할 수 있다.

---

## 2. Health Check와 Readiness — 다른 질문, 다른 응답

### `/health` — "살아 있니?"

```typescript
@Get("health")
getHealth() {
  return { status: "ok", appName: ..., environment: ..., timestamp: ... };
}
```

이 엔드포인트는 항상 200을 반환한다. 앱 프로세스가 살아 있고 HTTP 요청을 처리할 수 있다는 의미다. Kubernetes의 `livenessProbe`가 이 엔드포인트를 호출한다. 연속으로 실패하면 컨테이너를 재시작한다.

### `/ready` — "트래픽을 받아도 되니?"

```typescript
@Get("ready")
getReady() {
  if (!config.ready) {
    throw new ServiceUnavailableException({
      status: "not-ready",
      reason: "Set READY=true after dependencies are available.",
    });
  }
  return { status: "ready", ... };
}
```

이 엔드포인트는 조건부로 503을 반환할 수 있다. 앱은 살아 있지만 아직 트래픽을 받을 준비가 안 되었다는 의미다. 데이터베이스 커넥션이 아직 확립되지 않았거나, 캐시 워밍업이 진행 중이거나, 필요한 외부 서비스가 아직 응답하지 않을 때 사용한다.

Kubernetes의 `readinessProbe`가 이 엔드포인트를 호출한다. 503을 반환하면 해당 인스턴스를 서비스 엔드포인트에서 제외한다 — 트래픽이 가지 않는다. 프로세스를 죽이지는 않는다.

`health`와 `ready`를 분리하는 이유: 앱이 살아 있지만 아직 준비되지 않은 상태가 존재하기 때문이다. 이 구분은 그레이스풀 배포의 기반이다.

---

## 3. Structured Logging — 기계가 읽는 로그

### console.log의 한계

`console.log("User created:", userId)`는 사람에게는 읽기 좋다. 하지만 로그 수집 시스템(ELK, Datadog, CloudWatch)은 이 문자열을 파싱할 수 없다. "누가", "언제", "어떤 엔드포인트에서", "얼마나 걸렸는지"를 자동으로 추출할 수 없다.

### JSON 로그

`StructuredLoggingInterceptor`는 모든 HTTP 요청을 가로채서 JSON 형태의 로그를 `process.stdout`에 출력한다.

```json
{
  "level": "info",
  "appName": "production-readiness-app",
  "environment": "production",
  "requestId": "abc-123",
  "method": "GET",
  "path": "/health",
  "statusCode": 200,
  "durationMs": 3,
  "outcome": "ok"
}
```

각 필드가 구조화되어 있으므로 로그 수집 시스템이 인덱싱하고 검색할 수 있다. "statusCode가 500인 요청"이나 "durationMs가 1000 이상인 요청"을 쿼리로 찾을 수 있다.

### Request ID 전파

인터셉터는 클라이언트가 보낸 `x-request-id` 헤더를 읽고, 응답에도 그대로 돌려보낸다. 요청 ID가 없으면 기본값을 채운다. 이 ID가 로그에 포함되므로, 하나의 요청이 여러 서비스를 거치더라도 추적할 수 있다. 이것이 분산 추적(distributed tracing)의 출발점이다.

### stdout vs 파일

로그를 `process.stdout.write()`로 직접 쓴다. `console.log()`가 아니다. 이유는:
1. `console.log`는 줄바꿈, 포맷팅 등 부가 처리를 한다
2. 컨테이너 환경에서는 stdout이 곧 로그 수집 파이프라인의 입력이다
3. 파일에 쓰면 컨테이너가 로그를 어디에 저장할지, 로테이션은 어떻게 할지 고민해야 한다
4. stdout으로 보내면 Docker/Kubernetes가 로그를 수집하고 관리한다

---

## 4. Dockerfile — 멀티스테이지 빌드

```dockerfile
FROM node:22-alpine AS build
WORKDIR /app
COPY package.json pnpm-lock.yaml* ./
RUN corepack enable && pnpm install
COPY . .
RUN pnpm run build

FROM node:22-alpine
WORKDIR /app
COPY --from=build /app/package.json ./
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
ENV NODE_ENV=production
CMD ["node", "dist/main.js"]
```

두 단계를 거치는 이유:
1. **빌드 스테이지**: TypeScript 컴파일, devDependencies 포함. 이미지 크기가 크다.
2. **런타임 스테이지**: 컴파일된 JS와 런타임 의존성만 복사. 이미지 크기가 작다.

`node:22-alpine`을 쓰는 이유: Alpine Linux는 glibc 대신 musl을 사용하여 이미지 크기가 극적으로 줄어든다. 일반 node 이미지(~1GB)에 비해 Alpine 버전은 ~150MB 수준.

---

## 5. APP_INTERCEPTOR — 전역 등록의 DI 방식

`AppModule`에서 인터셉터를 전역으로 등록하는 방식이 특별하다:

```typescript
{
  provide: APP_INTERCEPTOR,
  inject: [RuntimeConfigService],
  useFactory: (runtimeConfig: RuntimeConfigService) => {
    return new StructuredLoggingInterceptor(runtimeConfig);
  },
}
```

`main.ts`에서 `app.useGlobalInterceptors()`를 쓰는 것 대비 이 방식의 장점: DI 컨테이너를 통해 생성되므로 의존성(RuntimeConfigService)을 자동으로 주입받을 수 있다. `useGlobalInterceptors`로 등록하면 수동으로 인스턴스를 만들어야 한다.

---

## 6. 테스트 전략

### Config 단위 테스트

`loadRuntimeConfig`를 빈 객체(`{}`)로 호출하면 기본값만으로 유효한 설정이 만들어진다. 개발 환경에서 환경변수 없이도 앱이 시작되는 것을 보장한다.

잘못된 PORT를 넘기면 예외가 발생하는지를 테스트로 고정한다. fail-fast의 동작을 회귀 방지하는 것이다.

### E2E 테스트의 환경변수 조작

E2E 테스트에서는 `process.env`를 직접 패치한다:

```typescript
process.env = { ...process.env, ...envPatch };
```

`afterEach`에서 설정한 환경변수를 `delete`로 정리한다. 테스트 간 환경변수 오염을 방지하기 위해서다.

`READY=false`일 때 `/ready`가 503을 반환하는지, `READY=true`일 때 `/health`가 200을 반환하는지를 검증한다.

stdout 스파이로 로그 출력 여부도 확인한다:
```typescript
const stdoutSpy = vi.spyOn(process.stdout, "write").mockImplementation(() => true);
```

---

## 에필로그: 배포의 시작

이 프로젝트는 "코드를 어떻게 운영 환경에 올릴 것인가"에 대한 첫 번째 답이다. Config, health check, structured logging, Docker — 이 네 가지는 모든 프로덕션 서비스의 최소 조건이다.

다음 프로젝트(09-platform-capstone)에서는 지금까지의 모든 것을 하나로 합친다. REST, 파이프라인, 인증, 영속, 이벤트, 그리고 이 운영 인프라까지. 그리고 프로젝트 10에서는 SQLite 대신 Postgres가, 단일 컨테이너 대신 Docker Compose가 등장한다.
