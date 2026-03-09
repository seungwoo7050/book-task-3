# GitHub Actions 완전 가이드

GitHub Actions는 GitHub 저장소에 내장된 CI/CD 파이프라인이다. 코드 푸시, PR, 스케줄 등 이벤트에 반응하여 빌드, 테스트, 배포를 자동으로 실행한다. YAML 파일 하나로 워크플로를 정의하고, GitHub이 제공하는 러너에서 실행된다. 이 글을 읽고 나면 워크플로를 작성하고, 테스트 자동화와 배포 파이프라인을 구성할 수 있다.

먼저 아래 세 질문을 기준으로 읽으면 워크플로 파일이 훨씬 빨리 정리된다.

1. **트리거:** 이 워크플로는 어떤 이벤트에서, 어떤 브랜치/경로 조건으로 실행되는가?
2. **잡 구조:** 이 잡들은 병렬인가 순차인가, 어떤 서비스 컨테이너가 필요한가?
3. **시크릿:** 이 파이프라인에서 노출되면 안 되는 값은 어디에 저장하고 어떻게 주입하는가?

---

## 1. GitHub Actions의 사고방식

GitHub Actions는 "스크립트를 실행하는 서버"가 아니라, "이벤트 → 잡 → 스텝 의 선언적 파이프라인"이다.

![GitHub Actions 이벤트와 워크플로 기본 구조](./images/github-actions-mental-model.svg)

이 그림은 이 문서 전체를 읽는 기준표다. 먼저 아래 세 질문으로 읽으면 된다.

1. **트리거:** 어떤 이벤트가 이 워크플로를 깨우고, 브랜치/경로 조건이 실행 범위를 어떻게 줄이는가?
2. **잡 구조:** 잡들이 서로 독립적으로 병렬 실행되는가, 아니면 `needs`로 순서를 강제하는가?
3. **상태 전달:** 캐시, 아티팩트, 시크릿 중 무엇이 어느 스코프에서 공유되는가?

그림을 위에서 아래로 읽으면 GitHub Actions는 "YAML 한 번 실행"이 아니라 이벤트에 반응해 러너 위에서 job graph를 만드는 시스템이라는 점이 드러난다. 따라서 Actions는 `트리거`, `job dependency`, `상태 전달 방식` 세 축으로 읽는 편이 가장 빠르다.

**핵심 용어:**

| 용어 | 의미 |
|------|------|
| **Workflow** | 하나의 YAML 파일. 이벤트에 반응하는 자동화 단위 |
| **Job** | 같은 러너에서 실행되는 스텝 묶음. 잡 간에는 파일 시스템을 공유하지 않음 |
| **Step** | 잡 안의 개별 명령. 순서대로 실행 |
| **Action** | 재사용 가능한 스텝 단위 (`actions/checkout`, `actions/setup-java` 등) |
| **Runner** | 워크플로를 실행하는 서버 (GitHub 호스팅 또는 자체 호스팅) |
| **Secret** | 암호화된 환경 변수 (저장소 Settings에서 관리) |

---

## 2. 프로젝트 구조

```
.github/
└── workflows/
    ├── ci.yml            # PR/push 시 빌드+테스트
    ├── deploy.yml        # main 머지 시 배포
    └── scheduled.yml     # 정기 작업
```

---

## 3. 기본 워크플로

