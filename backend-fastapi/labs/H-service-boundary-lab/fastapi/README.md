# H-service-boundary-lab FastAPI

이 문서는 H-service-boundary-lab의 실행과 검증 진입점입니다. 문제 정의나 설계 해설보다 먼저 손을 움직여 보고 싶을 때 여기서 시작합니다.

## 이 워크스페이스가 제공하는 답

- `identity-service`에서 토큰 발급
- `workspace-service`에서 bearer claims만으로 workspace 생성
- 서비스별 `/api/v1/health/live`, `/api/v1/health/ready`

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

- `workspace-service`: 호스트 `8011`
- `identity-service`: 호스트 `8111`

## 실행 전에 알아둘 점


## 역할이 다른 관련 문서

- 문제 요약과 답안 인덱스: [상위 README](../README.md)
- canonical problem statement: [problem/README.md](../problem/README.md)
- 설계 설명: [docs/README.md](../docs/README.md)
- 학습 로그: [notion/README.md](../notion/README.md)
