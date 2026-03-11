# J-edge-gateway-lab FastAPI

이 문서는 J-edge-gateway-lab의 실행과 검증 진입점입니다. 문제 정의나 설계 해설보다 먼저 손을 움직여 보고 싶을 때 여기서 시작합니다.

## 이 워크스페이스가 제공하는 답

- gateway public auth / platform route
- request id propagation
- cookie + CSRF를 gateway에만 두는 edge 구조
- 내부 서비스 fan-out과 websocket edge

## 빠른 실행

```bash
cp .env.example .env
docker compose up --build
```

## 검증 명령

```bash
make install
make lint
make test
make smoke
docker compose up --build
```

## 런타임 구성

- `gateway`: 호스트 `8013` 포트로 public API와 websocket edge를 노출합니다.
- `identity-service`: 호스트 `8121` 포트로 내부 인증 API를 노출합니다.
- `workspace-service`: 호스트 `8122` 포트로 내부 워크스페이스 API를 노출합니다.
- `notification-service`: 호스트 `8123` 포트로 알림 API를 노출합니다.
- `redis`: `6393` 포트로 pub/sub와 내부 통합 경로를 제공합니다.

## 실행 전에 알아둘 점

- 브라우저 쿠키와 CSRF는 gateway에만 남기고 내부 서비스는 bearer token만 읽습니다.
- gateway는 public route shape를 유지한 채 내부 `identity-service`, `workspace-service`, `notification-service`로 fan-out 합니다.
- request id는 gateway에서 생성해 내부 호출 전체로 전달합니다.
- 이 워크스페이스의 초점은 기능 추가보다 edge 책임 재배치입니다.

## 역할이 다른 관련 문서

- 문제 요약과 답안 인덱스: [상위 README](../README.md)
- canonical problem statement: [problem/README.md](../problem/README.md)
- 설계 설명: [docs/README.md](../docs/README.md)
- 학습 로그: [notion/README.md](../notion/README.md)
