# B-federation-security-lab FastAPI

이 문서는 B-federation-security-lab의 실행과 검증 진입점입니다. 문제 정의나 설계 해설보다 먼저 손을 움직여 보고 싶을 때 여기서 시작합니다.

## 이 워크스페이스가 제공하는 답

- Google OIDC 로그인
- 외부 계정 연결
- TOTP 2FA
- recovery code
- auth audit log
- `/api/v1/health/live`, `/api/v1/health/ready`

## 빠른 실행

가장 빠른 로컬 확인:

```bash
python3 -m venv .venv
source .venv/bin/activate
make install
make run
```

Compose 전체 확인:

```bash
cp .env.example .env
docker compose up --build
```

## 검증 명령

```bash
make lint
make test
make smoke
docker compose up --build
```

## 런타임 구성

- `api`: 호스트 `8000` 포트로 노출됩니다.
- `db`: PostgreSQL 16, 데이터베이스 이름은 `b_federation_security_lab`입니다.
- `redis`: Redis 7을 사용합니다.

## 실행 전에 알아둘 점

- `make run`과 Compose의 `api` 명령 모두 `alembic upgrade head`를 먼저 실행합니다.
- `make run`은 기본 SQLite 설정으로도 시작할 수 있습니다.
- `.env.example`은 PostgreSQL, Redis, 실제 Google OIDC 설정을 담은 Compose 기준 값입니다.
- 외부 공급자 동작은 로컬 학습용 흐름과 테스트 더블을 기준으로 정리되어 있습니다.

## 역할이 다른 관련 문서

- 문제 요약과 답안 인덱스: [상위 README](../README.md)
- canonical problem statement: [problem/README.md](../problem/README.md)
- 설계 설명: [docs/README.md](../docs/README.md)
- 학습 로그: [notion/README.md](../notion/README.md)
