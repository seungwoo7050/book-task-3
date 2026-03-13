# workspace-backend-v2-msa

이 글은 v1과 같은 협업형 도메인을 MSA로 다시 풀었을 때 무엇이 단순해지고 무엇이 더 복잡해지는가를 묻는다. v2 capstone의 목표는 public API는 익숙하게 유지하면서도, 내부 경계와 분산 실패 경로가 어떻게 늘어나는지를 숨기지 않고 드러내는 데 있다.

## 이 글이 붙잡는 질문
같은 public 협업 흐름을 유지한 채 identity, workspace, notification, gateway로 분해하면 어떤 복잡성과 장애 복구 문제가 새로 생기며, 그 사실을 어떤 검증 기록으로 솔직하게 남길 수 있는가가 이 글의 핵심 질문이다.

## 왜 이 프로젝트를 따로 읽어야 하나
capstone README와 docs, compose, system test, verification report가 gateway 아래의 public flow와 notification-service 장애 복구를 독립적으로 설명한다. 그래서 이 프로젝트는 "MSA 버전"이 아니라 단일 백엔드 기준선과 직접 비교하는 최종 비교판이 된다.

## 이번 글에서 따라갈 흐름
1. v1 단일 백엔드 기준선을 다시 분해한다.
2. gateway와 세 서비스의 runtime scope를 compose로 고정한다.
3. public flow와 recovery를 system test 하나로 묶어 본다.
4. 재검증 기록에서 성공과 미완료를 구분해 남긴다.

## 마지막에 확인할 근거
- 코드: `capstone/workspace-backend-v2-msa/fastapi/compose.yaml::__compose__`
- 테스트/런타임: `capstone/workspace-backend-v2-msa/fastapi/tests/test_system.py::test_v2_system_flow_and_notification_recovery`
- CLI: `make test`, `docker compose up --build -d`, `docker build --progress=plain -t workspace-v2-identity-fresh ./services/identity-service`, `docker pull python:3.12-slim`, `docker compose -p workspace-backend-v2-msa-dd63448c -f compose.yaml up -d --no-build`, `inline Python end-to-end flow for register -> verify -> login -> invite -> comment -> drain -> recovery -> websocket`

## 이 글을 다 읽고 나면
- 브라우저 경계가 왜 gateway에 남아야 하는지 더 분명해진다.
- 서비스별 DB ownership과 bearer claims 규칙이 어떻게 함께 작동하는지 이해하게 된다.
- 이벤트, recovery, websocket이 분산 환경에서 어떤 추가 비용을 만드는지 보게 된다.
- 검증 기록: 2026-03-10에 service unit tests는 통과했고, fresh build 경로는 Docker Desktop 문제로 성공 기록을 남기지 못했지만 prebuilt image 기준 Compose runtime과 end-to-end 협업 흐름 검증은 완료했다.
- 다음으로 이어 볼 대상: 비교 기준선은 workspace-backend
