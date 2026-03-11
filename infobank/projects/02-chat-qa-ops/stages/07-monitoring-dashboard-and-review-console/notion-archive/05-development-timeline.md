> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Monitoring Dashboard — 개발 타임라인

## 1단계: FastAPI 백엔드 프로젝트 생성

```bash
mkdir -p chat-qa-ops/07-monitoring-dashboard-and-review-console/python/{src/stage07,tests}
```

### pyproject.toml 작성

```bash
cat > chat-qa-ops/07-monitoring-dashboard-and-review-console/python/pyproject.toml << 'EOF'
[project]
name = "stage07-monitoring-dashboard"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["fastapi>=0.115", "uvicorn>=0.34"]

[tool.pytest.ini_options]
testpaths = ["tests"]
EOF
```

이전 stage들과 달리 외부 패키지가 필요하다:
- `fastapi`: API 서버
- `uvicorn`: ASGI 서버

```bash
cd chat-qa-ops/07-monitoring-dashboard-and-review-console/python
uv sync
```

## 2단계: SNAPSHOT dict + API 엔드포인트 작성

```bash
touch chat-qa-ops/07-monitoring-dashboard-and-review-console/python/src/stage07/__init__.py
# app.py 작성
```

SNAPSHOT dict를 먼저 완성하고, 각 엔드포인트는 SNAPSHOT의 해당 키를 반환하는 1줄 함수로 구현했다.
compare 데이터의 수치(84.06→87.76 등)는 stage 06의 golden set 결과 기반으로 산출된 값이다.

```bash
cd chat-qa-ops/07-monitoring-dashboard-and-review-console/python
uv run uvicorn stage07.app:app --reload --port 8000
# 별도 터미널에서 curl로 각 엔드포인트 확인
curl http://localhost:8000/api/dashboard/overview | python -m json.tool
```

## 3단계: API 테스트 작성

```bash
touch chat-qa-ops/07-monitoring-dashboard-and-review-console/python/tests/test_api.py
```

FastAPI의 TestClient를 사용하면 실제 서버를 띄우지 않고 테스트할 수 있다.
추가 의존성:

```bash
uv add --dev httpx  # TestClient 내부에서 필요
uv run pytest tests/ -x -v
```

## 4단계: React 프로젝트 생성

```bash
cd chat-qa-ops/07-monitoring-dashboard-and-review-console
pnpm create vite react --template react-ts
cd react
pnpm install
```

### 추가 패키지 설치

```bash
pnpm add react-router-dom
pnpm add -D @testing-library/react @testing-library/jest-dom @testing-library/user-event vitest jsdom
```

- `react-router-dom`: 클라이언트 사이드 라우팅
- `@testing-library/*`: 컴포넌트 테스트
- `vitest`: Vite 네이티브 테스트 러너

### Vite 설정

```bash
# vite.config.ts에 proxy 설정 추가
# vitest.config.ts 생성
```

## 5단계: API 클라이언트 작성

```bash
mkdir -p react/src/api
touch react/src/api/client.ts
```

fetch를 감싼 `apiGet()`, `apiPost()` 헬퍼를 만들었다.
에러 처리는 throw 방식으로 하고, 호출하는 쪽에서 try/catch로 처리한다.

## 6단계: 페이지 컴포넌트 구현

순서: Overview → Failures → SessionReview → EvalRunner

```bash
mkdir -p react/src/{pages,components,i18n}
```

각 페이지에서 useEffect로 API를 호출하고, useState로 데이터를 관리한다.

### Overview.tsx 구현 시 주의점

version compare 섹션은 overview API와 version-compare API 두 개를 호출해야 한다.
두 API 호출을 separate useEffect로 분리했다.

## 7단계: 컴포넌트 테스트

```bash
pnpm run test
# 또는
pnpm exec vitest run
```

각 페이지마다 `*.test.tsx` 파일을 만들어서:
1. API 클라이언트를 모킹
2. SNAPSHOT 데이터를 반환하도록 설정
3. 렌더링 후 기대하는 텍스트/요소가 화면에 있는지 확인

## 비고

- 이 stage는 Python(backend)과 React/TypeScript(frontend) 두 개의 프로젝트로 구성된다.
- 두 프로젝트의 패키지 관리자가 다르다: uv(Python) vs pnpm(React).
- capstone에서는 Docker Compose로 두 서비스를 함께 배포한다.
