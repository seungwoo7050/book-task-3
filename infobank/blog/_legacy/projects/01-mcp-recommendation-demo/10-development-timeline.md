# 01 MCP 추천 최적화 개발 타임라인

이 문서는 `notion/`을 보지 않고, 현재 버전별 README, 서비스 코드, 테스트, runbook, 실제 재검증 CLI만으로 `01-mcp-recommendation-demo`의 chronology를 다시 세운 기록이다. git history가 버전 재배치 위주로 압축돼 있어서, 시간 대신 `Day / Session`과 `v0 -> v1 -> v2 -> v3` 버전 사다리를 기준으로 읽는다.

## Day 1

### Session 1

- 목표: `v0-initial-demo`가 단순 키워드 검색 예제가 아니라 `seeded catalog + manifest contract + baseline recommendation`을 함께 고정하는 기준선인지 확인한다.
- 진행: `v0` README, `recommendation-service.ts`, `manifest-validation.test.ts`를 같이 읽어 추천과 계약 검증이 어디서 만나는지 먼저 따라갔다.
- 이슈: 처음엔 baseline selector가 query token match만으로 끝날 거라고 생각했다. 그런데 실제 코드는 `compatibility`, `locale`, `maturity`, `freshness`까지 baseline에서 이미 점수화한다.
- 판단: 이 프로젝트의 첫 버전은 "추천 결과를 뽑아 본다"보다 "추천 결과를 계약과 함께 설명 가능한 상태로 만든다"가 중심이다.

CLI:

```bash
$ cd projects/01-mcp-recommendation-demo/capstone/v0-initial-demo
$ pnpm install
$ cp .env.example .env
$ pnpm db:up
$ pnpm migrate
$ pnpm seed
$ pnpm dev
$ pnpm test
$ pnpm eval
```

이 시점의 첫 핵심 코드는 baseline recommendation이 호환성을 강한 패널티로 다룬다는 점이었다.

```ts
const versionMatch =
  semver.gte(request.environment.clientVersion, entry.compatibility.minimumClientVersion) &&
  semver.lte(request.environment.clientVersion, entry.compatibility.maximumClientVersion);

return transportMatch && platformMatch && versionMatch ? 15 : -20;
```

처음엔 `intent`나 `capability` 쪽 가중치만 보면 될 것 같았는데, 실제로는 baseline 단계부터 `transport / platform / clientVersion` 불일치에 음수 점수를 주고 있었다. 즉 이 프로젝트는 처음부터 "좋아 보이는 추천"보다 "지금 실행 가능한 추천"을 더 중요하게 본다.

manifest 검증도 별도 후처리가 아니라 출발선에 있다.

```ts
const parsed = mcpManifestSchema.safeParse({
  id: "bad",
  slug: "bad",
  name: "Bad",
  version: "1.0.0"
});

expect(parsed.success).toBe(false);
```

이 테스트를 보고 나서야 `seed`와 `recommendation` 사이에 manifest schema가 끼어 있다는 게 분명해졌다. baseline이 성립하려면 catalog entry가 아니라 manifest contract부터 통과해야 한다는 뜻이다.

### Session 2

- 목표: `v1-ranking-hardening`이 정말로 rerank와 compare를 도입했는지, 아니면 baseline 결과를 보기 좋게 포장한 것인지 확인한다.
- 진행: `rerank-service.ts`, `compare-service.ts`, `v1` README를 함께 읽고 usage event와 feedback record가 어떤 식으로 candidate score에 반영되는지 추적했다.
- 이슈: 처음엔 candidate 쪽이 baseline보다 점수만 조금 더 얹는다고 생각했다. 그런데 compare 로직은 candidate가 실제로 이기지 못하면 baseline top을 그대로 유지한다.
- 판단: `v1`의 핵심은 새 랭킹 함수를 붙인 것이 아니라, baseline과 candidate를 같은 eval case에서 비교 가능한 실험 단위로 바꾼 것이다.

CLI:

```bash
$ cd projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening
$ pnpm install
$ cp .env.example .env
$ pnpm db:up
$ pnpm migrate
$ pnpm seed
$ pnpm dev
$ pnpm test
$ pnpm eval
$ pnpm e2e
```

candidate 쪽이 실제 사용 신호를 어떻게 반영하는지는 이 조각이 가장 잘 드러냈다.

```ts
const uplift =
  ctr * 14 + acceptRate * 18 + feedbackAverage * 5 + explanationQuality * 4 + freshness * 2;
```

처음엔 rerank라고 해서 모델이나 복잡한 relevance 함수가 먼저 떠올랐지만, 실제 구현은 impression, click, accept, feedback, explanation locale, freshness를 합성해 점수를 올리는 식이었다. 운영형 추천으로 넘어갈 때 가장 먼저 필요한 게 "정교한 모델"이 아니라 "학습 가능한 신호 저장"이라는 판단이 코드에 남아 있다.

compare 쪽은 더 보수적이었다.

```ts
const candidateWins = candidateScore >= baselineScore;

candidateTop: candidateWins
  ? candidate.topCandidates[0]?.catalogId ?? null
  : baseline.topCandidates[0]?.catalogId ?? null,
```

이 짧은 분기 때문에 `v1`은 candidate를 무조건 새 정답으로 선언하지 않는다. 당시에는 compare artifact가 단순 리포트일 거라 생각했는데, 실제로는 baseline보다 나쁠 때 candidate top을 채택하지 않는 보호장치가 먼저 들어가 있었다.

### Session 3

