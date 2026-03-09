# Docker Compose 완전 가이드

Docker Compose는 여러 컨테이너의 실행 환경을 YAML 하나로 선언하는 도구다. 로컬 개발 환경에서 DB, 캐시, 메시지 브로커, 앱 서버를 함께 띄우고 싶은 순간부터 Compose가 진가를 낸다. 핵심은 컨테이너 목록을 나열하는 것이 아니라, 서비스 간 관계와 준비 완료 조건을 코드로 고정하는 데 있다.

---

## 1. Docker Compose의 사고방식

Compose는 "컨테이너를 여러 개 실행하는 명령어"가 아니라, 한 프로젝트의 런타임 토폴로지를 선언하는 파일이다. 먼저 어떤 서비스가 서로를 어떤 이름으로 찾고, 어떤 데이터가 유지되며, 어떤 서비스만 선택적으로 켤지부터 잡아야 한다.

![Docker Compose 서비스 토폴로지와 읽는 기준](./images/docker-compose-topology.svg)

이 문서는 아래 세 질문으로 읽으면 된다.

1. **토폴로지:** 어떤 서비스가 내부 네트워크에서 누구와 통신하는가?
2. **준비 완료:** `started`와 `ready`를 어떻게 구분하고 앱 시작 시점을 제어할 것인가?
3. **환경 분리:** 기본 파일, override, profile 중 어떤 축으로 개발/디버그 구성을 나눌 것인가?

그림을 기준으로 보면 Compose는 세 가지 책임으로 정리된다.

- `services`는 실행할 컨테이너와 그 시작 방법을 정의한다.
- `networks`와 `volumes`는 서비스의 통신 경로와 데이터 보존 방식을 고정한다.
- `profiles`, override 파일, `.env`는 환경별 변형 범위를 통제한다.

### 핵심 개념

| 개념 | 의미 |
|------|------|
| 서비스 이름 = hostname | `postgres` 서비스는 내부 네트워크에서 `postgres:5432`로 접근한다 |
| `up -d` | 프로젝트 전체를 백그라운드로 기동한다 |
| `down` | 컨테이너와 네트워크를 정리한다. 볼륨은 유지된다 |
| `down -v` | 컨테이너와 named volume까지 삭제한다 |
| `depends_on` | 시작 순서를 정한다. 준비 완료를 보장하지는 않는다 |
| healthcheck | 서비스가 실제로 요청을 받을 준비가 되었는지 판별한다 |

---

## 2. 기본 구조

Compose 파일은 서비스 정의 하나만 잘 읽어도 대부분 이해된다. 아래 예시는 로컬 개발 환경에서 가장 흔한 `app + postgres + redis` 구성을 보여준다.

```yaml
# compose.yml
services:
  postgres:
    image: postgres:16
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
      POSTGRES_DB: myapp
    volumes:
      - pg-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U dev"]
      interval: 5s
      timeout: 3s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgresql://dev:dev@postgres:5432/myapp
      REDIS_URL: redis://redis:6379
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy

volumes:
  pg-data:
```

이 예제는 Compose를 읽는 기본 규칙을 한 번에 보여준다.

- `app`은 호스트 포트 `3000`으로 노출되지만, 내부에서는 `postgres`, `redis` 서비스 이름으로 통신한다.
- `pg-data`는 컨테이너를 내렸다 올려도 DB 데이터가 남도록 보장한다.
- `condition: service_healthy`를 붙여야 앱이 "컨테이너 생성"이 아니라 "실제 준비 완료"를 기다린다.

---

## 3. 서비스 설정 상세

### `image` vs `build`

```yaml
services:
  postgres:
    image: postgres:16

  api:
    build:
      context: .
      dockerfile: Dockerfile
      target: development
      args:
        NODE_VERSION: "22"

  web:
    build: ./frontend
    image: myapp/web:latest
```

- `image`는 이미 존재하는 이미지를 바로 가져온다.
- `build`는 로컬 Dockerfile로 이미지를 만든다.
- 둘을 같이 쓰면 "이 Dockerfile로 빌드한 이미지에 이 태그를 붙인다"는 뜻이다.

### `ports`

```yaml
ports:
  - "8080:3000"
  - "127.0.0.1:5432:5432"
  - "3000"
```

- `"호스트:컨테이너"` 형식이다.
- `127.0.0.1:`를 붙이면 외부 접근을 막고 로컬에서만 바인딩한다.
- 컨테이너 포트만 적으면 호스트 포트는 자동 할당된다.

