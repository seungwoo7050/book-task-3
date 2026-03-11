# Chat QA Ops v3 self-hosted OSS 스냅샷

`v3-self-hosted-oss`는 `v2-submission-polish`를 단일 팀용 self-hosted QA Ops OSS 스냅샷으로 확장한 버전이다. 목표는 새 평가 축을 더 붙이는 것이 아니라, 한 팀이 직접 설치하고 로그인해서 dataset import, KB import, evaluation job, dashboard review를 운영할 수 있게 만드는 것이다.

## 이 버전에서 할 수 있는 것

- 관리자 로그인 후 상담 transcript JSONL을 업로드할 수 있다.
- Markdown ZIP 기반 KB bundle을 업로드할 수 있다.
- dataset + KB bundle 조합으로 비동기 evaluation job을 생성할 수 있다.
- 선택한 job/run 기준으로 overview, failures, session review를 볼 수 있다.
- baseline/candidate run label 비교로 배포 승인 판단 근거를 만들 수 있다.

## 권장 읽기 순서

1. 상위 [`../README.md`](../README.md)
2. [`../docs/release-readiness.md`](../docs/release-readiness.md)
3. 이 문서
4. 필요하면 `python/`, `react/`, `docs/`로 내려가 세부 구현을 본다

## 빠른 시작

가장 단순한 경로는 Docker Compose다.

```bash
cd projects/02-chat-qa-ops/capstone/v3-self-hosted-oss
docker compose up --build
```

기본 접속:

- Web: `http://localhost:5173`
- API: `http://localhost:8000`
- Admin email: `admin@example.com`
- Admin password: `password123`

Compose 기본 모드는 외부 API key 없이 동작한다.

- evaluator mode: heuristic
- retrieval backend: keyword
- database: PostgreSQL
- optional profile: `ai` (`ollama`, `chroma`)

AI profile이 필요하면 다음 명령을 사용한다.

```bash
docker compose --profile ai up --build
```

## 로컬 검증

백엔드:

```bash
cd python
UV_PYTHON=python3.12 uv sync --extra dev
UV_PYTHON=python3.12 make gate-all
```

프론트엔드:

```bash
cd react
pnpm install
pnpm test --run
```

## 포트폴리오 관점 메모

- `v0~v2`는 보존용 데모와 proof 역할을 유지하고, `v3`는 self-hosted 사용 권장 버전이다.
- 학생 입장에서는 "제출용 데모"와 "설치 가능한 OSS snapshot"을 분리하는 README 전략을 참고하면 좋다.
- 더 자세한 판단 과정과 회고는 stage별 `notion/`과 capstone `notion/`에서 볼 수 있다.

## 범위 밖

- single admin auth 외 추가 권한 체계
- transcript 생성 자체
- multi-tenant, RBAC, SSO, billing, Redis/Celery, Kubernetes
