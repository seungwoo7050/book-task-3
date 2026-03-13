# H-service-boundary-lab Structure Plan

## 한 줄 약속
- 공유 DB를 끊고, identity와 workspace를 claims로만 이어 보기

## 독자 질문
- 단일 백엔드에서 자연스럽게 함께 있던 인증과 워크스페이스 도메인을 어디서 끊을 것인가.
- 인증 서비스와 워크스페이스 서비스를 왜 분리하는가 어떤 데이터는 claim으로 넘기고 어떤 데이터는 넘기지 않는가 서비스별 DB ownership을 어디까지 강제할 것인가 공유 ORM 모델을 금지하면 무엇이 불편해지고 무엇이 명확해지는가

## 서술 원칙
- 기존 `blog/` 초안은 입력 근거로 사용하지 않는다.
- 사실로 확인되는 날짜와 명령은 `git log`와 `docs/verification-report.md`에서만 가져온다.
- finer-grained chronology는 코드/테스트 의존 순서를 바탕으로 복원했다고 명시한다.

## 글 흐름
1. 서비스 분리를 기능 추가가 아니라 경계 선택 문제로 보기
2. compose runtime을 두 서비스로 제한하기
3. system test로 claims-only 협업을 고정하기
4. 2026-03-10 재검증으로 MSA 시작점을 닫기
5. 남은 범위와 다음 비교 대상 정리

## Evidence Anchor
- 주 코드 앵커: `labs/H-service-boundary-lab/fastapi/compose.yaml::__compose__` — runtime이 identity-service와 workspace-service 두 개로만 닫혀 있음을 보여 준다.
- 보조 앵커: `labs/H-service-boundary-lab/fastapi/tests/test_system.py::test_identity_token_then_workspace_creation` — identity에서 받은 token claims만으로 workspace를 생성하는 최소 경계를 보여 준다.
- 문서 앵커: `labs/H-service-boundary-lab/problem/README.md`, `labs/H-service-boundary-lab/docs/README.md`
- CLI 앵커:
- `make lint`
- `make test`
- `make smoke`
- `docker compose up --build`

## 글에서 강조할 개념
- `identity-service`와 `workspace-service`의 책임 경계 bearer claims가 경계 계약으로 쓰이는 이유 공유 ORM 모델을 피하는 이유 서비스 분리를 시작할 때 gateway나 event broker를 일부러 뒤로 미루는 이유
- `identity-service`와 `workspace-service` 분리 기준 서비스별 DB ownership bearer claims 기반 사용자 전달 이벤트 브로커와 gateway는 아직 넣지 않습니다. 로컬 런타임은 SQLite 두 개로 제한합니다.

## 끝맺음
- 제외 범위: 이벤트 브로커 edge gateway websocket과 실시간 전달
- 검증 문장: 2026-03-10에 lint, service unit test, system test, smoke가 통과했다.
