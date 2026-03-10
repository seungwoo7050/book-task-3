# 저장소 기준 문서

## 문서 구조

각 lab과 capstone은 아래 공개 구조를 유지합니다.

```text
README.md
problem/
fastapi/
docs/
notion/
notion-archive/   # 이전 노트를 보관할 때만 존재
```

각 `fastapi/` 워크스페이스는 아래 항목을 기준으로 설명합니다.

```text
app/
tests/
alembic/
pyproject.toml
.env.example
Dockerfile
compose.yaml
Makefile
README.md
```

## MSA 예외 규칙

- 기본 공개 구조 `README / problem / fastapi / docs / notion`는 유지합니다.
- 다만 MSA 프로젝트의 `fastapi/`는 단일 앱이 아니라 오케스트레이션 루트로 설명할 수 있습니다.
- MSA 프로젝트의 `fastapi/` 아래에는 최소한 `gateway/`, `services/<service-name>/`, `contracts/`, `scripts/`, `compose.yaml`, `Makefile`, `.env.example`, `README.md`를 둡니다.
- 각 서비스 디렉터리는 자체 `app/`, `tests/`, `alembic/`, `pyproject.toml`, `Dockerfile`, `README.md`를 가집니다.
- 비교 학습을 위해 v1과 v2 사이에 공용 패키지를 새로 만들지 않습니다.
- 문서에는 서비스 경계, 데이터 ownership, 이벤트 계약, request id 전파 규칙을 먼저 적습니다.

## 런타임 공통 규칙

- HTTP 라우트는 `/api/v1` 아래에 마운트합니다.
- health endpoint는 `/health/live`, `/health/ready`를 기준으로 설명합니다.
- 에러 응답은 문서에서 일관된 envelope가 있다는 점을 분명히 적습니다.
- OpenAPI는 코드에서 생성되는 것을 전제로 설명합니다.
- 로그는 기계가 읽기 쉬운 구조화 로그를 지향합니다.

## 실행과 검증 문서 규칙

- 각 워크스페이스는 최소한 `make install`, `make run`, `make lint`, `make test`, `make smoke`, `docker compose up --build`를 문서에 포함합니다.
- MSA 오케스트레이션 루트의 `make install`, `make lint`, `make test`, `make smoke`는 내부 서비스와 시스템 검증을 함께 호출해도 됩니다.
- 문서에 적는 명령은 실제 `Makefile`, `.env.example`, `compose.yaml`에 근거해야 합니다.
- 새 검증을 다시 돌리지 않았다면, 이전 검증 결과를 최신 결과처럼 쓰지 않습니다.
- 검증 보고서는 "확인된 사실"과 "아직 문서 수준인 가정"을 분리해서 적습니다.

## 공개 문서 톤

- 한글 우선으로 작성하고, 필요한 기술 용어만 영어를 병기합니다.
- 독자를 초중급 학습자로 가정합니다.
- 기능 나열보다 "왜 이 랩이 분리되어 있는지", "어디까지 단순화했는지", "포트폴리오로 어떻게 확장할 수 있는지"를 먼저 설명합니다.
- 학습용 저장소라는 이유로 설명을 생략하지 않습니다. 다만 운영 준비가 끝난 제품처럼 과장해서도 안 됩니다.

## 노트 정책

- `notion/`은 현재 공개용 학습 노트 세트입니다.
- `notion-archive/`는 이전 버전 노트의 백업 보관소입니다.
- 새 노트를 다시 작성할 때는 기존 노트를 삭제하지 말고 `notion-archive/`로 옮긴 뒤 새 `notion/`을 만듭니다.
- 각 `notion/`은 아래 여섯 파일을 기본 세트로 유지합니다.

```text
00-problem-framing.md
01-approach-log.md
02-debug-log.md
03-retrospective.md
04-knowledge-index.md
05-development-timeline.md
README.md
```

## 저장소 정리 규칙

- `.env`, 로컬 DB, 캐시, `*.egg-info/` 같은 개발 산출물은 추적하지 않습니다.
- workflow와 문서는 현재 존재하는 경로만 가리켜야 합니다.
- 복붙으로 생긴 잘못된 프로젝트 이름, 오래된 절대 경로, 존재하지 않는 트랙 설명은 남겨두지 않습니다.

## 공개 가능 상태의 기준

- 루트 README와 각 랩 README만 읽어도 학습 목표와 실행 경로를 이해할 수 있어야 합니다.
- `problem/`, `fastapi/`, `docs/`, `notion/`의 역할이 문서에서 분명해야 합니다.
- 검증 보고서가 마지막 실제 실행 시점을 숨기지 않아야 합니다.
- 학생이 이 레포를 참고해 자기만의 구조를 설계할 수 있을 정도로 의도와 한계가 설명되어 있어야 합니다.
