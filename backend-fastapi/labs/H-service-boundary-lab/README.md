# H-service-boundary-lab

서비스를 어디서 나누고 무엇을 공유하지 말아야 하는지 배우는 MSA 입문 랩입니다. `identity-service`와 `workspace-service`를 분리하고, bearer claims로만 사용자 정보를 전달하면서 서비스별 DB ownership을 설명하는 데 집중합니다.

## 문제 요약

- 단일 백엔드에서 자연스럽게 함께 있던 인증과 워크스페이스 도메인을 처음으로 분리한다. 핵심 질문은 "어디서 경계를 끊어야 하며, 서비스가 서로의 DB를 읽지 않고도 동작할 수 있는가"이다.
- `identity-service`가 토큰을 발급한다.
- `workspace-service`가 그 토큰 claims만으로 workspace를 생성한다.
- 상세 성공 기준과 제외 범위는 [problem/README.md](problem/README.md)에 둡니다.

## 내 답

- 내부 인증 API
- bearer token으로 workspace 생성
- 서비스별 health endpoint

## 핵심 설계 선택

- `identity-service`와 `workspace-service` 분리 기준
- 서비스별 DB ownership
- bearer claims 기반 사용자 전달
- 이벤트 브로커와 gateway는 아직 넣지 않습니다.
- 로컬 런타임은 SQLite 두 개로 제한합니다.

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

- 이벤트 브로커
- edge gateway
- websocket과 실시간 전달

## 다음 랩 또는 비교 대상

- 다음 단계는 [I-event-integration-lab](../I-event-integration-lab/README.md)입니다.
- 설계 설명은 [docs/README.md](docs/README.md), 학습 로그는 [notion/README.md](notion/README.md), 실행 진입점은 [fastapi/README.md](fastapi/README.md)에서 읽습니다.
