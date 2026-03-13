# F-realtime-lab Structure Plan

## 한 줄 약속
- HTTP로는 표현되지 않는 연결 상태를 별도 모델로 만들기

## 독자 질문
- presence와 알림을 다룰 때, WebSocket 연결 상태와 사용자 online 상태를 어떻게 구분할 것인가.
- WebSocket 인증은 어디서 끝나야 하는가 presence는 왜 TTL과 heartbeat를 함께 써야 하는가 fan-out을 메모리에서 시작하고 Redis로 확장하는 경계는 어디인가

## 서술 원칙
- 기존 `blog/` 초안은 입력 근거로 사용하지 않는다.
- 사실로 확인되는 날짜와 명령은 `git log`와 `docs/verification-report.md`에서만 가져온다.
- finer-grained chronology는 코드/테스트 의존 순서를 바탕으로 복원했다고 명시한다.

## 글 흐름
1. 실시간 전달을 별도 상태 모델로 정의하기
2. WebSocket connect와 heartbeat를 분리된 surface로 두기
3. presence 만료와 잘못된 token을 테스트로 고정하기
4. 2026-03-09 재검증으로 health/probe surface를 닫기
5. 남은 범위와 다음 비교 대상 정리

## Evidence Anchor
- 주 코드 앵커: `labs/F-realtime-lab/fastapi/app/api/v1/routes/realtime.py::notifications_ws` — 연결 인증, presence 갱신, 수신 loop가 한 함수 안에서 만난다.
- 보조 앵커: `labs/F-realtime-lab/fastapi/tests/integration/test_realtime.py::test_invalid_token_disconnects_and_presence_expires` — 잘못된 token disconnect와 TTL 만료를 실제로 보여 준다.
- 문서 앵커: `labs/F-realtime-lab/problem/README.md`, `labs/F-realtime-lab/docs/README.md`
- CLI 앵커:
- `python3 -m compileall app tests`
- `make lint`
- `make test`
- `make smoke`
- `./tools/compose_probe.sh <workspace> <host-port>`

## 글에서 강조할 개념
- 연결 상태와 사용자 상태의 차이 다중 연결 fan-out 모델 reconnect를 고려한 보조 HTTP surface의 역할
- WebSocket 인증 presence heartbeat와 TTL 한 사용자에 대한 다중 소켓 fan-out 테스트와 로컬 로직은 인메모리 상태를 적극적으로 활용합니다. Redis는 확장 경계로 두되, 이 랩의 핵심은 연결 모델 설명에 둡니다.

## 끝맺음
- 제외 범위: 완전한 broker 기반 수평 확장 구현 메시지 replay 보장 대규모 채팅 제품 수준의 방/채널 모델
- 검증 문장: 2026-03-09에 compile, lint, test, smoke, Compose live/ready probe가 모두 통과했다.
