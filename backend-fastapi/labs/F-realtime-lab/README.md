# F-realtime-lab

실시간 알림과 연결 상태 관리를 최소 단위로 연습하는 랩입니다. WebSocket, presence, fan-out을 별도 주제로 다뤄서 실시간 기능을 다른 도메인 문제와 섞지 않고 이해하도록 돕습니다.

## 이 랩에서 배우는 것

- WebSocket 인증
- presence heartbeat와 TTL
- 한 사용자에 대한 다중 소켓 fan-out
- 재연결을 고려한 HTTP 보조 surface

## 선수 지식

- HTTP와 WebSocket의 차이
- 비동기 I/O 기본
- Redis pub/sub이 어떤 문제를 푸는지에 대한 감각

## 구현 범위

- WebSocket 연결 인증
- presence 업데이트
- 알림 게시와 fan-out
- health endpoint

## 일부러 단순화한 점

- 테스트와 로컬 로직은 인메모리 상태를 적극적으로 활용합니다.
- Redis는 확장 경계로 두되, 이 랩의 핵심은 연결 모델 설명에 둡니다.

## 실행 방법

1. [problem/README.md](problem/README.md)에서 실시간 범위를 확인합니다.
2. [fastapi/README.md](fastapi/README.md)로 API와 Redis 구성을 실행합니다.
3. [docs/README.md](docs/README.md)와 [notion/README.md](notion/README.md)로 connection model을 정리합니다.

## 검증 방법

- `cd fastapi && make lint`
- `cd fastapi && make test`
- `cd fastapi && make smoke`
- `cd fastapi && docker compose up --build`

## 추천 학습 순서

1. 어떤 상태를 메모리에 두고 어떤 상태를 외부 저장소로 보낼지 구분합니다.
2. fan-out과 reconnect 요구를 함께 봅니다.
3. 확장 시 Redis나 broker가 어디에 들어갈지 도식으로 정리합니다.

## 포트폴리오로 확장하려면

- presence를 workspace나 room 단위로 세분화할 수 있습니다.
- delivery ack, unread state, reconnect replay까지 확장할 수 있습니다.
- README에는 "실시간 기능이 왜 별도 랩으로 분리되었는가"를 짧게 설명하는 것이 좋습니다.
