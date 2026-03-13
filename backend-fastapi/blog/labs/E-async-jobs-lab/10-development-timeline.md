# E-async-jobs-lab: 요청-응답을 끝내는 대신, outbox와 retry 상태를 먼저 보여주기

이 글은 `labs/E-async-jobs-lab/README.md`, `problem/README.md`, `docs/README.md`, `labs/E-async-jobs-lab/fastapi/app/api/v1/routes/jobs.py::drain_outbox`, `labs/E-async-jobs-lab/fastapi/tests/integration/test_async_jobs.py::test_retrying_job_requires_second_drain`, `backend-fastapi/docs/verification-report.md`를 바탕으로 실제 구현 순서를 다시 복원한다.

E 랩이 바꾸는 건 기능보다 시간축이다. problem/README.md는 요청을 받고 바로 일을 끝내는 대신, idempotency key, outbox, retry 상태를 먼저 설명하라고 요구한다. docs/README.md 역시 worker보다 handoff boundary를 먼저 묻는다. 그래서 이 글도 queue 기술 선택보다 '무엇을 언제 확정하고 언제 뒤로 미루는가'에 초점을 둔다.

## 1. 비동기 작업을 별도 boundary로 떼어내기
첫 단계에서 비동기 작업은 알림 기능이 아니라 시간 분리 문제로 정의된다. README.md가 enqueue API, outbox 저장, Celery worker 실행, retry 상태 모델을 같이 묶는 이유도 여기에 있다. 즉 프로젝트의 중심은 worker 프로세스 그 자체보다 요청-응답 밖으로 어떤 책임을 밀어내는지 정하는 일이다.

## 2. enqueue와 drain을 다른 route로 나누기
코드에서는 drain_outbox가 그 경계를 가장 잘 보여 준다. 이 함수는 서비스 객체를 받지만, 실제로는 repository에서 pending event를 읽고 각 이벤트를 deliver_notification.delay(...).get()으로 넘긴다. 저장과 dispatch가 한 route 안에서 명시적으로 분리되니, 글에서도 outbox가 왜 중간 단계인지 훨씬 선명하게 설명할 수 있다.

```python
def drain_outbox(service: Annotated[JobsService, Depends(get_jobs_service)]) -> DrainResponse:
    repository = JobsRepository(service.session)
    dispatched = []
    for event in repository.list_pending_events():
        dispatched.append(deliver_notification.delay(event.id).get())
    return DrainResponse(processed=len(dispatched), statuses=dispatched)


@router.get("/notifications/{job_id}", response_model=JobResponse)
def get_job(
    job_id: str,
    service: Annotated[JobsService, Depends(get_jobs_service)],
```

여기서 보이는 건 저장과 worker dispatch 사이에 의도적인 handoff 단계가 놓여 있다는 점이다.

## 3. retry 상태를 테스트로 고정하기
테스트는 retry를 정상 경로로 만들어 준다. 첫 번째 테스트는 같은 Idempotency-Key를 두 번 보내도 같은 job id가 돌아오는지 본다. 두 번째 테스트는 첫 drain 뒤 status가 retrying이고, 두 번째 drain 뒤에야 sent와 attempt_count == 2가 되는지 확인한다. 이 흐름이 있기 때문에 retry를 에러 꼬리표가 아니라 상태 기계의 일부로 서술할 수 있다.

```python
def test_retrying_job_requires_second_drain(client) -> None:
    job = client.post(
        "/api/v1/jobs/notifications",
        json={"recipient": "retry@example.com", "subject": "Retry me"},
        headers={"Idempotency-Key": "job-2"},
    )
    assert job.status_code == 200

    first_drain = client.post("/api/v1/jobs/outbox/drain")
    assert first_drain.status_code == 200
    first_job = client.get(f"/api/v1/jobs/notifications/{job.json()['id']}")
    assert first_job.json()["status"] == "retrying"
```

테스트는 첫 drain의 retrying과 두 번째 drain의 sent 전이를 실제로 확인한다.

## 4. 2026-03-09 재검증으로 worker surface를 다시 닫기
보고서 기준 2026-03-09 재검증은 compile, lint, test, smoke, Compose probe를 모두 포함한다. 거기에 API 스키마 자동 초기화 메모까지 붙어 있어서, 이 프로젝트가 문서 수준 가정이 아니라 실제 로컬 워크스페이스로 다시 살아났다는 사실을 보여 준다. 비동기 작업 예제도 독립 프로젝트가 되려면 결국 이런 실행 surface가 필요하다.

```bash
python3 -m compileall app tests
make lint
make test
make smoke
./tools/compose_probe.sh labs/E-async-jobs-lab/fastapi 8003
```

2026-03-09에 compile, lint, test, smoke, Compose live/ready probe가 통과했고, 로컬 학습 실행을 위해 API 스키마 자동 초기화를 두었다. 이 랩은 메시징 인프라 전체보다 enqueue -> outbox -> drain -> status 조회 순서를 재현하는 데 초점을 둔다.

## 정리
E 랩의 핵심은 '나중에 처리한다'는 말 대신, 무엇을 outbox에 남기고 어떤 상태를 retry로 볼지 명시했다는 점이다. 이 결정이 다음 F 랩에서 실시간 전달을 붙일 때도, 요청-응답 밖으로 밀어낸 일과 연결 상태를 어떻게 다르게 다룰지 설명하는 발판이 된다.