- 목표: `v2-submission-polish`가 단순 문서 정리 버전이 아니라 `compatibility gate -> release gate -> artifact export`까지 포함한 제출 흐름인지 확인한다.
- 진행: `runbook.md`, `release-gate-service.ts`, `routes.integration.test.ts`, 실제 `pnpm db:up -> migrate -> seed -> test -> eval -> compatibility -> release:gate -> artifact:export` 경로를 차례로 실행했다.
- 이슈: 처음엔 `pnpm test`만으로도 route integration이 바로 통과할 줄 알았다. 실제로는 prepared DB가 없으면 `/api/catalog`가 `500`을 반환했고, `db:up -> migrate -> seed` 뒤에야 `9 passed`가 됐다.
- 판단: 이 버전의 실제 최소 단위는 라이브러리 테스트가 아니라 seeded PostgreSQL 위에서 돌아가는 release workflow 전체다.
- 검증:
- `pnpm seed` 출력: `Seeded 12 catalog entries, 12 eval cases, usage signals, feedback, experiments, and release candidates.`
- `pnpm test` 출력: node `6 files / 9 tests passed`, react `1 file / 1 test passed`
- `pnpm eval` 출력: `top3Recall 0.9583333333333334`, `explanationCompleteness 1`, `forbiddenHitRate 0`
- `pnpm compatibility rc-release-check-bot-1-5-0` 출력: `"passed": true`
- `pnpm release:gate rc-release-check-bot-1-5-0` 출력: `"passed": true`

CLI:

```bash
$ cd projects/01-mcp-recommendation-demo/capstone/v2-submission-polish
$ pnpm db:up
$ pnpm migrate
$ pnpm seed
$ pnpm test
$ pnpm eval
$ pnpm compatibility rc-release-check-bot-1-5-0
$ pnpm release:gate rc-release-check-bot-1-5-0
$ pnpm artifact:export rc-release-check-bot-1-5-0
```

release gate가 실제로 보는 범위는 점수만이 아니었다.

```ts
if (!requiredPathsExist(candidate.requiredDocs) || !requiredPathsExist(candidate.requiredArtifacts)) {
  reasons.push("제출용 docs 또는 artifact 파일이 누락되었습니다.");
}

if (!releaseNotesComplete(candidate.releaseNotesKo)) {
  reasons.push("release note에 '변경 요약', '검증', '리스크' 섹션이 모두 들어 있지 않습니다.");
}
```

처음엔 `offline eval`과 `compare uplift`만 넘으면 끝날 줄 알았는데, 실제 `v2`는 docs, artifact, release note section까지 체크했다. 이 버전이 submission polish인 이유가 UI 마감이 아니라 "증빙 누락이 없는가"를 gate로 강제한다는 데 있었다.

integration test도 같은 흐름을 강하게 전제한다.

```ts
const evalResponse = await app.inject({
  method: "POST",
  url: "/api/evals/run"
});

expect(evalBody.metrics.top3Recall).toBeGreaterThanOrEqual(0.9);
expect(evalBody.acceptance.top3RecallPass).toBe(true);
```

이 테스트를 보고 나서 `v2`를 단순 API 스모크라고 읽을 수 없게 됐다. 추천 API가 뜨는지만 보는 것이 아니라, eval acceptance와 release artifact 경로까지 한 번에 검증해야 이 버전의 의미가 살아난다.

### Session 4

- 목표: `v3-oss-hardening`이 `v2`에 로그인 화면만 얹은 확장인지, 아니면 운영 단위를 분리한 self-hosted 버전인지 확인한다.
- 진행: `v3` README와 `auth-service.ts`, `job-service.ts`, `audit-service.ts`, root `package.json` 스크립트를 읽어 auth, worker, queue, audit, Compose 경로를 함께 정리했다.
- 이슈: 처음엔 productization이 곧 "콘솔 로그인 추가"라고 생각했다. 그런데 실제 구현은 `owner bootstrap`, `pg-boss` worker, queue별 job summary, audit event까지 별도 운영 단위를 만든다.
- 판단: `v3`의 경계는 추천 알고리즘 추가가 아니라, 추천/평가/게이트를 사람이 로그인한 상태에서 비동기로 운영할 수 있게 만든 데 있다.

CLI:

```bash
$ cd projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening
$ pnpm install
$ cp .env.example .env
$ pnpm db:up
$ pnpm migrate
$ pnpm seed
$ pnpm bootstrap:owner
$ pnpm dev
$ pnpm test
$ pnpm test:integration
$ pnpm compare
$ docker compose up -d --build
```

auth가 단순 세션 문자열이 아니라 명시적 토큰/TTL 구조를 가진다는 점이 먼저 보였다.

```ts
const token = randomBytes(32).toString("hex");
const session: Session = {
  id: randomUUID(),
  userId,
  createdAt: new Date(now).toISOString(),
  lastSeenAt: new Date(now).toISOString(),
  expiresAt: new Date(now + SESSION_TTL_MS).toISOString()
};
```

`v2`에서는 없던 `sessionSecret`, token hash, `lastSeenAt`, `expiresAt`가 추가되면서, 추천 데모가 로그인된 운영 콘솔로 넘어갔다는 사실이 분명해진다.

job worker 쪽은 더 명확하다.

```ts
const jobQueues = [
  "eval",
  "compare",
  "compatibility",
  "release-gate",
  "artifact-export"
] satisfies JobName[];
```

그리고 enqueue 시점에 audit event도 함께 남긴다.

```ts
await createAuditEvent(
  buildAuditEvent({
    actor,
    action: "job.enqueue",
    targetType: "job",
    targetId: jobId,
```

처음엔 release workflow를 버튼 하나로 동기 실행하는 수준일 거라고 봤지만, 실제 `v3`는 queue 이름 자체를 운영 표면으로 끌어올리고, 누가 어떤 작업을 큐에 넣었는지 audit trail로 남긴다. 이 시점부터는 더 이상 "제출용 polish"가 아니라 "single-node self-hosted 운영 후보"라고 읽는 편이 정확하다.
