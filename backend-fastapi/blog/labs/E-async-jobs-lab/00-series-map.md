# E-async-jobs-lab

이 글은 요청이 끝났다고 일이 끝난 것은 아닌 순간을 다룬다. E 랩의 관심사는 worker 기술 자체보다, 무엇을 지금 확정하고 무엇을 나중으로 미뤄야 하는지, 그리고 그 handoff를 어떤 상태 모델로 드러낼 것인지에 있다.

## 이 글이 붙잡는 질문
idempotency key, outbox, retry 상태를 포함한 비동기 작업 경계를 어떻게 설명해야 요청-응답 바깥의 일을 신뢰 가능하게 만들 수 있는가가 이 글의 핵심 질문이다.

## 왜 이 프로젝트를 따로 읽어야 하나
README와 docs는 비동기 전달을 별도 boundary로 정의하고, route와 통합 테스트는 enqueue, drain, retry 전이를 독립적으로 검증한다. 그래서 이 랩은 메시지 큐 소개가 아니라 시간 분리 설계를 읽는 글이 된다.

## 이번 글에서 따라갈 흐름
1. 비동기 작업을 기능이 아니라 시간 분리 문제로 정의한다.
2. enqueue와 drain을 다른 route로 나눠 handoff boundary를 드러낸다.
3. retrying에서 sent로 넘어가는 상태 전이를 테스트로 고정한다.
4. 재검증 기록으로 worker와 compose surface를 닫는다.

## 마지막에 확인할 근거
- 코드: `labs/E-async-jobs-lab/fastapi/app/api/v1/routes/jobs.py::drain_outbox`
- 테스트/런타임: `labs/E-async-jobs-lab/fastapi/tests/integration/test_async_jobs.py::test_retrying_job_requires_second_drain`
- CLI: `python3 -m compileall app tests`, `make lint`, `make test`, `make smoke`, `./tools/compose_probe.sh labs/E-async-jobs-lab/fastapi 8003`

## 이 글을 다 읽고 나면
- 요청 시점의 저장과 나중 전달을 왜 같은 트랜잭션으로 보지 않는지 알게 된다.
- outbox와 retry 상태가 운영 가시성과 어떻게 연결되는지 보게 된다.
- idempotency가 비동기 흐름에서 어떤 안전장치인지 감이 잡힌다.
- 검증 기록: 2026-03-09에 compile, lint, test, smoke, Compose live/ready probe가 통과했고, 로컬 학습 실행을 위해 API 스키마 자동 초기화를 두었다.
- 다음으로 이어 볼 대상: F-realtime-lab
