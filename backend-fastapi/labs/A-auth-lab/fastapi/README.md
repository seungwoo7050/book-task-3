# A-auth-lab FastAPI

## 이 구현이 다루는 범위

- 로컬 회원가입과 로그인
- 이메일 검증
- 비밀번호 재설정
- refresh token rotation
- cookie 기반 인증과 CSRF 보호
- `/api/v1/health/live`, `/api/v1/health/ready`

## 빠른 시작

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

## Compose 구성

- `api`: 호스트 `8000` 포트로 노출됩니다.
- `db`: PostgreSQL 16, 데이터베이스 이름은 `a_auth_lab`입니다.
- `redis`: Redis 7을 사용합니다.
- `mailpit`: 메일 UI를 `8025` 포트로 노출합니다.

## 이 워크스페이스에서 확인할 점

- `make run`은 기본 SQLite 설정으로도 바로 뜹니다.
- `.env.example`은 `db`, `redis`, `mailpit`을 가리키는 Compose 기준 값입니다.
- Compose는 메일 검증 실험을 위해 Mailpit까지 함께 띄웁니다.
- 로컬 인증에 집중하는 랩이므로 외부 로그인이나 2FA는 포함하지 않습니다.

## 함께 읽을 문서

- [상위 README](../README.md)
- [문제 정의](../problem/README.md)
- [문서 지도](../docs/README.md)
