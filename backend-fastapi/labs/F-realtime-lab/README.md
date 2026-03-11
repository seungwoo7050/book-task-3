# F-realtime-lab

실시간 알림과 연결 상태 관리를 최소 단위로 연습하는 랩입니다. WebSocket, presence, fan-out을 별도 주제로 다뤄서 실시간 기능을 다른 도메인 문제와 섞지 않고 이해하도록 돕습니다.

## 문제 요약

- 클라이언트와 서버가 장시간 연결을 유지하면서 presence와 알림을 주고받는다고 가정합니다. HTTP 요청만으로는 표현하기 어려운 연결 상태, heartbeat, fan-out을 별도 모델로 다뤄야 합니다.
- WebSocket 연결이 인증된 사용자와 연결되어야 합니다.
- presence heartbeat가 TTL 기반으로 갱신되어야 합니다.
- 상세 성공 기준과 제외 범위는 [problem/README.md](problem/README.md)에 둡니다.

## 내 답

- WebSocket 연결 인증
- presence 업데이트
- 알림 게시와 fan-out
- health endpoint

## 핵심 설계 선택

- WebSocket 인증
- presence heartbeat와 TTL
- 한 사용자에 대한 다중 소켓 fan-out
- 테스트와 로컬 로직은 인메모리 상태를 적극적으로 활용합니다.
- Redis는 확장 경계로 두되, 이 랩의 핵심은 연결 모델 설명에 둡니다.

## 검증

```bash
make lint
make test
make smoke
docker compose up --build
```

- 실행과 환경 설명은 [fastapi/README.md](fastapi/README.md)에서 다룹니다.
- 마지막 기록된 실제 검증 결과는 [../../docs/verification-report.md](../../docs/verification-report.md)에 있습니다.

## 제외 범위

- 완전한 broker 기반 수평 확장 구현
- 메시지 replay 보장
- 대규모 채팅 제품 수준의 방/채널 모델

## 다음 랩 또는 비교 대상

- 다음 단계는 [G-ops-lab](../G-ops-lab/README.md)입니다.
- 설계 설명은 [docs/README.md](docs/README.md), 학습 로그는 [notion/README.md](notion/README.md), 실행 진입점은 [fastapi/README.md](fastapi/README.md)에서 읽습니다.
