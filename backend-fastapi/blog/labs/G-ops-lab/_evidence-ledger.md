# G-ops-lab Evidence Ledger

## 독립 프로젝트 판정
- 판정: 처리 대상
- 이유: 프로젝트 README와 docs가 운영성 자체를 독립 주제로 잡고, `tests/integration/test_ops.py`, workflow matrix, Compose probe가 서로 다른 검증 축을 제공한다.
- 프로젝트 질문: 학습용 백엔드에서도 liveness, readiness, metrics, CI, target shape 문서를 어디까지 분리해서 보여줘야 하는가.
- 주의: finer-grained 구현 순서는 commit granularity가 거칠어서 README, docs, code surface, tests 의존 순서를 바탕으로 복원했다. 실제 날짜가 확인되는 부분은 git log와 검증 보고서에만 한정했다.

## 소스 인벤토리
- `labs/G-ops-lab/README.md`
- `labs/G-ops-lab/problem/README.md`
- `labs/G-ops-lab/docs/README.md`
- `labs/G-ops-lab/fastapi/README.md`
- `labs/G-ops-lab/fastapi/Makefile`
- `labs/G-ops-lab/fastapi/compose.yaml`
- `backend-fastapi/.github/workflows/labs-fastapi.yml`
- `backend-fastapi/docs/verification-report.md`
- `backend-fastapi/labs/G-ops-lab/fastapi/app/api/v1/routes/ops.py`
- `backend-fastapi/labs/G-ops-lab/fastapi/tests/integration/test_ops.py`
- `git log -- backend-fastapi/labs/G-ops-lab`

## 프로젝트 표면 요약
- 문제 요약: 기능은 단순해도, 백엔드가 어떻게 살아 있는지 확인하고 어떻게 배포 가정을 설명할지 정리해야 합니다. health check, readiness, metrics, CI, 배포 문서는 개발용 API와 별개의 운영성 문제입니다. live / ready health endpoint가 구분되어야 합니다. 요청 수 같은 최소 metrics surface가 있어야 합니다. 상세 성공 기준과 제외 범위는 problem/README.md에 둡니다.
- 성공 기준: live / ready health endpoint가 구분되어야 합니다. 요청 수 같은 최소 metrics surface가 있어야 합니다. 로컬 Compose 부팅과 CI 명령이 정리되어야 합니다. AWS target shape가 실제 배포 완료처럼 과장되지 않고 문서로 설명되어야 합니다.
- 설계 질문: liveness와 readiness는 왜 분리해야 하는가 "최소 metrics"는 어떤 운영 질문에 답해야 하는가 배포 문서는 어디까지 사실이고 어디부터 가정인가
- 실제 검증 surface: make lint make test make smoke docker compose up --build 실행과 환경 설명은 fastapi/README.md에서 다룹니다. 마지막 기록된 실제 검증 결과는 ../../docs/verification-report.md에 있습니다.

## 시간 표지
- 2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료
- 2026-03-10 a3edce2 docs: enhance backend-fastapi
- 2026-03-09 7813150 docs(notion): front-react, backend-fastapi
- 2026-03-09 73372bd Add project: backend-fastapi, backend-spring, cpp-server

## Chronology Ledger
| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1, 2026-03-09 add project commit 73372bd를 기준으로 복원 | 학습용 API에서도 운영 기준을 따로 설명할 수 있게 만들기 | README.md, problem/README.md, docs/README.md | health endpoint 하나만 있어도 운영성 설명이 가능할 것 | live/ready, request-count metrics, JSON 로그, CI, AWS target shape 문서를 같은 프로젝트 범위로 묶음 | README의 `make run`, `docker compose up --build` | 문제 정의가 live/ready 분리와 metrics, Compose/CI, target shape를 모두 성공 기준으로 둠 | problem/README.md 성공 기준 | 운영성은 기능 부록이 아니라 별도 질문 묶음으로 봐야 설명이 가능하다 | health와 metrics route 구현 |
| 2 | Phase 2, route/runtime 의존성으로 복원 | liveness와 readiness를 같은 상태로 보지 않는 surface 만들기 | app/api/v1/routes/health.py, app/api/v1/routes/ops.py, app/runtime.py | 단순 `/health` 하나면 충분할 것 | `/health/live`, `/ops/ready`, `/ops/metrics`를 분리하고 metrics registry를 앱 state로 둠 | `make test` | metrics route가 Prometheus text 형식으로 `app_requests_total`을 반환 | app/api/v1/routes/ops.py::metrics | 운영 질문은 '살아 있는가'와 '요청을 받을 준비가 됐는가'를 다르게 묻는다 | 테스트와 workflow로 surface 고정 |
| 3 | Phase 3, 테스트와 CI surface 정리 | ops route가 문서뿐 아니라 회귀 테스트와 workflow로 유지되게 만들기 | tests/integration/test_ops.py, .github/workflows/labs-fastapi.yml, tools/compose_probe.sh | metrics 출력은 사람이 눈으로 확인하면 충분할 것 | live/ready/metrics를 통합 테스트로 묶고, workflow matrix에 workspace를 등록 | `make test`, `make smoke` | test가 live 200, ready 200, metrics text에 `app_requests_total` 포함 여부를 확인 | tests/integration/test_ops.py::test_live_ready_and_metrics | 운영성도 endpoint를 만든 뒤엔 자동 검증 표면이 함께 있어야 금세 썩지 않는다 | 실제 재실행 기록과 문서 구분 정리 |
| 4 | 2026-03-09 재검증 + 2026-03-11 track polish | 운영 문서가 실제 사실과 target shape를 혼동하지 않도록 닫기 | docs/verification-report.md, docs/aws-deployment.md, fastapi/README.md | AWS target shape 문서를 쓰면 배포가 된 것처럼 읽힐 수 있다 | compile, lint, test, smoke, Compose probe는 사실로 적고, AWS는 문서 수준 target shape로 구분 | `python3 -m compileall app tests`, `make lint`, `make test`, `make smoke`, `./tools/compose_probe.sh labs/G-ops-lab/fastapi 8005` | 2026-03-09 기준 재검증 통과, docs가 실제 배포 완료를 주장하지 않음 | docs/verification-report.md G-ops-lab 항목 | 운영성 글에서는 '확인된 사실'과 '배치 가정'을 분리해서 써야 과장이 줄어든다 | capstone 통합 구조로 이동 |
