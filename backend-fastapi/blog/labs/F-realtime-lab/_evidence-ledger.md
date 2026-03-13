# F-realtime-lab Evidence Ledger

## 독립 프로젝트 판정
- 판정: 처리 대상
- 이유: README와 docs가 WebSocket 인증, TTL heartbeat, fan-out을 독립 문제로 설명하고, `tests/integration/test_realtime.py`가 연결 유지와 presence 만료를 직접 검증한다.
- 프로젝트 질문: presence와 알림을 다룰 때, WebSocket 연결 상태와 사용자 online 상태를 어떻게 구분할 것인가.
- 주의: finer-grained 구현 순서는 commit granularity가 거칠어서 README, docs, code surface, tests 의존 순서를 바탕으로 복원했다. 실제 날짜가 확인되는 부분은 git log와 검증 보고서에만 한정했다.

## 소스 인벤토리
- `labs/F-realtime-lab/README.md`
- `labs/F-realtime-lab/problem/README.md`
- `labs/F-realtime-lab/docs/README.md`
- `labs/F-realtime-lab/fastapi/README.md`
- `labs/F-realtime-lab/fastapi/Makefile`
- `labs/F-realtime-lab/fastapi/compose.yaml`
- `backend-fastapi/.github/workflows/labs-fastapi.yml`
- `backend-fastapi/docs/verification-report.md`
- `backend-fastapi/labs/F-realtime-lab/fastapi/app/api/v1/routes/realtime.py`
- `backend-fastapi/labs/F-realtime-lab/fastapi/tests/integration/test_realtime.py`
- `git log -- backend-fastapi/labs/F-realtime-lab`

## 프로젝트 표면 요약
- 문제 요약: 클라이언트와 서버가 장시간 연결을 유지하면서 presence와 알림을 주고받는다고 가정합니다. HTTP 요청만으로는 표현하기 어려운 연결 상태, heartbeat, fan-out을 별도 모델로 다뤄야 합니다. WebSocket 연결이 인증된 사용자와 연결되어야 합니다. presence heartbeat가 TTL 기반으로 갱신되어야 합니다. 상세 성공 기준과 제외 범위는 problem/README.md에 둡니다.
- 성공 기준: WebSocket 연결이 인증된 사용자와 연결되어야 합니다. presence heartbeat가 TTL 기반으로 갱신되어야 합니다. 한 사용자에게 여러 활성 연결이 있어도 fan-out이 가능해야 합니다. 재연결 보조용 HTTP surface가 있어야 합니다.
- 설계 질문: WebSocket 인증은 어디서 끝나야 하는가 presence는 왜 TTL과 heartbeat를 함께 써야 하는가 fan-out을 메모리에서 시작하고 Redis로 확장하는 경계는 어디인가
- 실제 검증 surface: make lint make test make smoke docker compose up --build 실행과 환경 설명은 fastapi/README.md에서 다룹니다. 마지막 기록된 실제 검증 결과는 ../../docs/verification-report.md에 있습니다.

## 시간 표지
- 2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료
- 2026-03-10 a3edce2 docs: enhance backend-fastapi
- 2026-03-09 7813150 docs(notion): front-react, backend-fastapi
- 2026-03-09 73372bd Add project: backend-fastapi, backend-spring, cpp-server

## Chronology Ledger
| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1, 2026-03-09 add project commit 73372bd를 기준으로 복원 | HTTP 요청 밖에 있는 연결 상태를 독립 문제로 분리 | README.md, problem/README.md, docs/README.md | 알림 전송 endpoint 하나만 추가하면 실시간 랩으로 충분할 것 | WebSocket 인증, presence heartbeat, 다중 연결 fan-out을 성공 기준에 포함 | README의 `make run`, `docker compose up --build` | 문제 정의가 연결 상태, heartbeat, fan-out을 별도 요구로 명시 | problem/README.md 성공 기준 | 실시간 전달은 메시지 내용보다 연결 상태 모델을 먼저 세워야 설명된다 | 연결/사용자 상태 경계 구현 |
| 2 | Phase 2, route/runtime 의존성으로 복원 | 연결 인증과 presence 갱신을 각각 다른 surface로 고정 | app/api/v1/routes/realtime.py, app/runtime.py, app/schemas/realtime.py | WebSocket만 있으면 presence도 자연스럽게 해결될 것 | notifications_ws에서 connect와 receive loop를 두고, 별도 heartbeat/presence HTTP endpoint를 둠 | `make test` | WebSocket connect 직후 tracker.heartbeat가 호출되고, 별도 `/presence` route가 존재 | app/api/v1/routes/realtime.py::notifications_ws | 연결 상태와 사용자 online 상태는 같은 값처럼 보여도 갱신 표면이 다르다 | invalid token, TTL expiry 검증 |
| 3 | Phase 3, 테스트가 presence semantics를 굳힘 | 잘못된 token disconnect와 heartbeat TTL 만료를 실제 요청으로 검증 | tests/integration/test_realtime.py | 알림 전달 성공만 확인해도 실시간 구조를 설명할 수 있을 것 | invalid token 접속 실패, heartbeat 후 1.1초 뒤 offline, websocket 수신 fan-out을 테스트화 | `make test` | 잘못된 token은 즉시 disconnect, TTL 경과 후 `online`이 False | tests/integration/test_realtime.py::test_invalid_token_disconnects_and_presence_expires | 실시간 시스템은 메시지 전달보다 연결이 끊겼을 때 상태가 어떻게 수렴하는지가 더 중요하다 | 재실행 surface와 health 확인 |
| 4 | 2026-03-09 재검증 + 2026-03-11 track polish | 실시간 실험도 독립 앱으로 다시 띄워 검증됐음을 닫기 | docs/verification-report.md, fastapi/README.md, tools/compose_probe.sh | 테스트만 있으면 WebSocket 랩의 독립성이 충분할 것 | compile, lint, test, smoke, Compose probe 결과 기록 | `python3 -m compileall app tests`, `make lint`, `make test`, `make smoke`, `./tools/compose_probe.sh labs/F-realtime-lab/fastapi 8004` | 2026-03-09 기준 compile/lint/test/smoke/Compose probe 통과 | docs/verification-report.md F-realtime-lab 항목 | WebSocket 랩도 마지막엔 HTTP health surface로 다시 닫혀야 관리 가능하다 | 운영성 surface로 이동 |
