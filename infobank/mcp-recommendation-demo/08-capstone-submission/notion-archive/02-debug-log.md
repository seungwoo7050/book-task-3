# 02 — 디버그 기록: 4개 버전에서 만난 문제들

## v0 문제: Zod 스키마 순환 참조

### 증상

`catalogEntrySchema`가 `mcpManifestSchema`를 참조하고, manifest가 다시 catalog의 일부 필드를 참조하는 구조에서 TypeScript 타입 추론이 실패한다.

### 원인

Zod의 `z.infer<>`는 스키마가 완전히 정의된 후에만 타입을 추론할 수 있다.  
서로를 참조하면 `any`로 추론되거나 컴파일 에러가 발생한다.

### 해결

스키마를 계층적으로 분리했다:
1. `mcpManifestSchema` → 독립적으로 정의
2. `catalogEntrySchema` → manifest의 필드를 embed하되 schema 자체를 참조하지 않음

`catalogEntrySchema`가 manifest 전체를 포함하는 것이 아니라, manifest의 핵심 필드를 flat하게 들고 있는 구조로 변경했다.

## v1 문제: Usage Signal이 0인 도구의 reranking

### 증상

새로 추가된 MCP 도구(usage log가 없는)가 reranking 후 항상 맨 뒤로 밀린다.  
usage signal = 0이면 baseline 점수에 가산이 없기 때문이다.

### 원인

reranker가 `usageBoost = acceptCount * weight`로 계산하는데,  
새 도구는 acceptCount = 0이므로 boost = 0.  
기존 도구는 accept 몇 개만 있어도 점수가 올라가서 새 도구가 하위로 밀린다.

### 해결

cold-start 보정을 추가했다:
- usage event가 N개 미만인 도구에게 "중립 boost" (기존 도구의 평균 boost)를 부여
- 이렇게 하면 usage가 없어도 "다른 도구와 동일한 출발선"에서 시작한다

## v1 문제: Compare 결과의 nDCG@3이 항상 동일

### 증상

baseline과 candidate의 nDCG@3이 동일한 값으로 나온다.  
uplift = 0.

### 원인

`/api/recommendations`와 `/api/recommendations/candidate`가 같은 selector를 호출하고 있었다.  
reranker가 candidate 라우트에만 적용되어야 하는데, 라우팅 실수로 둘 다 baseline이 호출됨.

### 해결

candidate 라우트에서 `rerankCatalog()`를 명시적으로 호출하도록 분기를 수정했다.  
이후 compare에서 candidate nDCG@3 > baseline nDCG@3으로 uplift가 양수가 되는 것을 확인했다.

## v2 문제: Compatibility Gate의 semver 파싱 실패

### 증상

버전 문자열이 `"^1.2.0"` (caret range) 형태인 경우 semver 파싱에서 `null`이 반환된다.

### 원인

`semver.parse()`는 exact version만 받는다.  
range 문자열은 `semver.satisfies()`와 함께 써야 한다.

### 해결

`testedClientVersions` 배열의 각 항목에 대해:
- 먼저 `semver.valid()`로 exact version인지 확인
- exact면 `semver.satisfies(target, version)`
- range면 `semver.satisfies(target, rangeString)` 직접 사용

## v2 문제: Release Gate에서 check 누락

### 증상

Release gate가 `PASS`를 반환했는데, eval recall이 threshold 이하인 경우에도 통과했다.

### 원인

check 목록에서 `evalRecallAboveThreshold`가 빠져 있었다.  
gate 로직이 "등록된 check만 검사"하는 구조여서, check를 등록하지 않으면 통과로 간주된다.

### 해결

gate 로직을 "check 목록이 비면 FAIL"로 변경했다:

```typescript
if (checks.length === 0) return { verdict: "FAIL", reason: "no checks defined" };
```

그리고 필수 check 5개를 `requiredChecks` 상수로 정의해서, 실행 전에 모두 존재하는지 확인한다.

## v3 문제: 세션 쿠키가 Docker 환경에서 유실

### 증상

로컬에서는 로그인이 유지되는데, Docker Compose로 올리면 페이지 새로고침 시 로그아웃된다.

### 원인

`secure: true`로 설정된 쿠키가 HTTP 환경(Docker 내부)에서 브라우저에 의해 거부된다.

### 해결

로컬/Compose 환경에서는 `secure: false`로 설정:

```typescript
const sessionCookieOptions = {
  path: "/",
  httpOnly: true,
  sameSite: "lax" as const,
  secure: false  // process.env.NODE_ENV === "production"이면 true
};
```

## v3 문제: pg-boss worker가 job을 두 번 실행

### 증상

eval job이 한 번 enqueue되었는데 audit log에 두 번 기록된다.

### 원인

worker 프로세스가 `newJob` 이벤트를 두 번 구독하고 있었다.  
`worker.ts`에서 `subscribe`를 두 번 호출하는 코드가 있었다 (개발 중 hot-reload에서 중복 등록).

### 해결

worker 시작 시 기존 구독을 정리하는 로직 추가, 그리고 각 job name에 대해 `subscribe`를 한 번만 호출하도록 보장했다.

## v3 문제: Docker 빌드에서 pnpm workspace 캐시 문제

### 증상

`docker compose build`에서 shared 패키지의 변경사항이 api 이미지에 반영되지 않는다.

### 원인

Dockerfile에서 `COPY pnpm-lock.yaml .` 단계가 캐시되면, 이후 `COPY shared/ shared/` 단계도 캐시된 레이어를 사용한다. shared의 소스 파일이 바뀌어도 lock 파일이 같으면 캐시가 깨지지 않는다.

### 해결

Dockerfile에서 소스 COPY를 lock 파일과 분리하고 `--no-cache` 옵션을 문서화했다:

```bash
docker compose build --no-cache
# 또는 specific service만
docker compose build --no-cache api
```
