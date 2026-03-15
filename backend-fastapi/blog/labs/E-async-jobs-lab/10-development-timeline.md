# E-async-jobs-lab development timeline

이 글은 E 랩을 "비동기 큐 붙이기"로 요약하지 않는다. 현재 남아 있는 source of truth를 따라가면, 이 프로젝트의 핵심은 요청-응답 안에서 무엇을 확정하고 무엇을 나중으로 미룰지 명시하는 데 있다. 실제로 중요한 건 Celery 자체보다 `Idempotency-Key`, outbox event, `queued -> retrying -> sent` 상태 전이, 그리고 eager worker로 그 경계를 재현하는 테스트 루프다.

## Phase 1. 문제 정의가 worker보다 handoff boundary를 먼저 요구한다

[`problem/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/problem/README.md) 와 [`docs/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/docs/README.md) 를 보면, 이 랩이 먼저 묻는 건 "어떤 큐를 쓸 것인가"가 아니다. 중복 요청을 어떻게 흡수할지, 저장과 전달 사이를 어디서 자를지, retry 가능한 상태를 어떻게 드러낼지가 더 앞에 있다.

이 순서가 중요하다. 비동기 예제를 읽을 때 흔히 worker 프로세스나 broker 설정부터 보게 되지만, E 랩은 오히려 시간축을 먼저 설계한다. 지금 확정되는 건 enqueue 요청과 outbox 저장이고, 실제 전달은 나중 단계로 미뤄진다. 그래서 이 랩의 설명도 기술 스택이 아니라 handoff boundary에서 시작해야 자연스럽다.

## Phase 2. enqueue는 단순 생성이 아니라 idempotency 저장 계약이 된다

[`jobs.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/app/api/v1/routes/jobs.py) 와 [`JobsService`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/app/domain/services/jobs.py) 를 보면, `POST /notifications`는 그냥 job row를 하나 넣는 endpoint가 아니다. `Idempotency-Key`를 헤더로 받고, 동일 키가 이미 있으면 기존 job을 그대로 반환한다. 새 키라면 `notification_jobs`와 `outbox_events`를 같은 세션 안에서 함께 저장한다.

```python
existing = self.repository.get_job_by_idempotency_key(idempotency_key)
if existing:
    return existing
job = NotificationJob(
    idempotency_key=idempotency_key,
    recipient=recipient,
    subject=subject,
    status="queued",
    attempt_count=0,
)
self.repository.save(job)
self.repository.save(OutboxEvent(job_id=job.id, status="pending"))
```

이 구조 덕분에 "중복 요청 방지"가 추상 규칙이 아니라 저장 계약으로 바뀐다. 동시에 [`schemas/jobs.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/app/schemas/jobs.py) 가 `recipient: EmailStr`를 쓰기 때문에, 이 랩의 런타임은 곧바로 `email-validator` dependency와도 연결된다.

## Phase 3. outbox handoff는 분명하지만 drain endpoint가 다시 동기적으로 닫는다

실제 handoff를 가장 잘 보여 주는 건 `POST /outbox/drain`이다. 이 route는 service에서 바로 끝나지 않고, repository로 `pending` 또는 `retrying` event를 꺼낸 뒤 각 event를 Celery task로 보낸다. 그런데 곧바로 `.get()`으로 결과를 기다린다.

```python
for event in repository.list_pending_events():
    dispatched.append(deliver_notification.delay(event.id).get())
```

여기서 이 랩의 현재 성격이 선명해진다. outbox는 분명히 별도 단계로 존재하지만, drain API 자체는 아직 fire-and-forget로 풀리지 않았다. 학습 목적상 handoff를 눈에 보이게 만들려는 선택에 가깝고, 완전히 비동기적인 운영 경계를 흉내 내기보다 "언제 저장하고 언제 비우는가"를 이해시키는 데 초점이 있다.

## Phase 4. 상태 기계는 retry를 정상 경로로 다루지만 failure는 아직 비워 둔다

[`process_event()`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/app/domain/services/jobs.py) 를 보면 상태 전이는 단순하다. 기본은 `queued`에서 시작하고, 수신자가 `retry@`로 시작하면서 첫 시도라면 `retrying`으로 남긴다. 그다음 drain에서는 `sent`로 닫힌다.

