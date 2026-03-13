# H-service-boundary-lab

이 글은 단일 백엔드에서 자연스럽게 함께 있던 인증과 워크스페이스 도메인을 어디서 끊을 것인가라는 질문에서 출발한다. H 랩은 MSA 전체를 한꺼번에 보여 주지 않고, 가장 작은 서비스 분해가 claims만으로 어디까지 가능한지부터 차근히 확인한다.

## 이 글이 붙잡는 질문
서비스가 서로의 DB를 직접 읽지 않고도 협업 흐름을 시작할 수 있으려면 어디서 경계를 끊어야 하는가, 그리고 bearer claims만으로 어떤 계약을 만들 수 있는가가 이 글이 붙잡는 질문이다.

## 왜 이 프로젝트를 따로 읽어야 하나
README와 problem 문서는 identity와 workspace의 DB ownership을 핵심 기준으로 삼고, compose와 system test는 실제 runtime을 두 서비스로 제한한다. 그래서 이 글은 "MSA 맛보기"가 아니라 첫 경계 선택을 읽는 문서가 된다.

## 이번 글에서 따라갈 흐름
1. 서비스 분리를 기능 추가가 아니라 경계 선택 문제로 본다.
2. compose runtime을 두 서비스로 제한해 범위를 고정한다.
3. claims-only 협업이 system test에서 어떻게 증명되는지 본다.
4. 재검증 기록으로 MSA 시작점을 닫는다.

## 마지막에 확인할 근거
- 코드: `labs/H-service-boundary-lab/fastapi/compose.yaml::__compose__`
- 테스트/런타임: `labs/H-service-boundary-lab/fastapi/tests/test_system.py::test_identity_token_then_workspace_creation`
- CLI: `make lint`, `make test`, `make smoke`, `docker compose up --build`

## 이 글을 다 읽고 나면
- `identity-service`와 `workspace-service`의 책임 경계가 또렷해진다.
- bearer claims가 왜 첫 경계 계약으로 자주 쓰이는지 이해하게 된다.
- gateway나 broker를 일부러 뒤로 미루는 이유가 보이기 시작한다.
- 검증 기록: 2026-03-10에 lint, service unit test, system test, smoke가 통과했다.
- 다음으로 이어 볼 대상: I-event-integration-lab
