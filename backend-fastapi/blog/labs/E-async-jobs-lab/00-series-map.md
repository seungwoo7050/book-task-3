# E-async-jobs-lab 시리즈 지도

이 시리즈는 요청-응답 뒤로 밀려나는 비동기 작업을 `idempotency key`와 outbox 경계로 설명하는 방법을 실제 소스 기준으로 다시 읽습니다.

## 이 시리즈가 보는 문제

- 같은 알림 요청이 두 번 와도 같은 job으로 흡수되어야 합니다.
- 저장과 전달을 같은 성공으로 다루지 않고, outbox를 거쳐 단계적으로 설명할 수 있어야 합니다.

## 실제 구현 표면

- `/api/v1/jobs/notifications`
- `Idempotency-Key` 헤더
- `/api/v1/jobs/outbox/drain`
- `queued`, `retrying`, `sent` 상태 전이

## 대표 검증 엔트리

- `pytest tests/integration/test_async_jobs.py -q`
- `make smoke`
- `docker compose up --build`

## 읽는 순서

1. [프로젝트 README](../../../labs/E-async-jobs-lab/README.md)
2. [문제 정의](../../../labs/E-async-jobs-lab/problem/README.md)
3. [실행 진입점](../../../labs/E-async-jobs-lab/fastapi/README.md)
4. [대표 통합 테스트](../../../labs/E-async-jobs-lab/fastapi/tests/integration/test_async_jobs.py)
5. [핵심 구현](../../../labs/E-async-jobs-lab/fastapi/app/domain/services/jobs.py)
6. [개발 타임라인](10-development-timeline.md)

## 근거 파일

- [README.md](../../../labs/E-async-jobs-lab/README.md)
- [problem/README.md](../../../labs/E-async-jobs-lab/problem/README.md)
- [fastapi/README.md](../../../labs/E-async-jobs-lab/fastapi/README.md)
- [tests/integration/test_async_jobs.py](../../../labs/E-async-jobs-lab/fastapi/tests/integration/test_async_jobs.py)
- [app/domain/services/jobs.py](../../../labs/E-async-jobs-lab/fastapi/app/domain/services/jobs.py)
- [docs/verification-report.md](../../../docs/verification-report.md)
