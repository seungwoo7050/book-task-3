# Self-Hosted Review Ops

앞 글까지는 QA Ops를 제출 가능한 regression proof로 만드는 과정이었다. 이 글은 그 흐름을 `v3`에서 어떻게 self-hosted review ops 제품으로 바꿨는지 따라간다. 핵심은 evaluator를 더 복잡하게 만드는 것이 아니라, dataset과 KB bundle을 어떤 권한의 운영자가 어떤 job으로 다시 돌릴지 경계를 세우는 일이다.

구현 순서 요약:

- sync `/api/evaluate/*` 경로는 유지하되, 운영용 재실행은 `/api/jobs`와 worker loop로 분리했다.
- job은 dataset, KB bundle, run label, prompt/kb/evaluator/retrieval version을 함께 기록한다.
- worker는 turn 단위 진행률을 업데이트하고 실패를 job status에 남긴다.

## Day 4

### Session 1

- 당시 목표: 제출용 evaluate demo를 운영자가 반복 실행할 수 있는 self-hosted review ops surface로 바꾼다.
- 변경 단위: `api/routes/evaluation.py`, `api/routes/jobs.py`, `services/jobs.py`
- 처음 가설: `/api/evaluate/batch` 같은 sync endpoint만 있어도 review console에는 충분할 것이라고 봤다.
- 실제 진행: sync batch endpoint는 유지하되, 운영자가 dataset과 KB bundle을 선택해 재실행하는 경로는 `/api/jobs`와 worker loop로 분리했다.

우선 `v3`도 sync batch entrypoint는 남겨 둔다.

```py
run = create_evaluation_run(
    session,
    kb_bundle_id=payload.kb_bundle_id,
    run_label=payload.run_label or payload.prompt_version,
    dataset_name=payload.dataset or "batch-evaluate",
    prompt_version=payload.prompt_version,
    kb_version=payload.kb_version,
    evaluator_version=payload.evaluator_version,
    retrieval_version=payload.retrieval_version,
)
```

왜 이 코드가 중요했는가:

`v2`의 제출형 evaluate 흐름을 완전히 버린 게 아니라, run metadata를 더 분명하게 남기는 기반으로 유지했기 때문이다. self-hosted 제품도 결국 evaluation run이라는 동일한 중심 객체 위에 선다.

하지만 운영 경계는 별도 job route에서 생긴다.

```py
batch = session.get(ConversationBatch, payload.dataset_id)
bundle = session.get(KnowledgeBaseBundle, payload.kb_bundle_id)
if batch is None:
    raise HTTPException(status_code=404, detail="dataset not found")
if bundle is None:
    raise HTTPException(status_code=404, detail="kb bundle not found")

run = create_evaluation_run(
    session,
    batch_id=batch.id,
    kb_bundle_id=bundle.id,
    run_label=payload.run_label or f"{batch.name}-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}",
    dataset_name=batch.name,
    baseline_label=payload.baseline_label,
    candidate_label=payload.candidate_label,
)
```

이 코드는 운영자가 무엇을 다시 돌렸는지를 dataset과 KB bundle id 수준으로 고정한다. 이제 compare나 dashboard는 단순히 "최근 평가"가 아니라 특정 입력 조합의 job 결과를 읽게 된다.

### Session 2

- 당시 목표: job 상태와 진행률을 HTTP 요청 밖으로 빼내 worker가 책임지게 만든다.
- 변경 단위: `services/jobs.py`
- 처음 가설: job id만 발급해 두고 실제 평가는 요청 스레드에서 끝까지 돌려도 괜찮을 것이라고 봤다.
- 실제 진행: pending job을 picker가 고르고, worker가 turn 목록을 순서대로 평가하면서 progress를 갱신하고, 실패를 `error_summary`에 기록하게 바꿨다.

핵심 코드는 job worker 자체다.

```py
turn_ids = list(
    session.scalars(
        select(Turn.id)
        .join(Conversation, Conversation.id == Turn.conversation_id)
        .where(Conversation.batch_id == job.batch_id)
        .order_by(Conversation.external_id.asc(), Turn.turn_index.asc())
    ).all()
)
job.progress_total = len(turn_ids)
job.progress_completed = 0
job.status = "running"
```

그리고 각 turn마다 진행률이 올라간다.

```py
for index, turn_id in enumerate(turn_ids, start=1):
    pipeline.evaluate_turn(
        turn_id,
        evaluator_version=run.evaluator_version,
        prompt_version=run.prompt_version,
        kb_version=run.kb_version,
        retrieval_version=run.retrieval_version,
        run=run,
        kb_bundle_id=bundle.id,
        allow_cache=False,
    )
    job.progress_completed = index
    job.updated_at = _utc_now()
    session.flush()
job.status = "completed"
```

왜 이 코드가 중요했는가:

여기서 QA Ops는 더 이상 "API 한 번 호출해서 결과를 기다리는 데모"가 아니다. 입력 dataset이 커져도, 실패가 나도, 운영자는 job 상태와 error summary를 읽으며 다시 시도할 수 있다.

CLI:

```bash
$ UV_PYTHON=python3.12 uv sync --extra dev
Resolved and installed dev dependencies

$ UV_PYTHON=python3.12 make gate-all
MP1: 2 passed
MP2: 4 passed
MP3: 2 passed
MP4: 1 passed
MP5: 1 passed
frontend vitest: 6 passed
Integrity gate passed for target=all
```

검증 신호:

- `v3` gate는 backend job flow와 frontend operator surface를 같은 snapshot으로 묶는다.
- `Jobs.test.tsx` 같은 UI 회귀가 붙어 있어서, job 상태가 API에만 존재하지 않고 콘솔에도 반영됨을 확인한다.

마지막으로 README는 이 경계를 설치 경험으로 바꾼다.

```bash
$ docker compose up --build
Web: http://localhost:5173
API: http://localhost:8000
```

이 quickstart가 중요한 이유는, `v3`가 제출용 스냅샷이 아니라 self-hosted OSS 후보 버전이라는 사실을 코드 밖 운영 경로로도 보여 주기 때문이다.

새로 배운 것:

self-hosted productization은 evaluator를 더 정교하게 만드는 문제가 아니었다. 어떤 입력 조합을 어떤 run label로 어떤 job이 수행했는지, 그리고 그 상태를 운영자가 어떻게 다시 읽을지를 API 경계와 worker 상태 모델에 새기는 일이었다.
