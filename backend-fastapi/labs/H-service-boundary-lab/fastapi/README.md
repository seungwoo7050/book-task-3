# H-service-boundary-lab FastAPI

## 이 구현이 다루는 범위

- `identity-service`에서 토큰 발급
- `workspace-service`에서 bearer claims만으로 workspace 생성
- 서비스별 `/api/v1/health/live`, `/api/v1/health/ready`

## 빠른 시작

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

## Compose 구성

- `workspace-service`: 호스트 `8011`
- `identity-service`: 호스트 `8111`

## 함께 읽을 문서

- [상위 README](../README.md)
- [문제 정의](../problem/README.md)
- [문서 지도](../docs/README.md)