```python
job.attempt_count += 1
if job.recipient.startswith("retry@") and job.attempt_count == 1:
    job.status = "retrying"
    event.status = "retrying"
    self.session.commit()
    return event
job.status = "sent"
event.status = "delivered"
```

이 랩이 좋은 건 retry를 오류 꼬리표가 아니라 정상 상태 전이로 드러낸다는 점이다. 하지만 같은 이유로 현재 한계도 보인다. 문제 정의는 성공, 재시도, 실패를 구분하라고 말하지만, 실제 코드에는 terminal `failed` 상태가 없다. 문서가 이 간극을 지우면 구현보다 더 성숙한 작업 상태 기계처럼 보이게 된다.

## Phase 5. 테스트는 비동기 인프라를 eager 모드로 접어 넣어 학습 루프를 만든다

[`tests/conftest.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi/tests/conftest.py) 는 `CELERY_TASK_ALWAYS_EAGER=true`, `CELERY_BROKER_URL=memory://`, `CELERY_RESULT_BACKEND=cache+memory://`를 주고 임시 SQLite DB를 세팅한다. 즉 테스트는 분산 환경을 재현하지 않고, 비동기 경계를 동기적으로 관찰 가능한 학습 루프로 바꾼다.

통합 테스트는 그 위에서 두 가지를 고정한다. 같은 `Idempotency-Key`를 두 번 보내도 같은 job id가 나와야 하고, `retry@example.com`은 첫 drain 뒤 `retrying`, 두 번째 drain 뒤 `sent`가 되어야 한다.

```python
first_drain = client.post("/api/v1/jobs/outbox/drain")
assert first_drain.status_code == 200
first_job = client.get(f"/api/v1/jobs/notifications/{job.json()['id']}")
assert first_job.json()["status"] == "retrying"

second_drain = client.post("/api/v1/jobs/outbox/drain")
second_job = client.get(f"/api/v1/jobs/notifications/{job.json()['id']}")
assert second_job.json()["status"] == "sent"
assert second_job.json()["attempt_count"] == 2
```

이 테스트 덕분에 E 랩은 "큐를 붙였다"가 아니라 "retry를 포함한 상태 전이를 어디까지 API로 관찰할 수 있는가"를 보여 주는 실습이 된다.

## Phase 6. 오늘 다시 돌린 검증은 lint와 런타임 의존성 상태를 분리해서 보여 준다

2026-03-14 현재 셸에서 다시 실행한 명령은 아래와 같다.

```bash
make lint
make test
make smoke
PYTHONPATH=. pytest
PYTHONPATH=. python -m tests.smoke
```

오늘 확인한 결과는 이렇다.

- `make lint`: 통과.
- `make test`: `ModuleNotFoundError: No module named 'app'`.
- `make smoke`: Homebrew `python3` 기준 `ModuleNotFoundError: No module named 'fastapi'`.
- `PYTHONPATH=. pytest`: `EmailStr` import 단계에서 `email-validator is not installed`.
- `PYTHONPATH=. python -m tests.smoke`: 같은 `email-validator` import 오류로 실패.

이 결과는 의미가 분명하다. 코드 스타일과 정적 품질은 깨끗하지만, 현재 셸에서 앱을 실제로 import해서 테스트 루프를 끝까지 돌리려면 path와 Python dependency가 먼저 맞아야 한다. 특히 E 랩은 `EmailStr` 때문에 `email-validator`가 없으면 API import 자체가 막힌다.

## 정리

E-async-jobs-lab이 실제로 보여 주는 건 Celery 설정법보다 handoff를 어디서 자르는가다. enqueue 시점에는 idempotency와 outbox 저장만 확정하고, drain 단계에서 worker task를 밀어 넣으며, retry는 정상 상태 전이로 다룬다. 동시에 현재 구현은 drain endpoint가 다시 결과를 기다리고, failure 종착지는 비워 두고 있으며, 현재 셸에서는 `email-validator` 부재 때문에 앱 import가 막힌다. 이 사실들을 같이 남겨야 다음 F 랩에서 실시간 전달을 볼 때도 "요청 밖으로 밀어낸 일"과 "지금 연결된 상태"를 어떻게 다르게 다뤄야 하는지 이어서 읽을 수 있다.