### `volumes`

```yaml
services:
  api:
    volumes:
      - pg-data:/var/lib/postgresql/data
      - ./src:/app/src
      - ./config:/app/config:ro
      - /app/node_modules

volumes:
  pg-data:
    driver: local
```

- named volume은 영속 데이터를 Docker가 관리하게 만든다.
- bind mount는 호스트 파일 변경을 즉시 반영할 때 쓴다.
- 읽기 전용 설정 파일은 `:ro`로 마운트한다.
- `/app/node_modules` 같은 익명 볼륨은 bind mount가 의존성을 덮어쓰는 문제를 막을 때 자주 쓴다.

### `environment`와 `env_file`

```yaml
services:
  api:
    environment:
      NODE_ENV: development
      DATABASE_URL: postgresql://dev:dev@postgres:5432/myapp

    env_file:
      - .env
      - .env.local
```

```yaml
services:
  api:
    env_file: .env
    environment:
      NODE_ENV: development
```

- `env_file`은 여러 키를 한 번에 로드한다.
- 같은 키가 중복되면 `environment` 값이 최종 우선순위를 가진다.
- 민감 정보는 실제 운영에서는 Compose 파일보다 별도 시크릿 관리 체계로 빼는 편이 안전하다.

---

## 4. `depends_on`과 healthcheck

Compose에서 가장 자주 틀리는 부분은 "컨테이너가 떴다"와 "서비스가 준비됐다"를 같은 뜻으로 보는 것이다. DB는 프로세스가 먼저 뜨더라도 초기화가 끝나기 전까지는 연결을 받지 못할 수 있다.

![Docker Compose 준비 완료 흐름](./images/docker-compose-readiness.svg)

그림 아래 운영 규칙은 단순하다.

- `depends_on`만 쓰면 생성 순서만 보장되고, 앱은 여전히 너무 일찍 시작할 수 있다.
- healthcheck는 "이 서비스가 지금 요청을 받아도 되는가"를 주기적으로 묻는 장치다.
- 앱이 DB/캐시를 강하게 의존한다면 `condition: service_healthy`를 붙여 시작 시점을 지연시킨다.

### 올바른 패턴

```yaml
services:
  postgres:
    image: postgres:16
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U dev"]
      interval: 5s
      timeout: 3s
      retries: 5
      start_period: 10s

  api:
    depends_on:
      postgres:
        condition: service_healthy
```

### 자주 쓰는 healthcheck

```yaml
# PostgreSQL
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]

# MySQL
healthcheck:
  test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]

# Redis
healthcheck:
  test: ["CMD", "redis-cli", "ping"]

# HTTP 서비스
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:3000/health"]

# Kafka (kraft mode)
healthcheck:
  test: ["CMD-SHELL", "kafka-broker-api-versions --bootstrap-server localhost:9092"]
```

---

## 5. 네트워크와 볼륨

Compose는 프로젝트 단위 네트워크를 자동으로 만들어 주지만, 트래픽 경계를 명확히 하고 싶다면 네트워크를 직접 나누는 편이 좋다.

```yaml
services:
  api:
    networks:
      - backend

  web:
    networks:
      - frontend
      - backend

  postgres:
    networks:
      - backend

networks:
  frontend:
  backend:
```

이 구조는 다음을 의미한다.

- `web`은 `frontend`, `backend` 둘 다 붙어서 브라우저 요청도 받고 API도 호출할 수 있다.
- `postgres`는 `backend`에만 붙어서 `web`이 직접 접근하지 못한다.
- 네트워크를 명시하지 않으면 Compose는 `<project>_default` 네트워크 하나를 만들고 모든 서비스를 거기에 연결한다.

데이터 보존 기준도 함께 명확히 잡아야 한다.

- DB 데이터, 업로드 파일은 named volume에 둔다.
- 애플리케이션 소스와 설정은 bind mount로 연결한다.
- 테스트 DB처럼 빠르게 버려도 되는 상태는 `tmpfs`를 고려한다.

---

## 6. 환경별 설정: override와 profiles

로컬 개발, 디버그, CI, 데모 환경을 같은 Compose 파일 하나로 모두 해결하려 하면 금방 지저분해진다. 기본 파일은 공통 토폴로지에 집중하고, 차이는 override와 profile로 분리하는 편이 읽기 쉽다.

