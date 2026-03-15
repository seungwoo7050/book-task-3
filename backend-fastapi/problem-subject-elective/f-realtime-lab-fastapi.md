# f-realtime-lab-fastapi 문제지

## 왜 중요한가

클라이언트와 서버가 장시간 연결을 유지하면서 presence와 알림을 주고받는다고 가정합니다. HTTP 요청만으로는 표현하기 어려운 연결 상태, heartbeat, fan-out을 별도 모델로 다뤄야 합니다.

## 목표

시작 위치의 구현을 완성해 WebSocket 연결이 인증된 사용자와 연결되어야 합니다, presence heartbeat가 TTL 기반으로 갱신되어야 합니다, 한 사용자에게 여러 활성 연결이 있어도 fan-out이 가능해야 합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../labs/F-realtime-lab/fastapi/app/__init__.py`
- `../labs/F-realtime-lab/fastapi/app/api/__init__.py`
- `../labs/F-realtime-lab/fastapi/app/api/deps.py`
- `../labs/F-realtime-lab/fastapi/app/api/v1/__init__.py`
- `../labs/F-realtime-lab/fastapi/tests/conftest.py`
- `../labs/F-realtime-lab/fastapi/tests/integration/test_realtime.py`
- `../labs/F-realtime-lab/fastapi/compose.yaml`
- `../labs/F-realtime-lab/fastapi/Makefile`

## starter code / 입력 계약

- `../labs/F-realtime-lab/fastapi/app/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- WebSocket 연결이 인증된 사용자와 연결되어야 합니다.
- presence heartbeat가 TTL 기반으로 갱신되어야 합니다.
- 한 사용자에게 여러 활성 연결이 있어도 fan-out이 가능해야 합니다.
- 재연결 보조용 HTTP surface가 있어야 합니다.

## 제외 범위

- 완전한 broker 기반 수평 확장 구현
- 메시지 replay 보장
- 대규모 채팅 제품 수준의 방/채널 모델

## 성공 체크리스트

- 핵심 흐름은 `get_connection_manager`와 `get_presence_tracker`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `client`와 `test_websocket_notification_delivery_and_presence`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../labs/F-realtime-lab/fastapi/compose.yaml` fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi && PYTHONPATH=. python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi && PYTHONPATH=. python3 -m pytest
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi test
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi && python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`f-realtime-lab-fastapi_answer.md`](f-realtime-lab-fastapi_answer.md)에서 확인한다.
