# Primer — 시작하기 전에 먼저 읽는 개념서

각 문서는 공식 문서를 읽기 전에 감을 잡는 짧은 안내서다. 문법 전부를 다루지 않고, 실무에서 반복되는 패턴과 사고방식을 먼저 전달한다. 마지막에만 짧은 빠른 참조를 붙인다.

## 어떻게 읽을지

1. 언어 한 편, 프레임워크 한 편, 도구 한 편을 골라 읽는다.
2. 실제 코드를 연 뒤, 필요할 때만 각 문서의 **빠른 참조** 섹션으로 돌아온다.

---

## 목적별 추천 순서

| 목적 | 추천 읽기 순서 |
|------|----------------|
| 알고리즘 문제 풀이 | [Python](language/python.md) → [C++](language/cpp.md) → [Makefile](tool/makefile.md) |
| 시스템 프로그래밍 | [C](language/c.md) → [C++](language/cpp.md) → [CMake](tool/cmake.md) → [Makefile](tool/makefile.md) |
| 네트워크 실습 | [Python](language/python.md) → [C++](language/cpp.md) → [CMake](tool/cmake.md) → [Wireshark](tool/wireshark.md) |
| Go 백엔드 | [Go](language/go.md) → [SQL](database/sql.md) → [gRPC](backend/grpc.md) → [Docker](devops/docker.md) → [Docker Compose](devops/docker-compose.md) → [Observability](devops/observability-reliability.md) → [Makefile](tool/makefile.md) |
| Node 백엔드 | [TypeScript](language/typescript.md) → [Node.js](backend/nodejs.md) → [Express](backend/express.md) 또는 [NestJS](backend/nestjs.md) → [Drizzle ORM](database/drizzle-orm.md) → [Vitest](testing/vitest.md) → [Load Testing](testing/load-testing.md) |
| Python 백엔드 | [Python](language/python.md) → [FastAPI](backend/fastapi.md) → [Pydantic](backend/pydantic.md) → [SQLAlchemy](database/sqlalchemy.md) → [Celery](backend/celery.md) → [Redis](database/redis.md) → [uv](tool/uv-py.md) → [pytest](testing/pytest.md) → [Load Testing](testing/load-testing.md) → [Observability](devops/observability-reliability.md) → [GitHub Actions](devops/github-actions.md) |
| 프론트엔드 | [HTML](frontend/html.md) → [CSS](frontend/css.md) → [TypeScript](language/typescript.md) → [React](frontend/react.md) → [Next.js](frontend/nextjs.md) → [Vite](frontend/vite.md) → [Vitest](testing/vitest.md) → [Playwright](testing/playwright.md) |
| 모바일 앱 | [TypeScript](language/typescript.md) → [React](frontend/react.md) → [React Native](frontend/react-native.md) → [Kotlin](language/kotlin.md) → [Swift](language/swift.md) |
| Spring 백엔드 | [Java](language/java.md) → [Spring Boot](backend/spring-boot.md) → [Spring Data JPA](database/spring-data-jpa.md) → [Gradle](tool/gradle.md) → [Redis](database/redis.md) → [Kafka](backend/kafka.md) → [JUnit 5](testing/junit.md) → [GitHub Actions](devops/github-actions.md) |
| C++ 서버 | [C++](language/cpp.md) → [CMake](tool/cmake.md) → [Makefile](tool/makefile.md) → [Load Testing](testing/load-testing.md) → [Failure Injection](devops/failure-injection.md) → [GitHub Actions](devops/github-actions.md) |
| 클라우드·보안 | [Python](language/python.md) → [Terraform](devops/terraform.md) → [Docker](devops/docker.md) → [Docker Compose](devops/docker-compose.md) → [Observability](devops/observability-reliability.md) → [Failure Injection](devops/failure-injection.md) → [Makefile](tool/makefile.md) |
| **캡스톤 제출 공통** | [Observability](devops/observability-reliability.md) → [Load Testing](testing/load-testing.md) → [Failure Injection](devops/failure-injection.md) → [Capstone Path](submission/root-to-three-capstones.md) → [Submission Rubric](submission/submission-readiness-rubric.md) |

---

## 전체 문서 목록

### Language

프로그래밍 언어의 핵심 사고방식과 실무 패턴.

| 문서 | 한줄 요약 |
|------|-----------|
| [C](language/c.md) | 메모리를 직접 관리하는 시스템 언어 |
| [C++](language/cpp.md) | STL과 RAII 중심의 시스템·알고리즘 언어 |
| [Python](language/python.md) | 스크립트부터 서비스까지 폭넓은 범용 언어 |
| [Go](language/go.md) | 표준 라이브러리 중심의 서버 언어 |
| [JavaScript](language/javascript.md) | 브라우저와 Node를 잇는 동적 언어 |
| [TypeScript](language/typescript.md) | 컴파일 시점 타입으로 설계를 강화하는 JS 상위 집합 |
| [Kotlin](language/kotlin.md) | Android 네이티브 진입점 언어 |
| [Java](language/java.md) | 정적 타입 클래스 기반의 JVM 범용 언어 |
| [Swift](language/swift.md) | iOS 네이티브 진입점 언어 |

### Frontend

웹·모바일 UI를 구성하는 마크업, 스타일, 프레임워크.

