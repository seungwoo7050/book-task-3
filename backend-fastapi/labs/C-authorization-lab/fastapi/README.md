# C-authorization-lab FastAPI

이 문서는 C-authorization-lab의 실행과 검증 진입점입니다. 문제 정의나 설계 해설보다 먼저 손을 움직여 보고 싶을 때 여기서 시작합니다.

## 이 워크스페이스가 제공하는 답

- 워크스페이스 생성
- 초대 발행과 응답
- 역할 변경
- 소유권 기반 접근 제어
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

- `api`: 호스트 `8001` 포트로 노출됩니다.
- `db`: PostgreSQL 16, 데이터베이스 이름은 `c_authorization_lab`입니다.

## 실행 전에 알아둘 점

- `make run`은 기본 SQLite 설정으로도 바로 뜹니다.
- `.env.example`은 PostgreSQL이 있는 Compose 경로용 값입니다.
- Compose는 인가 규칙 실험에 필요한 최소 구성으로 API와 DB만 띄웁니다.
- 인증은 이 랩의 핵심이 아니므로 별도 헤더 기반 단순 경로를 전제합니다.

## 역할이 다른 관련 문서

- 문제 요약과 답안 인덱스: [상위 README](../README.md)
- canonical problem statement: [problem/README.md](../problem/README.md)
- 설계 설명: [docs/README.md](../docs/README.md)
- 학습 로그: [notion/README.md](../notion/README.md)