![Docker Compose 설정 병합과 profiles](./images/docker-compose-config-merge.svg)

이 섹션의 읽는 기준은 세 가지다.

- 공통 서비스 정의는 `compose.yml`에 두고, 개발 편의성은 `compose.override.yml`에 덧씌운다.
- 옵션성 도구는 `profiles`로 분리해서 필요할 때만 켠다.
- 최종 결과가 헷갈리면 항상 `docker compose config`로 병합 결과를 출력해 확인한다.

### `profiles` — 선택적 서비스

```yaml
services:
  postgres:
    image: postgres:16

  redis:
    image: redis:7-alpine

  mailhog:
    image: mailhog/mailhog
    profiles: [debug]

  adminer:
    image: adminer
    profiles: [debug]
    ports:
      - "8080:8080"
```

```bash
docker compose up -d
docker compose --profile debug up -d
```

### override 파일

```yaml
# compose.yml
services:
  api:
    build: .
    environment:
      NODE_ENV: production
```

```yaml
# compose.override.yml
services:
  api:
    volumes:
      - ./src:/app/src
    environment:
      NODE_ENV: development
    command: npx tsx watch src/server.ts
```

```bash
docker compose up -d
docker compose -f compose.yml -f compose.prod.yml up -d
```

---

## 7. 실전 Compose 예제

### 풀스택 개발 환경

```yaml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
      POSTGRES_DB: myapp
    ports:
      - "5432:5432"
    volumes:
      - pg-data:/var/lib/postgresql/data
      - ./docker/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U dev"]
      interval: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      retries: 5

  api:
    build:
      context: .
      target: development
    ports:
      - "3000:3000"
    volumes:
      - ./src:/app/src
      - /app/node_modules
    environment:
      NODE_ENV: development
      DATABASE_URL: postgresql://dev:dev@postgres:5432/myapp
      REDIS_URL: redis://redis:6379
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    command: npx tsx watch src/server.ts

  mailhog:
    image: mailhog/mailhog
    ports:
      - "1025:1025"
      - "8025:8025"

volumes:
  pg-data:
```

### 멀티 DB 테스트 환경

```yaml
services:
  test-db:
    image: postgres:16
    environment:
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
      POSTGRES_DB: test
    ports:
      - "5433:5432"
    tmpfs:
      - /var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U test"]
      interval: 2s
      retries: 10
```

---

## 8. 자주 쓰는 명령어

```bash
# ── 생명주기 ──
docker compose up -d
docker compose up -d --build
docker compose down
docker compose down -v
docker compose restart api

# ── 상태 확인 ──
docker compose ps
docker compose ps -a
docker compose logs -f
docker compose logs -f api
docker compose top

# ── 실행 ──
docker compose exec postgres psql -U dev
docker compose run --rm api npm test

# ── 디버깅 ──
docker compose config
docker compose events

# ── 정리 ──
docker compose down --rmi all -v
docker system prune
```

---

## 9. 자주 하는 실수

| 실수 | 원인과 해결 |
|------|-------------|
| DB 기동 전 앱 연결 실패 | `depends_on` + `condition: service_healthy` + healthcheck를 함께 사용한다 |
| 포트 충돌 | `lsof -i :5432`로 확인하고 호스트 포트를 바꾼다 |
| `down`이 데이터를 지웠다고 오해 | `down`은 볼륨 유지, `down -v`만 볼륨 삭제다 |
| `.env` 변수 미적용 | `docker compose config`로 치환 결과를 확인한다 |
| `depends_on`만으로 준비 완료를 기대 | 준비 완료는 healthcheck가 담당한다 |
| 빌드 캐시로 변경 미반영 | `docker compose up -d --build` 또는 `docker compose build --no-cache`를 사용한다 |
| bind mount 권한 문제 | 컨테이너 사용자와 호스트 파일 소유자를 맞춘다 |
| named volume과 bind mount 혼동 | named는 Docker 관리, bind는 호스트 경로 직접 공유다 |

---

## 10. 빠른 참조

```yaml
services:
  name:
    image: img:tag
    build: .
    ports: ["호스트:컨테이너"]
    environment: { KEY: val }
    env_file: .env
    volumes: [...]
    depends_on:
      other:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "..."]
      interval: 5s
      retries: 5
    command: override_cmd
    restart: unless-stopped
    profiles: [debug]
    networks: [backend]

volumes:
  name:

networks:
  name:
```
