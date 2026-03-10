# H-service-boundary-lab

서비스를 어디서 나누고 무엇을 공유하지 말아야 하는지 배우는 MSA 입문 랩입니다. `identity-service`와 `workspace-service`를 분리하고, bearer claims로만 사용자 정보를 전달하면서 서비스별 DB ownership을 설명하는 데 집중합니다.

## 이 랩에서 배우는 것

- `identity-service`와 `workspace-service` 분리 기준
- 서비스별 DB ownership
- bearer claims 기반 사용자 전달
- 공유 ORM 모델을 만들지 않는 이유

## 선수 지식

- [capstone/workspace-backend](../capstone/workspace-backend/README.md) 수준의 인증과 워크스페이스 흐름
- JWT와 FastAPI dependency 기본

## 구현 범위

- 내부 인증 API
- bearer token으로 workspace 생성
- 서비스별 health endpoint

## 일부러 단순화한 점

- 이벤트 브로커와 gateway는 아직 넣지 않습니다.
- 로컬 런타임은 SQLite 두 개로 제한합니다.

## 실행 방법

1. [problem/README.md](problem/README.md)로 서비스 분해 이유를 읽습니다.
2. [fastapi/README.md](fastapi/README.md)에서 두 서비스를 함께 실행합니다.
3. [docs/README.md](docs/README.md)와 [notion/README.md](notion/README.md)로 경계 선택 이유를 정리합니다.

## 검증 방법

- `cd fastapi && make lint`
- `cd fastapi && make test`
- `cd fastapi && make smoke`
- `cd fastapi && docker compose up --build`

## 추천 학습 순서

1. 먼저 어떤 테이블을 어느 서비스가 소유하는지 적습니다.
2. 그다음 토큰 claims만으로 workspace를 만들 수 있는지 확인합니다.
3. 마지막으로 왜 cross-DB 조회를 막았는지 설명합니다.

## 포트폴리오로 확장하려면

- 사용자 프로필 snapshot이나 조직 도메인 검증을 붙여 볼 수 있습니다.
- 서비스 간 스키마 공유를 피하는 대안을 문서화하면 설명력이 좋아집니다.
