# E-async-jobs-lab Structure Plan

## 한 줄 약속
- 요청-응답을 끝내는 대신, outbox와 retry 상태를 먼저 보여주기

## 독자 질문
- 알림 작업을 바로 실행하지 않고 뒤로 넘길 때, 어떤 저장과 전달 경계를 드러내야 안전하다고 말할 수 있는가.
- 작업을 바로 실행하지 않고 outbox에 한 번 더 저장하는 이유는 무엇인가 idempotency key는 중복 요청과 어떤 관계가 있는가 retry 가능한 실패와 바로 종료해야 하는 실패는 어떻게 다른가

## 서술 원칙
- 기존 `blog/` 초안은 입력 근거로 사용하지 않는다.
- 사실로 확인되는 날짜와 명령은 `git log`와 `docs/verification-report.md`에서만 가져온다.
- finer-grained chronology는 코드/테스트 의존 순서를 바탕으로 복원했다고 명시한다.

## 글 흐름
1. 비동기 작업을 별도 boundary로 떼어내기
2. enqueue와 drain을 다른 route로 나누기
3. retry 상태를 테스트로 고정하기
4. 2026-03-09 재검증으로 worker surface를 다시 닫기
5. 남은 범위와 다음 비교 대상 정리

## Evidence Anchor
- 주 코드 앵커: `labs/E-async-jobs-lab/fastapi/app/api/v1/routes/jobs.py::drain_outbox` — 요청과 worker 실행 사이에 repository와 Celery task를 명시적으로 끼워 넣는다.
- 보조 앵커: `labs/E-async-jobs-lab/fastapi/tests/integration/test_async_jobs.py::test_retrying_job_requires_second_drain` — 첫 drain에서 retrying, 두 번째 drain에서 sent가 되는 상태 전이를 고정한다.
- 문서 앵커: `labs/E-async-jobs-lab/problem/README.md`, `labs/E-async-jobs-lab/docs/README.md`
- CLI 앵커:
- `python3 -m compileall app tests`
- `make lint`
- `make test`
- `make smoke`
- `./tools/compose_probe.sh <workspace> <host-port>`

## 글에서 강조할 개념
- outbox handoff boundary worker가 담당하는 책임 작업 상태 전이의 최소 모델
- 비동기 enqueue와 실제 실행의 분리 outbox handoff idempotency key 대규모 분산 메시징 대신 로컬 Redis + Celery 조합으로 제한합니다. 알림 도메인은 일반화된 예시로 유지합니다.

## 끝맺음
- 제외 범위: 대규모 메시징 시스템 비교 고급 스케줄링과 운영 대시보드 실서비스 수준의 분산 장애 복구 실험
- 검증 문장: 2026-03-09에 compile, lint, test, smoke, Compose live/ready probe가 통과했고, 로컬 학습 실행을 위해 API 스키마 자동 초기화를 두었다.
