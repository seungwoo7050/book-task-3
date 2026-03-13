# self-hosted review ops

앞 글까지 오면 `v2`가 왜 설득력 있는 capstone snapshot인지 이해할 수 있다. 평가 파이프라인이 있고, regression compare가 있고, 그 결과를 proof artifact로 닫을 수 있기 때문이다. 이번 글은 그다음 질문에 답한다. 이 흐름을 실제 팀이 설치해서 운영할 수 있는 표면으로 옮기면 어떤 모습이 될까?

`v3-self-hosted-oss`의 핵심은 평가 로직을 새로 만드는 것이 아니다. 이미 있던 evaluation pipeline과 regression proof를, 로그인, dataset 업로드, KB bundle, 비동기 job, selected-job review UI를 가진 운영 surface로 다시 감싼 것이다.

가장 먼저 눈에 띄는 변화는 auth다. `python/backend/src/core/auth.py`와 `api/routes/auth.py`는 단순하지만 분명한 cookie auth를 추가한다.

이 코드가 중요한 이유는, QA Ops가 더 이상 공개 데모가 아니라 `누가 dataset을 올리고 job을 실행했는가`를 구분해야 하는 화면으로 바뀌었기 때문이다.

```python
cookie_value = create_session_cookie(secret=settings.session_secret, user_id=admin.id, email=admin.email)
response.set_cookie(
    key=SESSION_COOKIE_NAME,
    value=cookie_value,
    httponly=True,
    samesite="lax",
```

그다음 전환점은 `python/backend/src/api/routes/jobs.py`와 `services/jobs.py`다. job route는 dataset과 KB bundle을 받아 evaluation run을 만들고, worker는 pending job을 잡아 turn 단위로 진행률을 갱신한다.

아래 블록이 중요한 이유는, `v2`에서 한 번 실행하던 평가가 이제 운영자가 기다리고 추적할 수 있는 "작업"이 되었다는 점을 보여 주기 때문이다.

```python
job.progress_total = len(turn_ids)
job.progress_completed = 0
job.status = "running"
...
job.progress_completed = index
...
job.status = "completed"
```

이 변화 덕분에 operator는 더 이상 "평가를 한 번 돌린다"가 아니라, "어떤 자료 조합으로 어떤 job을 만들고, 얼마나 끝났는지 본다"는 언어로 일하게 된다.

프런트엔드도 그 변화에 맞춰 설계됐다. `react/src/App.tsx`는 로그인 게이트와 selected job 상태를 유지하고, `react/src/pages/Jobs.tsx`는 dataset, KB bundle, run label, version 정보를 받아 job 생성 폼과 job 테이블을 제공한다.

이 코드 조각은 self-hosted surface가 실제로 어떤 단위를 다루는지 보여 준다. 이전의 golden-set 중심 흐름이 dataset/bundle/job 중심 운영 흐름으로 번역된다.

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

좋은 점은 selected job이 곧바로 Failures, Session Review, Overview 필터로 이어진다는 것이다. 그래서 self-hosted surface가 생겨도 평가 로직 자체가 달라지지 않는다. 바뀌는 건 operator가 그 평가를 다루는 단위뿐이다.

실제 회귀 신호도 확보돼 있다.

```bash
cd capstone/v3-self-hosted-oss/python
UV_PYTHON=python3.12 make gate-all
```

```text
Mypy: no issues found in 51 source files
MP1 2 passed
MP2 4 passed
MP3 2 passed
MP4 1 passed
MP5 1 passed
Frontend 6 passed
Integrity gate passed for target=all
```

이 출력이 증명하는 것은 범위가 넓어졌다는 사실이다. `v2`가 평가 파이프라인과 regression proof를 중심으로 테스트됐다면, `v3`는 로그인, dataset import, job 생성, selected job review 같은 운영 표면까지 포함해 더 넓은 end-user 흐름을 검증한다.

결국 이 트랙의 마지막 단계는 "더 좋은 judge를 만들었다"가 아니라, "이미 있는 평가 체계를 팀이 실제로 운영할 수 있는 형태로 옮겼다"에 가깝다. 그래서 `Chat QA Ops`는 `Rule -> Evidence -> Judge -> Compare -> Review Ops` 순서로 읽을 때 가장 설득력이 크다.
