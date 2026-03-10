# 개발 타임라인

## 이 문서의 목적

- 처음 체크아웃한 사람이 어떤 순서로 실행하면 현재 상태를 다시 확인할 수 있는지 적습니다.
- 빠른 자동 검증 경로와 전체 의존성을 올리는 경로를 분리해서 적습니다.

## 1. 시작 위치를 고정한다

```bash
cd <repo-or-project-path>
python3 -m venv .venv
source .venv/bin/activate
make install
```

- 로컬 기본 설정만으로 실행 가능한지, `.env.example`이 Compose 전용 값인지 먼저 적습니다.
- `make run`을 바로 써도 되는지, 아니면 `.env`를 만들기 전에 주의할 점이 있는지 적습니다.

## 2. 가장 빠른 자동 재현 경로

```bash
pytest <가장 대표적인 integration test 파일> -q
make smoke
```

- 어떤 시나리오를 이 테스트가 끝까지 증명하는지 적습니다.
- `make smoke`가 정확히 무엇만 확인하는지도 적습니다.

## 3. 로컬 편집 루프를 연다

```bash
make run
```

다른 터미널에서:

```bash
curl http://127.0.0.1:<local-port>/api/v1/health/live
curl http://127.0.0.1:<local-port>/api/v1/health/ready
```

- 이 경로가 빠른 이유와, 반대로 여기서는 보이지 않는 의존성이 무엇인지 적습니다.

## 4. Compose나 외부 의존성까지 포함한 경로를 적는다

```bash
cp .env.example .env
docker compose up --build -d
docker compose ps
curl http://127.0.0.1:<compose-port>/api/v1/health/live
```

- 어떤 서비스가 떠야 하는지, 어떤 포트가 열리는지, 종료 명령이 무엇인지 적습니다.
- 외부 provider나 worker가 있으면 이 단계에서만 보이는 차이를 적습니다.

## 5. 핵심 기능을 수동으로 재현한다

- 가장 중요한 API 또는 흐름을 실제 요청 순서대로 적습니다.
- 동적 값이 있으면 `<TOKEN>`, `<USER_ID>` 같은 자리표시자를 쓰고, 그 값을 어디서 얻는지 바로 위에 적습니다.
- 외부 provider 때문에 완전 수동 재현이 어렵다면 그 사실을 숨기지 말고, 어떤 테스트가 기준 재현 경로인지 적습니다.

## 6. 막히면 먼저 확인할 것을 적는다

- 가장 자주 어긋나는 헤더, 쿠키, 토큰, 환경 변수, worker 상태를 적습니다.
- 실패했을 때 어느 테스트 파일이나 로그를 먼저 보면 좋은지도 적습니다.
