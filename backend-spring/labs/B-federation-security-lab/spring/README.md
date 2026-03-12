# B-federation-security-lab Spring 워크스페이스

- 상태: `verified scaffold`
- 현재 범위: Google OAuth2 callback 모델링, 2FA 흐름, audit log surface

## 실행과 검증 명령

```bash
cp .env.example .env
make run
make lint
make test
make smoke
docker compose up --build
```

## 현재 한계

- Google integration은 실제 provider가 아니라 simulated contract다
- TOTP 생성은 학습 가독성을 위한 단순화 버전이다
