# A-auth-lab Spring 워크스페이스

- 상태: `verified scaffold`
- 현재 범위: 로컬 계정 인증 surface, token rotation 모델링, Mailpit-ready 로컬 워크플로

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

- auth persistence는 초기 scaffold 수준으로 가볍게 두었다
- 이메일 검증과 비밀번호 재설정은 frontend 없는 API-first 모델링에 집중한다
