# G-ops-lab structure plan

## 한 줄 약속

- 운영성을 health endpoint 모음이 아니라 alive, ready, metrics, logging, target-shape 문서를 구분해서 읽는 최소 surface로 만든다.

## 독자 질문

- 왜 이 랩은 `health/ready`와 `ops/ready`를 같은 의미로 다루지 않는가
- 인메모리 request counter와 JSON logging만으로도 어떤 운영 질문까지는 답할 수 있는가
- AWS 문서는 왜 구현 산출물이 아니라 target shape 설명으로만 남아 있어야 하는가
- 어떤 surface가 실제로 검증됐고, 어떤 surface는 문서 가정으로만 남았는가
- 현재 문서에 적힌 검증 명령은 지금 셸에서 그대로 재현되는가

## 이번 Todo의 작성 원칙

- 다른 lab 문장이나 구조를 가져오지 않는다.
- 기존 `blog/` 본문은 사실 근거로 사용하지 않는다.
- `problem/README`, source code, tests, 실제 재실행 CLI만으로 서사를 복원한다.
- 구현된 ops surface와 문서-only target shape를 섞지 않는다.

## 글 흐름

1. 문제 정의가 기능보다 운영 질문을 먼저 묻는다는 점부터 고정한다.
2. live, dependency-ready, config-ready, metrics를 각 route에서 분리해 읽는다.
3. middleware 기반 request counter와 JSON logging이 남기는 최소 운영 신호를 설명한다.
4. 통합 테스트, smoke, AWS target-shape 문서를 함께 놓고 검증된 사실과 가정을 구분한다.
5. 오늘 다시 돌린 CLI 결과로 현재 재현 가능 상태를 닫는다.

## Evidence anchor

- 주 코드 앵커: [ops.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/app/api/v1/routes/ops.py)
- 보조 코드 앵커: [health.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/app/api/v1/routes/health.py), [main.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/app/main.py), [runtime.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/app/runtime.py), [logging.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/app/core/logging.py)
- 테스트 루프 앵커: [test_ops.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/tests/integration/test_ops.py), [smoke.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/tests/smoke.py)
- 문서 경계 앵커: [aws-deployment.md](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/docs/aws-deployment.md)
- CLI 앵커: `make lint`, `make test`, `make smoke`, `PYTHONPATH=. pytest`, `PYTHONPATH=. python -m tests.smoke`

## 끝에서 남겨야 할 문장

- 이 랩의 강점은 작은 서비스에서도 alive, dependency-ready, config summary, metrics, logging을 서로 다른 운영 표면으로 읽게 만든다는 점이다.
- 이 랩의 현재 한계는 metrics가 인메모리 counter에 머물고, AWS는 문서 수준 target shape일 뿐이며, 2026-03-14 셸에서는 기본 `make` 진입점이 path/interpreter와 `health.py` lint 문제로 바로 닫히지 않는다는 점이다.
- 다음 단계인 `workspace-backend`나 이후 트랙을 읽을 때도, 무엇이 실제 운영 surface이고 무엇이 deployment assumption인지 이 기준으로 구분하게 된다.
