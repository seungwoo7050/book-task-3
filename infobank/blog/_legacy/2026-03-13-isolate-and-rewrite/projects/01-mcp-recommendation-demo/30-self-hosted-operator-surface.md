# Self-Hosted Operator Surface

이 글은 시리즈의 마지막 구간이다. `v2`가 제출용 proof를 완성했다면, `v3`는 그 흐름을 로그인된 운영자가 직접 설치해서 돌릴 수 있는 self-hosted surface로 바꾼다. 핵심은 새 추천 알고리즘이 아니라 auth, RBAC, queue worker, audit log가 recommendation workflow의 일부가 되는 순간이다.

구현 순서 요약:

- API 앞단에 cookie session과 role check를 넣어 owner/operator/viewer를 구분한다.
- eval/compare/compatibility/release gate/artifact export를 모두 background job으로 분리한다.
- worker와 metrics endpoint, audit trail, dashboard를 통해 operator가 상태를 읽게 만든다.

## Day 4

### Session 1

- 당시 목표: 누구나 열 수 있는 demo를 로그인된 operator console로 바꾼다.
- 변경 단위: `node/src/services/auth-service.ts`, `node/src/app.ts`
- 처음 가설: self-hosted라도 단일 관리자 환경이면 API key만 있으면 충분할 줄 알았다.
- 실제 진행: session token을 해시해서 저장하고, `resolveAuth()`가 cookie, session refresh, inactive user 정리, role check를 모두 맡게 했다. 이후 `/api/users`, `/api/auth/*` 같은 라우트가 이 경계를 공유한다.

핵심 코드:

```ts
const token = request.cookies[SESSION_COOKIE_NAME];
if (!token) {
  reply.code(401);
  return null;
}

const record = await getSessionRecordByTokenHash(hashSessionToken(token));
if (!record) {
  reply.clearCookie(SESSION_COOKIE_NAME, sessionCookieOptions);
  reply.code(401);
  return null;
}

if (roles && !roles.includes(user.role)) {
  reply.code(403);
  return null;
}
```

왜 이 코드가 중요했는가:

`v2`까지는 기능이 있느냐가 중심이었지만, `v3`부터는 누가 그 기능을 실행할 수 있느냐가 더 중요해진다. `401`과 `403`을 나누는 이 짧은 분기가 self-hosted product의 첫 경계였다.

CLI:

```bash
$ pnpm migrate
[✓] Changes applied

$ pnpm bootstrap:owner
{
  "ownerEmail": "owner@study1.local",
  "ownerId": "d52cd900-2a05-47e7-83cb-07beba6ab4f1",
  "role": "owner"
}
```

검증 신호:

- bootstrap 명령이 owner 계정을 명시적으로 만들기 때문에, 이제 시스템은 "seeded demo data"가 아니라 "운영자 계정이 있는 인스턴스"가 된다.

새로 배운 것:

self-hosted 확장은 기능의 개수가 아니라 identity boundary를 먼저 세우는 순서에서 갈린다.

### Session 2

- 당시 목표: eval, compare, release gate 같은 무거운 작업을 요청 한 번에 끝내지 않고 queue job으로 분리한다.
- 변경 단위: `node/src/services/job-service.ts`, `node/src/worker.ts`, `node/src/app.ts`
- 처음 가설: operator console에서도 버튼을 누르면 바로 eval/report가 돌아오는 sync path면 충분할 줄 알았다.
- 실제 진행: `enqueueJob()`이 job row와 audit event를 남기고, worker는 queue별로 `performJob()`을 호출해 status를 `pending -> running -> completed/failed`로 바꾼다. 요약 문장도 job output에서 바로 만들어 dashboard가 읽는다.

핵심 코드:

```ts
export async function enqueueJob(name: JobName, payload: QueuePayload, actor: StoredUser) {
  const boss = await getBoss();
  const jobId = await boss.send(name, payload);
  const run: JobRun = {
    id: jobId,
    name,
    status: "pending",
    createdByUserId: actor.id,
    createdByEmail: actor.email,
    payload: payload as Record<string, unknown>,
    output: null
  };
  await createJobRun(run);
}
```

worker는 같은 queue 이름을 그대로 `performJob()`에 연결한다.

```ts
for (const queueName of jobQueues) {
  await boss.work(queueName, async (jobs) => {
    for (const job of Array.isArray(jobs) ? jobs : [jobs]) {
      await markJobRunning(job.id);
      try {
        const result = await performJob(queueName, (job.data ?? {}) as QueuePayload);
        await markJobCompleted(job.id, queueName, result.output);
      } catch (error) {
        await markJobFailed(job.id, queueName, normalized);
        throw normalized;
      }
    }
  });
}
```

왜 이 코드가 중요했는가:

이제 API는 "바로 결과를 주는 곳"이 아니라 "job lifecycle을 시작하고 상태를 보여 주는 곳"으로 바뀐다. recommendation project가 운영 소프트웨어로 넘어가는 순간이 여기다.

CLI:

```bash
$ pnpm test
node test:  Test Files  5 passed | 1 skipped (6)
node test:       Tests  8 passed | 2 skipped (10)
react test: Test Files  1 passed (1)
react test:      Tests  2 passed (2)
```

검증 신호:

- node suite는 DB integration을 opt-in으로 남겨 둔 채 core gate logic을 유지하고,
- react suite는 owner login 이후 export/release-gate job flow까지 component test로 확인한다.

새로 배운 것:

background job을 도입하면 API 설계도 같이 바뀐다. release gate를 누가, 어떤 권한으로, 어떤 artifact와 함께 다시 실행했는지를 남겨야 operator console이 된다.

### Session 3

- 당시 목표: self-hosted 설치 경험을 코드 구조와 같은 수준으로 명시한다.
- 변경 단위: `docker-compose.yml`, `Dockerfile.api`, `Dockerfile.worker`, `Dockerfile.web`, `docs/install.md`, `docs/operations.md`
- 실제 진행: `postgres + api + worker + web`를 Compose 한 번에 올리도록 만들고, metrics와 audit log를 operator surface 일부로 다뤘다.
- 검증 신호: `README.md`는 local path와 Compose path를 분리하고, `pnpm test`는 기본 회귀를, `worker`와 metrics endpoint는 long-running 운영 경로를 맡는다.
- 새로 배운 것: 설치 문서가 별도 포장재가 아니라, queue worker와 role model이 실제로 어떻게 배치되는지를 설명하는 운영 spec이 됐다.

다음:

이 프로젝트의 끝은 "추천을 더 잘한다"가 아니라, "추천 실험과 release 판단을 한 팀이 직접 설치해서 다시 돌릴 수 있다"는 지점이다. 그래서 `v3`는 새로운 모델보다 auth, job, audit, Compose를 더 많이 건드린다.
