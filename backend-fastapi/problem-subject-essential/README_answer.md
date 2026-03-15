# backend-fastapi 서버 개발 필수 답안지

이 문서는 FastAPI 트랙에서 서버 공통으로 바로 이어지는 두 랩을 실제 앱 코드와 테스트 기준으로 정리한 답안지다. 핵심은 “프레임워크 문법”이 아니라, 비동기 작업 경계와 운영 경계를 FastAPI 애플리케이션 안에서 어떻게 분리하느냐다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [e-async-jobs-lab-fastapi](e-async-jobs-lab-fastapi_answer.md) | 시작 위치의 구현을 완성해 작업 enqueue 요청이 idempotency key를 받아야 합니다, outbox를 통해 저장과 전달 사이의 경계가 설명 가능해야 합니다, worker가 재시도 가능한 작업을 처리할 수 있어야 합니다를 한 흐름으로 설명하고 검증한다. 핵심은 get_jobs_service 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi && PYTHONPATH=. python3 -m pytest` |
| [g-ops-lab-fastapi](g-ops-lab-fastapi_answer.md) | 시작 위치의 구현을 완성해 live / ready health endpoint가 구분되어야 합니다, 요청 수 같은 최소 metrics surface가 있어야 합니다, 로컬 Compose 부팅과 CI 명령이 정리되어야 합니다를 한 흐름으로 설명하고 검증한다. 핵심은 get_metrics_registry 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi && PYTHONPATH=. python3 -m pytest` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
