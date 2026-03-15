# backend-fastapi 서버 개발 필수 문제지

`backend-fastapi`는 협업형 웹 API 트랙이지만, 그 안에서도 서버 공통으로 바로 이어지는 문제만 엄격하게 남깁니다.
이 트랙의 종합 과제는 [`../problem-subject-capstone/README.md`](../problem-subject-capstone/README.md)로 분리합니다.

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [e-async-jobs-lab-fastapi](e-async-jobs-lab-fastapi.md) | 시작 위치의 구현을 완성해 작업 enqueue 요청이 idempotency key를 받아야 합니다, outbox를 통해 저장과 전달 사이의 경계가 설명 가능해야 합니다, worker가 재시도 가능한 작업을 처리할 수 있어야 합니다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/E-async-jobs-lab/fastapi && PYTHONPATH=. python3 -m pytest` |
| [g-ops-lab-fastapi](g-ops-lab-fastapi.md) | 시작 위치의 구현을 완성해 live / ready health endpoint가 구분되어야 합니다, 요청 수 같은 최소 metrics surface가 있어야 합니다, 로컬 Compose 부팅과 CI 명령이 정리되어야 합니다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi && PYTHONPATH=. python3 -m pytest` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
