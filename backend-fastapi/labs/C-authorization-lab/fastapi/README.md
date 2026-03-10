# C-authorization-lab FastAPI

## 이 구현이 다루는 범위

- 워크스페이스 생성
- 초대 발행과 응답
- 역할 변경
- 소유권 기반 접근 제어
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

- `api`: 호스트 `8001` 포트로 노출됩니다.
- `db`: PostgreSQL 16, 데이터베이스 이름은 `c_authorization_lab`입니다.

## 이 워크스페이스에서 확인할 점

- `make run`은 기본 SQLite 설정으로도 바로 뜹니다.
- `.env.example`은 PostgreSQL이 있는 Compose 경로용 값입니다.
- Compose는 인가 규칙 실험에 필요한 최소 구성으로 API와 DB만 띄웁니다.
- 인증은 이 랩의 핵심이 아니므로 별도 헤더 기반 단순 경로를 전제합니다.

## 함께 읽을 문서

- [상위 README](../README.md)
- [문제 정의](../problem/README.md)
- [문서 지도](../docs/README.md)
