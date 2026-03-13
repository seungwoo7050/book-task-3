# workspace-backend Structure Plan

## 한 줄 약속
- 분리해서 배운 경계들을 하나의 협업형 백엔드 안에서 다시 조합하기

## 독자 질문
- 인증, 인가, 데이터 API, 알림, 실시간 전달을 하나의 제품형 구조로 합칠 때 무엇을 다시 설계해야 하는가.
- 인증, 인가, 데이터 API, 알림 전달이 어디서 만나고 어디서 분리되는가 랩 코드를 재사용하지 않고 다시 구현한 이유는 무엇인가 협업형 도메인에서 큐와 실시간 전달을 어떤 순서로 결합했는가

## 서술 원칙
- 기존 `blog/` 초안은 입력 근거로 사용하지 않는다.
- 사실로 확인되는 날짜와 명령은 `git log`와 `docs/verification-report.md`에서만 가져온다.
- finer-grained chronology는 코드/테스트 의존 순서를 바탕으로 복원했다고 명시한다.

## 글 흐름
1. 랩의 답을 제품 도메인으로 다시 묶기
2. platform route에 협업 흐름을 한데 모으기
3. 통합 테스트로 조합이 실제로 이어지는지 확인하기
4. 2026-03-09 재검증으로 단일 백엔드 기준선을 닫기
5. 남은 범위와 다음 비교 대상 정리

## Evidence Anchor
- 주 코드 앵커: `capstone/workspace-backend/fastapi/app/api/v1/routes/platform.py::create_comment` — 댓글 생성이 알림과 실시간 전달 흐름으로 이어지는 통합 지점이다.
- 보조 앵커: `capstone/workspace-backend/fastapi/tests/integration/test_capstone.py::test_local_auth_workspace_flow_and_google_member_notification` — 소유자 로컬 로그인과 협업자 Google 로그인, 초대, websocket 알림을 한 번에 통과시킨다.
- 문서 앵커: `capstone/workspace-backend/problem/README.md`, `capstone/workspace-backend/docs/README.md`
- CLI 앵커:
- `python3 -m compileall app tests`
- `make lint`
- `make test`
- `make smoke`
- `./tools/compose_probe.sh <workspace> <host-port>`

## 글에서 강조할 개념
- 통합 사용자 모델과 워크스페이스 경계 댓글/알림/실시간 전달의 연결 구조 capstone이 랩들의 단순 합이 아닌 이유
- 인증과 인가를 제품형 워크스페이스 도메인에 묶는 방법 프로젝트, 태스크, 댓글을 중심으로 한 협업 API 구조 queued notification과 realtime delivery의 결합 랩 코드를 공용 패키지로 묶지 않고 다시 구현합니다. 프런트엔드, 정적 자산, 실제 클라우드 인프라는 제외합니다.

## 끝맺음
- 제외 범위: 프런트엔드 렌더링과 정적 자산 제공 실제 클라우드 배포 자동화 랩 코드를 공용 패키지로 묶는 리팩터링
- 검증 문장: 2026-03-09에 compile, lint, test, smoke, Compose live/ready probe가 통과했고, 로컬 학습 실행을 위해 앱 시작 시 스키마 자동 초기화를 두었다.
