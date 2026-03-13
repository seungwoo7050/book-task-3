# workspace-backend

이 글은 분리해서 배운 인증, 인가, 데이터 API, 비동기 알림, 실시간 전달을 하나의 협업형 백엔드 안에서 다시 조합하면 무엇을 다시 설계해야 하는가를 묻는다. workspace-backend는 A~G 랩의 결과를 단순히 합쳐 둔 폴더가 아니라, 여러 경계가 한 사용자 흐름 안에서 어떻게 만나는지 보여 주는 단일 백엔드 기준선이다.

## 이 글이 붙잡는 질문
인증과 인가, 데이터 조작, 알림, 실시간 전달을 한 제품형 구조에 묶을 때 어떤 경계는 합쳐지고 어떤 경계는 그대로 남는가, 그리고 그 선택을 어떤 통합 흐름으로 증명할 수 있는가가 이 글의 핵심 질문이다.

## 왜 이 프로젝트를 따로 읽어야 하나
capstone README와 docs는 랩들의 단순 합이 아니라 협업형 SaaS 도메인으로 다시 조합된 범위를 설명하고, 통합 테스트는 로컬 로그인과 Google 로그인, invite, comment, drain, websocket을 한 흐름으로 묶는다. 그래서 이 프로젝트는 이후 MSA 비교를 위한 기준선으로 따로 읽을 가치가 있다.

## 이번 글에서 따라갈 흐름
1. 랩에서 배운 답을 협업형 제품 도메인으로 다시 묶는다.
2. platform route에 협업 흐름이 어디서 만나는지 본다.
3. 통합 테스트로 조합이 실제 사용자 행동으로 이어지는지 확인한다.
4. 재검증 기록으로 단일 백엔드 기준선을 닫는다.

## 마지막에 확인할 근거
- 코드: `capstone/workspace-backend/fastapi/app/api/v1/routes/platform.py::create_comment`
- 테스트/런타임: `capstone/workspace-backend/fastapi/tests/integration/test_capstone.py::test_local_auth_workspace_flow_and_google_member_notification`
- CLI: `python3 -m compileall app tests`, `make lint`, `make test`, `make smoke`, `./tools/compose_probe.sh capstone/workspace-backend/fastapi 8010`

## 이 글을 다 읽고 나면
- 통합 사용자 모델과 워크스페이스 경계가 어떤 타협으로 성립하는지 보게 된다.
- 댓글, 알림, 실시간 전달이 한 흐름으로 이어질 때 무엇이 중심 축이 되는지 이해하게 된다.
- 이 capstone이 왜 이후 MSA 비교의 기준선이 되는지 감이 잡힌다.
- 검증 기록: 2026-03-09에 compile, lint, test, smoke, Compose live/ready probe가 통과했고, 로컬 학습 실행을 위해 앱 시작 시 스키마 자동 초기화를 두었다.
- 다음으로 이어 볼 대상: H-service-boundary-lab