| 문서 | 한줄 요약 |
|------|-----------|
| [HTML](frontend/html.md) | 웹 플랫폼의 시맨틱 구조와 접근성 기초 |
| [CSS](frontend/css.md) | 박스 모델, 레이아웃, 반응형 스타일링 |
| [React](frontend/react.md) | 컴포넌트 트리로 UI를 선언하는 라이브러리 |
| [Next.js](frontend/nextjs.md) | 파일 기반 라우팅과 서버 컴포넌트를 얹은 React 프레임워크 |
| [React Native](frontend/react-native.md) | React로 네이티브 모바일 앱을 만드는 프레임워크 |
| [Vite](frontend/vite.md) | ESM 네이티브 개발 서버와 Rollup 번들링을 제공하는 빌드 도구 |

### Backend

서버 런타임, HTTP 프레임워크, 데이터 검증, RPC.

| 문서 | 한줄 요약 |
|------|-----------|
| [Node.js](backend/nodejs.md) | JS/TS 실행 환경이자 빌드 오케스트레이터 |
| [Express](backend/express.md) | 미들웨어 파이프라인 기반의 경량 HTTP 프레임워크 |
| [NestJS](backend/nestjs.md) | 데코레이터와 모듈로 구조를 강제하는 Node 프레임워크 |
| [Fastify](backend/fastify.md) | 스키마 기반 검증과 플러그인 캡슐화 중심의 Node.js 프레임워크 |
| [FastAPI](backend/fastapi.md) | Pydantic 모델 중심의 Python 비동기 API 프레임워크 |
| [Pydantic](backend/pydantic.md) | 타입힌트 기반 런타임 검증 모델 시스템 |
| [Spring Boot](backend/spring-boot.md) | 자동 구성 기반의 Java 백엔드 프레임워크 |
| [Celery](backend/celery.md) | Python 비동기 작업 큐 |
| [Kafka](backend/kafka.md) | 분산 이벤트 스트리밍 플랫폼 |
| [gRPC](backend/grpc.md) | Protocol Buffers 기반의 스키마 중심 RPC 프레임워크 |

### Database

데이터 저장, 질의, ORM.

| 문서 | 한줄 요약 |
|------|-----------|
| [SQL](database/sql.md) | 관계형 데이터를 다루는 선언적 질의 언어 |
| [SQLAlchemy](database/sqlalchemy.md) | Python의 표준 ORM과 DB 세션 관리 |
| [Spring Data JPA](database/spring-data-jpa.md) | Repository 추상화 기반의 Java ORM |
| [Drizzle ORM](database/drizzle-orm.md) | 타입 안전 스키마와 쿼리 빌더를 제공하는 TS ORM |
| [Redis](database/redis.md) | 인메모리 키-값 데이터 저장소 |

### Testing

단위·통합·E2E·성능 테스트 프레임워크.

| 문서 | 한줄 요약 |
|------|-----------|
| [Vitest](testing/vitest.md) | Vite 기반 TypeScript 테스트 러너 |
| [Playwright](testing/playwright.md) | 사용자 흐름 기반 E2E 테스트 도구 |
| [pytest](testing/pytest.md) | Python 테스트 프레임워크 |
| [JUnit 5](testing/junit.md) | Java 테스트 프레임워크 |
| [Load Testing](testing/load-testing.md) | k6·Locust·C++ 하네스 기반 성능 측정과 SLO 검증 |

### Submission

캡스톤 제출 준비와 판정 기준.

| 문서 | 한줄 요약 |
|------|-----------|
| [Capstone Path](submission/root-to-three-capstones.md) | 공통 기반에서 세 캡스톤 분기로 이어지는 제출 경로 |
| [Submission Readiness Rubric](submission/submission-readiness-rubric.md) | 기능·재현·테스트·운영 증거·문서 기준 제출 판정 스코어카드 |

### DevOps

컨테이너, 인프라, 배포, 관측성.

| 문서 | 한줄 요약 |
|------|-----------|
| [Docker](devops/docker.md) | 컨테이너 이미지 빌드와 실행의 기본 도구 |
| [Docker Compose](devops/docker-compose.md) | 로컬 인프라를 선언적으로 띄우는 도구 |
| [Terraform](devops/terraform.md) | 인프라를 코드로 선언하고 관리하는 IaC 도구 |
| [GitHub Actions](devops/github-actions.md) | GitHub 내장 CI/CD 파이프라인 |
| [Observability & Reliability](devops/observability-reliability.md) | SLI/SLO 모델, 로깅·메트릭·트레이싱 최소 구성, 인시던트 템플릿 |
| [Failure Injection](devops/failure-injection.md) | 재현 가능한 로컬 장애 훈련 시나리오 |

### Tool

빌드 시스템, 패키지 관리, 개발 워크플로.

| 문서 | 한줄 요약 |
|------|-----------|
| [Makefile](tool/makefile.md) | 빌드·테스트·실행의 표준 인터페이스 |
| [CMake](tool/cmake.md) | 멀티 타깃 C/C++ 빌드 시스템 |
| [uv](tool/uv-py.md) | Python 의존성·실행 환경 통합 관리 도구 |
| [Git](tool/git.md) | 버전 관리와 협업의 기본 도구 |
| [Gradle](tool/gradle.md) | JVM 프로젝트 빌드 자동화 도구 |
| [Wireshark](tool/wireshark.md) | 프로토콜 계층별 패킷 분석 도구 |

---

## 이 시리즈의 원칙

- **문법 전부를 다루지 않는다.** 공식 문서를 대체하지 않고, 진입 장벽을 낮추는 데 집중한다.
- **실무에서 반복되는 패턴만 남긴다.** 한 번 쓰고 버리는 트릭 대신, 매번 마주치는 구조를 다룬다.
- **사고방식을 먼저, 명령어를 나중에 준다.** 왜 그렇게 하는지를 알면 명령어는 자연히 따라온다.
