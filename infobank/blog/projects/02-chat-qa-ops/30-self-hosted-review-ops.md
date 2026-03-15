# self-hosted review ops

`v3-self-hosted-oss`의 핵심은 evaluator를 다시 쓰는 것이 아니다. 이미 있는 QA evaluation grammar를 로그인, dataset import, KB bundle, async job, selected-job review UI로 옮기는 것이다. 즉 `v3`는 알고리즘 확장보다 운영 surface 확장에 가깝다.

## auth가 붙으면서 QA Ops는 공개 데모가 아니라 운영 콘솔이 된다

`core/auth.py`는 password hash와 signed session cookie를 만든다.

```python
def create_session_cookie(*, secret: str, user_id: str, email: str, issued_at: int | None = None) -> str:
    issued = issued_at or int(time.time())
    payload = f"{user_id}:{email}:{issued}"
    signature = hmac.new(secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()
    return _urlsafe_encode(f"{payload}:{signature}".encode())
```

이 선택이 중요한 이유는 review console이 이제 "누가 들어와서 dataset을 올리고 job을 실행했는가"를 분리해야 하기 때문이다. README가 기본 admin email/password를 주는 것도 같은 맥락이다. `v3`는 공개 demo가 아니라 single-team self-hosted snapshot을 표방한다.

## job service가 evaluation을 기다릴 수 있는 작업으로 바꾼다

`services/jobs.py`는 pending job을 고르고, `EvaluationRun`, `KnowledgeBaseBundle`, `Turn` 목록을 읽어 worker loop로 처리한다.

```python
job.progress_total = len(turn_ids)
job.progress_completed = 0
job.status = "running"
...
job.progress_completed = index
...
job.status = "completed"
```

이 구조의 전환점은 evaluation이 더 이상 "한 번 실행하는 커맨드"가 아니라는 데 있다. operator는 dataset/bundle/run label/version 조합으로 job을 만들고, progress를 기다리고, 완료 후 overview/failures/session review를 다시 본다. 즉 v2의 proof가 v3에서는 asynchronous 운영 작업 단위가 된다.

## 프런트는 selected job을 기준으로 review surface를 다시 나눈다

`App.tsx`는 login gate, session check, jobs refresh, selected job state를 맡고, `Jobs.tsx`는 dataset/bundle 선택과 version inputs를 받아 `/api/jobs`에 post한다.

```tsx
const result = await apiPost<{ job: JobSummary }>("/api/jobs", {
  dataset_id: datasetId,
  kb_bundle_id: bundleId,
  run_label: runLabel.trim() || undefined,
  prompt_version: promptVersion,
  kb_version: kbVersion,
  evaluator_version: evaluatorVersion,
  retrieval_version: retrievalVersion,
});
```

좋은 점은 selected job이 app 전체의 기준이 된다는 것이다. sidebar에도 선택된 job이 보이고, `Overview`, `Failures`, `Session Review`는 모두 selected job 중심으로 좁혀 읽힌다. 이건 "모든 결과를 한꺼번에 본다"보다 훨씬 운영자다운 surface다.

또 `Jobs.tsx`는 pending/running job이 있으면 2.5초 interval로 `onRefreshJobs()`를 재호출한다. 즉 polling이 명시적이고, async job의 기다림이 제품 surface에 그대로 들어와 있다.

## 이번 재실행 결과가 보여 준 현재 상태

2026-03-14에 `v3` Python gate를 다시 돌린 결과는 다음과 같았다.

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python
PATH="$HOME/.local/bin:$PATH" UV_PYTHON=python3.12 make gate-all
```

결과:

- lint 통과
- mypy: `51 source files`
- MP1 `2 passed`
- MP2 `4 passed`
- MP3 `2 passed`
- MP4 `1 passed`
- MP5 `1 passed`
- frontend `6 passed`

프런트 테스트에서는 두 가지 비차단 경고도 보였다.

- `pnpm approve-builds` 관련 ignored build scripts 경고
- React Router future flag warnings

둘 다 현재 gate를 깨지는 않지만, self-hosted snapshot의 tooling surface가 완전히 정리된 상태는 아니라는 신호다.

## 이 단계의 결론

`v3`를 high-quality 확장으로 보이게 만드는 건 더 좋은 judge가 아니다. 이미 있던 평가 체계를 설치 가능한 운영 흐름으로 옮긴 점이다. 로그인, dataset upload, KB bundle, async job, selected-job review UI가 붙으면서 `Chat QA Ops`는 `Rule -> Evidence -> Judge -> Proof`에서 멈추지 않고, `Proof -> Review Ops`까지 이어지는 프로젝트가 된다.
