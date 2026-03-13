# F-realtime-lab 시리즈 지도

이 시리즈는 WebSocket, presence, fan-out을 데이터 API와 분리된 연결 모델로 읽기 위해 실제 소스와 테스트를 다시 따라갑니다.

## 이 시리즈가 보는 문제

- 인증된 연결만 websocket에 붙을 수 있어야 합니다.
- presence는 마지막 요청 시각이 아니라 TTL 기반 heartbeat로 관리되어야 합니다.

## 실제 구현 표면

- `/api/v1/realtime/ws/notifications/{user_id}`
- `/api/v1/realtime/presence/heartbeat`
- `/api/v1/realtime/presence/{user_id}`
- 한 사용자에 대한 다중 socket fan-out

## 대표 검증 엔트리

- `pytest tests/integration/test_realtime.py -q`
- `make smoke`

## 읽는 순서

1. [프로젝트 README](../../../labs/F-realtime-lab/README.md)
2. [문제 정의](../../../labs/F-realtime-lab/problem/README.md)
3. [실행 진입점](../../../labs/F-realtime-lab/fastapi/README.md)
4. [대표 통합 테스트](../../../labs/F-realtime-lab/fastapi/tests/integration/test_realtime.py)
5. [핵심 구현](../../../labs/F-realtime-lab/fastapi/app/runtime.py)
6. [개발 타임라인](10-development-timeline.md)

## 근거 파일

- [README.md](../../../labs/F-realtime-lab/README.md)
- [problem/README.md](../../../labs/F-realtime-lab/problem/README.md)
- [fastapi/README.md](../../../labs/F-realtime-lab/fastapi/README.md)
- [tests/integration/test_realtime.py](../../../labs/F-realtime-lab/fastapi/tests/integration/test_realtime.py)
- [app/runtime.py](../../../labs/F-realtime-lab/fastapi/app/runtime.py)
- [docs/verification-report.md](../../../docs/verification-report.md)
