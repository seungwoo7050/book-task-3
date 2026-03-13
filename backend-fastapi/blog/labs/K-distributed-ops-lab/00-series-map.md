# K-distributed-ops-lab

이 글은 분산 구조가 된 뒤 마지막으로 남는 운영 surface를 다룬다. K 랩의 관심사는 새 기능이 아니라, 여러 서비스의 health, metrics, request correlation을 어떤 최소 단위로 읽을 수 있게 만들 것인가에 있다.

## 이 글이 붙잡는 질문
여러 서비스가 동시에 살아 움직이는 상황에서 live/ready, metrics, correlation id를 어떻게 남겨야 문제를 추적 가능한 시스템으로 읽을 수 있는가가 이 글의 질문이다.

## 왜 이 프로젝트를 따로 읽어야 하나
README와 docs는 운영 관찰성을 분산 구조의 별도 주제로 설명하고, compose와 system test는 협업 흐름과 장애 복구를 실제 runtime 위에서 검증한다. 그래서 이 프로젝트는 MSA 운영성을 따로 읽는 마지막 랩이 된다.

## 이번 글에서 따라갈 흐름
1. 분산 구조의 운영 surface를 별도 문제로 끌어올린다.
2. service label이 붙은 metrics와 correlation 흐름을 확인한다.
3. system test와 smoke로 장애 복구까지 묶는다.
4. 재검증 기록으로 최종 MSA 운영 랩을 닫는다.

## 마지막에 확인할 근거
- 코드: `labs/K-distributed-ops-lab/fastapi/gateway/app/api/v1/routes/ops.py::metrics`
- 테스트/런타임: `labs/K-distributed-ops-lab/fastapi/tests/test_system.py::test_v2_system_flow_and_notification_recovery`
- CLI: `make test`, `make smoke`, `docker compose up --build`

## 이 글을 다 읽고 나면
- service label이 붙은 metrics가 왜 분산 환경에서 기본값이 되는지 이해하게 된다.
- request correlation이 단순 로그 포맷이 아니라 추적 계약이라는 점이 보인다.
- 운영 검증이 기능 테스트와 어떻게 다른지 감이 잡힌다.
- 검증 기록: 2026-03-10에 gateway/identity/workspace/notification unit test, system test, smoke가 통과했다.
- 다음으로 이어 볼 대상: workspace-backend-v2-msa
