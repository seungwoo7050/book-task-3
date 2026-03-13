# E-async-jobs-lab 개발 타임라인

## 2026-03-09
### Session 1

- 목표: 비동기 작업이라고 하면 처음엔 "Celery worker를 붙이는 것"이 전부라고 생각했다. `problem/README.md`를 먼저 읽어 실제 범위를 확인한다.
- 진행: 성공 기준에 idempotency key, outbox 패턴, 재시도 상태 전이가 들어 있다. 단순 백그라운드 실행이 아니라 "안전하게 넘기는 법"이 핵심이다.
- 이슈: 처음엔 "API가 알림 요청을 받으면 바로 worker에 넘기면 되는 거 아닌가?"라고 생각했다. 그런데 API 호출은 성공했는데 worker 전달이 실패하면? DB에는 남아 있지만 실제 알림은 안 간다.
- 판단: 저장과 전달을 분리해야 한다. API는 DB에 저장만 하고, 별도 drain 단계에서 outbox를 읽어 전달하는 구조로 가기로 했다.

CLI:

```bash
$ cd labs/E-async-jobs-lab/fastapi
$ python3 -m venv .venv
$ source .venv/bin/activate
$ make install
```

### Session 2

- 목표: idempotency key를 구현한다. 같은 요청이 두 번 오면 job이 두 개 만들어지면 안 된다.
- 진행: 처음 시도는 요청마다 무조건 새 job을 만드는 것이었다. 네트워크 재시도로 같은 요청이 두 번 오면 같은 알림이 두 번 발송된다.
- 조치: enqueue 전에 idempotency_key로 먼저 기존 job을 찾고, 있으면 그대로 반환한다.

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

이 블록에서 중요한 건 job과 outbox event를 같은 트랜잭션에서 만든다는 점이다. 처음엔 job만 만들고 outbox는 나중에 넣으려 했는데, 그러면 job은 있지만 outbox가 없는 불일치 상태가 가능하다.

- 검증: 같은 `Idempotency-Key`로 두 번 POST하면 같은 job id가 돌아오는 것을 확인했다.

```python
assert first.json()["id"] == second.json()["id"]
```

CLI:

```bash
$ pytest tests/integration/test_async_jobs.py::test_idempotent_enqueue_and_outbox_drain -q
```

```
1 passed
```

### Session 3

- 목표: drain을 구현한다. outbox에 쌓인 pending event를 읽어 실제 전달을 시도하는 단계다.
- 진행: `process_event`에서 event를 하나씩 읽어 job의 상태를 바꾼다. 성공하면 `sent`, 처리 중이면 `retrying`.
- 이슈: 재시도를 어떻게 테스트하나? 실제 SMTP 실패를 재현하기 어렵다. 처음엔 mock으로 실패를 주입하려 했는데, 더 간단한 방법이 있었다.
- 조치: `retry@`로 시작하는 수신자라면 첫 번째 시도에서 `retrying` 상태로 남기고, 두 번째 drain에서야 `sent`로 바꾸는 학습용 규칙을 넣었다.

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

처음엔 `retry@` 같은 매직 문자열이 너무 인위적이라고 생각했다. 하지만 이 랩의 목적은 "재시도 상태 전이를 관찰하는 것"이므로, 복잡한 실패 시뮬레이터보다 이 한 줄 규칙이 학습 목적에 더 부합한다.

- 검증: retry 수신자에게 첫 drain 후 `retrying`, 두 번째 drain 후 `sent`, `attempt_count == 2`까지 확인.

CLI:

```bash
$ pytest tests/integration/test_async_jobs.py -q
```

```
2 passed
```

### Session 4

- 목표: 전체 검증 루프를 돌리고 Compose 환경에서 API가 뜨는지 확인한다.
- 진행: worker와 Redis를 실제로 올려 전달 경계를 보려면 Compose가 필요하지만, 핵심 검증은 통합 테스트만으로도 끝난다.
- 이슈: 스키마 자동 초기화 이슈. 로컬 학습 환경에서 첫 실행 시 테이블이 없어서 실패. 이전 랩들과 동일하게 lifespan에서 `create_all`을 호출하도록 반영했다.
- 검증: compile, lint, test, smoke, Compose live/ready probe 모두 통과.
- 다음: 이 랩은 저장과 전달의 분리까지만 잡고, 실시간 연결(WebSocket, presence)은 F-realtime-lab으로 넘긴다.

CLI:

```bash
$ python3 -m compileall app tests
$ make lint
$ make test
```

```
2 passed
```

```bash
$ make smoke
$ docker compose up --build
```
