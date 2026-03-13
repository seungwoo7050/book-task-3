# self-hosted operator surface

앞 글까지 오면 `v2`가 왜 공식 제출 버전인지 이해할 수 있다. 추천 결과가 compare, compatibility, release gate, artifact export까지 이어지기 때문이다. 이번 글은 그다음 질문에 답한다. 이미 만든 proof pipeline을, 실제 팀이 설치해서 운영할 수 있는 표면으로 바꾸면 어떤 모습이 될까?

`v3-oss-hardening`의 핵심은 새 ranking 기능이 아니다. 이미 있는 `eval -> compare -> compatibility -> release-gate -> artifact-export` 체인을 로그인과 job queue 뒤로 옮기고, 역할에 따라 다르게 보이는 운영 화면으로 감싼 것이 핵심이다.

백엔드에서 그 전환점이 가장 잘 드러나는 파일은 `capstone/v3-oss-hardening/node/src/services/job-service.ts`다. 여기서는 이전까지 사람이 순서대로 실행하던 검증 단계를, 이름이 있는 작업 큐로 선언한다.

아래 배열이 중요한 이유는, `v2`에서 손으로 실행하던 proof가 `v3`에서 운영자가 다루는 "작업 목록"으로 바뀌는 순간을 보여 주기 때문이다.

```ts
const jobQueues = [
  "eval",
  "compare",
  "compatibility",
  "release-gate",
  "artifact-export"
] satisfies JobName[];
```

이후 `performJob`은 각 큐가 어떤 데이터를 읽고 어떤 결과를 남기는지 분명하게 정리한다. compare job은 uplift를 남기고, release-gate job은 pass/fail과 uplift를 남기고, artifact-export job은 새 artifact id를 남긴다. 즉 이전까지는 명령어 흐름이었던 것이, 이제는 운영자가 기다릴 수 있는 상태 변화로 바뀐다.

프런트엔드 쪽 대응물은 `react/components/mcp-dashboard.tsx`다. 여기서는 owner/operator/viewer 역할을 나누고, job 등록 뒤 polling으로 완료 여부를 확인한다.

이 코드가 중요한 이유는 사용 방식 자체를 바꾸기 때문이다. 사용자는 더 이상 `pnpm release:gate ...` 같은 명령을 외우지 않아도 된다. 로그인해서 job을 등록하고, 완료 요약과 audit log를 같은 화면에서 확인할 수 있다.

```ts
const canOperate = session?.user.role === "owner" || session?.user.role === "operator";

async function waitForJob(jobId: string) {
  for (let attempt = 0; attempt < 20; attempt += 1) {
    const response = await apiFetch<{ item: JobRun }>(`/api/jobs/${jobId}`);
```

좋은 점은 역할 구분도 분명하다는 것이다. viewer는 읽기 전용으로 남고, owner만 audit log와 settings를 다룬다. 그래서 recommendation project가 제품화될 때 필요한 최소한의 운영 질서가 이 단계에서 보이기 시작한다.

실제 회귀 신호도 확보돼 있다.

```bash
cd capstone/v3-oss-hardening
pnpm test
```

```text
node: 8 passed | 2 skipped
react: 2 passed
```

이 출력이 증명하는 것은, self-hosted surface가 단순한 화면 mock이 아니라는 점이다. node와 react दोनों에서 실제 동작 경로를 검증하고 있고, owner 로그인과 job flow도 테스트에 들어가 있다. 다만 `2 skipped`가 남아 있다는 점도 같이 읽어야 한다. 이 버전은 방향을 충분히 보여 주지만, 모든 route integration이 완전히 끝난 production-hardening 상태라고 과장하진 않는다.

그래도 이 단계가 중요한 이유는 분명하다. `v2`에서 이미 완성한 deterministic proof를 버리지 않고, 더 안전한 운영 표면으로 다시 배치했기 때문이다. 그래서 이 프로젝트의 전체 흐름은 `catalog -> ranking -> release proof -> operator jobs` 순서로 읽을 때 가장 설득력이 크다.
