# self-hosted operator surface

`v2`가 proof chain을 완성했다면, `v3-oss-hardening`은 그 proof를 운영자가 다룰 수 있는 표면으로 옮긴 단계다. 여기서 중요한 점은 새 recommendation algorithm이 추가된 것이 아니라는 것이다. 오히려 `eval -> compare -> compatibility -> release-gate -> artifact-export`라는 기존 체인을 queue와 RBAC 뒤로 감쌌다는 점이 핵심이다.

## 백엔드 전환점은 proof를 job queue로 이름 붙이는 순간이다

`job-service.ts`는 운영자가 다룰 작업 큐를 이렇게 선언한다.

```ts
const jobQueues = [
  "eval",
  "compare",
  "compatibility",
  "release-gate",
  "artifact-export"
] satisfies JobName[];
```

이 배열이 중요한 이유는 `v2`에서 사람이 CLI로 순서대로 실행하던 proof가, `v3`에서는 백엔드가 관리하는 named job이 된다는 사실을 보여 주기 때문이다. `performJob()` 안을 보면 각 작업은 결국 `v2`에서 보던 service들을 다시 호출한다.

- `eval`: `evaluateOfflineCases()`
- `compare`: `runCompare()`
- `compatibility`: `runCompatibilityGate()`
- `release-gate`: `runReleaseGate()`
- `artifact-export`: `buildSubmissionArtifact()`

즉 `v3`는 기존 proof를 버리는 게 아니라 orchestration만 바꾼다.

## 프런트 전환점은 owner/operator/viewer가 서로 다른 surface를 갖는다는 점이다

`mcp-dashboard.tsx`는 로그인 세션과 role을 읽고 다음처럼 권한을 나눈다.

```ts
const canOperate = session?.user.role === "owner" || session?.user.role === "operator";
const isOwner = session?.user.role === "owner";
```

이후 대시보드는 recommendation preview, job history, latest eval/compare/compatibility/gate/artifact, audit log, settings를 하나의 운영 콘솔에 묶는다. 중요한 건 사용자가 더 이상 `pnpm release:gate ...`를 외우지 않아도 된다는 점이다. 로그인 후 job을 enqueue하고, polling으로 결과를 기다리며, latest artifact까지 같은 화면에서 확인할 수 있다.

소스 안에 helper가 꽤 많이 들어 있는 것도 이 흐름을 보여 준다.

- `buildSampleCatalogEntry()`
- `buildSampleExperiment()`
- `buildSampleReleaseCandidate()`
- `apiFetch()`와 `sleep()`

즉 이 대시보드는 pretty mock이 아니라, self-hosted 운영 흐름을 데모하기 위한 실제 task surface다.

## 이번 재실행에서 확인된 현재 경계

2026-03-14에 `capstone/v3-oss-hardening`에서 `pnpm test`를 다시 돌린 결과는 아래와 같았다.

- node: `8 passed | 2 skipped`
- react: `2 passed`

react 테스트 중 하나는 실제로 `logs in as owner and runs export plus release-gate job flow`를 검증한다. 반면 node 쪽 route integration 2개는 아직 skipped다. 즉 `v3`는 operator flow를 설명할 만큼은 충분히 살아 있지만, 모든 route path를 production-hardening 수준으로 닫아 둔 상태는 아니다.

이 점을 문서에서 숨길 필요는 없다. 오히려 `v3`의 역할을 정확히 보여 준다. 현재 단계의 목적은 proof chain을 운영 표면으로 옮기는 것이지, 완전한 self-hosted SaaS를 보증하는 것이 아니기 때문이다.

## 왜 이 확장이 설득력 있는가

좋은 확장은 이전 단계를 부정하지 않는다. `v3`가 설득력 있는 이유는 `v2`에서 이미 deterministic하게 만들었던 proof를 그대로 재사용한다는 점이다. recommendation quality, compatibility, release gate, artifact export라는 핵심 판단은 여전히 같은 서비스가 담당한다. 바뀐 것은 누가, 어떤 surface에서, 어떤 권한으로 그 판단을 실행하고 기다릴 수 있느냐다.

그래서 이 프로젝트의 전체 흐름은 `catalog contract -> ranking trace -> release proof -> operator job surface` 순서로 읽을 때 가장 자연스럽다. `v3`는 새 알고리즘의 승리가 아니라, 이미 검증된 proof 체인을 운영자가 다룰 수 있게 만드는 제품화 단계다.