### Python (FastAPI) CI

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        ports: ["5432:5432"]
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7-alpine
        ports: ["6379:6379"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Install dependencies
        run: uv sync

      - name: Lint
        run: uv run ruff check .

      - name: Test
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/testdb
          REDIS_URL: redis://localhost:6379/0
        run: uv run pytest --tb=short -q
```

### Java (Spring Boot) CI

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        ports: ["5432:5432"]
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Java
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: 21

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v4

      - name: Build and test
        env:
          SPRING_DATASOURCE_URL: jdbc:postgresql://localhost:5432/testdb
          SPRING_DATASOURCE_USERNAME: test
          SPRING_DATASOURCE_PASSWORD: test
        run: ./gradlew build

      - name: Upload test report
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: test-report
          path: build/reports/tests/
```

### C++ CI

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies
        run: sudo apt-get update && sudo apt-get install -y cmake g++

      - name: Build
        run: |
          mkdir build && cd build
          cmake .. -DCMAKE_BUILD_TYPE=Release
          make -j$(nproc)

      - name: Test
        run: cd build && ctest --output-on-failure
```

---

## 4. 트리거 (on)

### 이벤트 종류

```yaml
on:
  push:
    branches: [main, develop]
    paths:
      - "src/**"
      - "build.gradle.kts"
    paths-ignore:
      - "docs/**"
      - "*.md"

  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

  schedule:
    - cron: "0 9 * * 1"           # 매주 월요일 09:00 UTC

  workflow_dispatch:                # 수동 실행 버튼
    inputs:
      environment:
        description: "배포 환경"
        required: true
        default: staging
        type: choice
        options: [staging, production]

  release:
    types: [published]
```

---

## 5. 잡 구성

잡 구조는 YAML 순서보다 의존성 그래프로 이해해야 한다. 같은 파일에 적혀 있어도 `needs`가 없으면 병렬 실행된다.

![GitHub Actions job graph와 matrix 실행](./images/github-actions-job-graph.svg)

- `lint`와 `test`처럼 독립 잡은 동시에 돌리고, 배포는 `needs`로 뒤에 붙인다.
- `matrix`는 잡을 복제해 여러 환경 조합을 만든다. 잡 본문이 반복 실행된다고 생각하면 된다.
- 잡마다 파일 시스템이 분리되므로, 빌드 산출물 전달은 artifact가 필요하다.

### 병렬 실행 (기본)

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make lint

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make test

  # lint와 test는 동시에 실행된다
```

### 순차 실행 (needs)

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: make test

  deploy:
    needs: test                    # test 성공 후 실행
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - run: make deploy
```

### 매트릭스 빌드

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        java-version: [17, 21]
        db: [postgres, mysql]
      fail-fast: false             # 하나 실패해도 나머지 계속 실행

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: ${{ matrix.java-version }}
      - run: ./gradlew test
```

---

## 6. 서비스 컨테이너

잡 안에서 Docker 컨테이너를 사이드카로 띄운다.

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        ports: ["5432:5432"]
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7-alpine
        ports: ["6379:6379"]
        options: --health-cmd "redis-cli ping" --health-interval 10s

      kafka:
        image: confluentinc/cp-kafka:7.6.0
        ports: ["9092:9092"]
        env:
          KAFKA_NODE_ID: 1
          KAFKA_PROCESS_ROLES: broker,controller
          KAFKA_CONTROLLER_QUORUM_VOTERS: 1@localhost:9093
          KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093
          KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
          KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
          KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT
          KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
          CLUSTER_ID: ci-cluster-001
```

---

## 7. 시크릿과 환경 변수

### 시크릿 사용

```yaml
steps:
  - name: Deploy
    env:
      AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
      AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    run: aws ecs update-service --cluster prod --service api --force-new-deployment
```

**시크릿 설정:** Repository → Settings → Secrets and variables → Actions

### 환경(Environment)

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production        # 승인 필요하게 설정 가능
    steps:
      - run: echo "Deploying to ${{ vars.DEPLOY_TARGET }}"
```

### 기본 제공 변수

```yaml
steps:
  - run: |
      echo "브랜치: ${{ github.ref_name }}"
      echo "커밋: ${{ github.sha }}"
      echo "리포: ${{ github.repository }}"
      echo "이벤트: ${{ github.event_name }}"
      echo "PR 번호: ${{ github.event.pull_request.number }}"
      echo "러너 OS: ${{ runner.os }}"
```

---

## 8. 캐싱

캐시와 아티팩트는 둘 다 "파일을 남긴다"는 점은 같지만 목적이 다르다. 캐시는 다음 실행을 빠르게 하고, 아티팩트는 이번 실행의 결과물을 옮긴다.

![GitHub Actions 캐시와 아티팩트 흐름](./images/github-actions-cache-artifact-flow.svg)

- 캐시는 의존성 디렉터리를 재사용해 같은 job의 다음 실행 시간을 줄인다.
- 아티팩트는 잡 간 파일 전달과 실패 분석용 보고서 보관에 쓴다.
- 같은 워크플로 안의 잡도 디스크를 공유하지 않으므로, build 결과를 deploy로 넘길 때는 artifact가 필요하다.

```yaml
# Gradle 캐시
- uses: actions/setup-java@v4
  with:
    distribution: temurin
    java-version: 21
    cache: gradle                  # setup-java가 자동 캐싱

# 수동 캐시
- uses: actions/cache@v4
  with:
    path: |
      ~/.gradle/caches
      ~/.gradle/wrapper
    key: gradle-${{ runner.os }}-${{ hashFiles('**/*.gradle.kts') }}
    restore-keys: gradle-${{ runner.os }}-

# Python (uv) 캐시
- uses: astral-sh/setup-uv@v4
  with:
    enable-cache: true

# Node.js 캐시
- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: npm
```

---

## 9. 아티팩트

### 업로드

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: app-jar
    path: build/libs/*.jar
    retention-days: 7
```

### 잡 간 전달

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: ./gradlew bootJar
      - uses: actions/upload-artifact@v4
        with:
          name: app
          path: build/libs/*.jar

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: app
      - run: ls -la *.jar
```

---

## 10. Docker 빌드와 푸시

```yaml
jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:${{ github.sha }}
            ghcr.io/${{ github.repository }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

---

## 11. 조건부 실행

```yaml
steps:
  # main 브랜치만
  - if: github.ref == 'refs/heads/main'
    run: make deploy

  # PR만
  - if: github.event_name == 'pull_request'
    run: make lint

  # 이전 스텝 실패해도 실행
  - if: always()
    run: make cleanup

  # 이전 스텝 실패 시만
  - if: failure()
    run: make notify-failure

  # 특정 파일 변경 시
  - uses: dorny/paths-filter@v3
    id: changes
    with:
      filters: |
        backend:
          - 'src/**'
        docs:
          - 'docs/**'

  - if: steps.changes.outputs.backend == 'true'
    run: make test
```

---

## 12. 자주 하는 실수

| 실수 | 올바른 방법 |
|------|-------------|
| 시크릿을 workflow에 하드코딩 | Repository Secrets에 저장하고 `${{ secrets.KEY }}`로 참조 |
| 캐시 없이 매번 의존성 설치 | `actions/cache` 또는 setup-*의 캐시 옵션 사용 |
| `paths-ignore` 없이 모든 파일 변경에 CI 실행 | 문서 변경 시 불필요한 빌드 방지 |
| 서비스 컨테이너에 health check 없음 | `options`에 health-cmd 설정하여 준비 대기 |
| 실패 시 디버깅 정보 없음 | `if: failure()`로 테스트 리포트 업로드 |
| 모든 잡을 순차(needs)로 연결 | 독립적인 lint, test는 병렬로 실행 |
| `GITHUB_TOKEN` 권한 과다 | `permissions`로 최소 권한 설정 |

---

## 13. 빠른 참조

```yaml
# ── 최소 CI ──
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make test

# ── 트리거 ──
on:
  push: { branches: [main] }
  pull_request: { branches: [main] }
  schedule: [{ cron: "0 9 * * 1" }]
  workflow_dispatch: {}

# ── 잡 의존 ──
jobs:
  build: { ... }
  deploy: { needs: build, if: "github.ref == 'refs/heads/main'" }

# ── 서비스 ──
services:
  postgres: { image: "postgres:16", ports: ["5432:5432"], env: { POSTGRES_PASSWORD: test } }

# ── 시크릿 ──
env: { API_KEY: "${{ secrets.API_KEY }}" }

# ── 캐시 ──
- uses: actions/cache@v4
  with: { path: ~/.cache, key: "cache-${{ hashFiles('lock-file') }}" }

# ── 아티팩트 ──
- uses: actions/upload-artifact@v4
  with: { name: report, path: build/reports/ }
```
