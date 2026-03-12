# backend-spring 저장소 기준

## 공개 표면

각 랩과 캡스톤은 최소한 아래 구조를 공개해야 합니다.

```text
README.md
problem/
spring/
docs/
notion/
```

각 레이어는 아래 질문을 담당합니다.

- `README.md`: 이 프로젝트가 무슨 문제를 풀고, 내 답이 무엇이며, 어디까지 검증했는가
- `problem/README.md`: canonical problem statement, 성공 기준, 의도적 제외 범위
- `spring/README.md`: 실행과 검증 명령, 런타임 전제 조건
- `docs/README.md`: 현재 구현 범위, 단순화, 다음 개선 방향
- `notion/README.md`: 개발 과정, 설계 결정, 디버깅, 재현 로그를 읽는 가이드

## README 기본 형식

프로젝트 루트 `README.md`는 가능한 한 첫 화면 안에서 아래를 답해야 합니다.

- 무슨 문제를 풀었는가
- 이번 단계의 답은 무엇인가
- 왜 이렇게 설계했는가
- 어떻게 다시 검증할 수 있는가
- 무엇을 일부러 남겼는가
- 다음에 어디를 읽어야 하는가

## `spring/` 워크스페이스 기준

각 `spring/` 디렉터리는 아래 구조를 유지합니다.

```text
src/main/java
src/main/resources
src/test/java
src/test/resources
build.gradle.kts
settings.gradle.kts
gradlew
gradle/wrapper
.env.example
Dockerfile
compose.yaml
Makefile
```

## 런타임 기준

- REST route는 `/api/v1` 아래에 둡니다.
- health endpoint는 `/api/v1/health/live`와 `/api/v1/health/ready`를 사용합니다.
- 오류 응답은 `ProblemDetail`에 `code`, `traceId`, `errors` 확장을 붙입니다.
- 로그는 JSON 형태를 우선합니다.
- OpenAPI는 코드에서 생성하고 springdoc으로 노출합니다.

## 검증 기준

각 `spring/` 워크스페이스는 최소한 아래 명령을 문서화해야 합니다.

- `make run`
- `make lint`
- `make test`
- `make smoke`
- `docker compose up --build`

문서에 적은 명령은 해당 `spring/` 디렉터리에서 실제로 재실행 가능해야 합니다.

## `notion/` 정책

- 이 레포의 `notion/` 디렉터리는 공개된 현재 학습 노트 세트입니다.
- `notion/`은 scratchpad가 아니라, 나중에 다시 봐도 재현 가능한 압축된 기록이어야 합니다.
- 권장 기본 세트는 `00-problem-framing.md`부터 `05-development-timeline.md`까지입니다.
- 공통 템플릿은 [templates/notion](templates/notion/README.md)에 둡니다.

## 언어와 주석 정책

- 공개 문서와 사람이 읽기 위한 설명 주석은 한국어를 기본으로 합니다.
- 식별자, 경로, 명령어, 프로토콜 이름, 설정 키, API route, 라이브러리 이름은 영어를 유지합니다.
- generated file이나 보일러플레이트까지 억지로 번역하지 않습니다.

## 공개 전 점검 기준

- 학습 트랙 또는 verified scaffold라는 성격이 명확히 드러나는가
- 문서에 적힌 검증 명령을 최근에 다시 실행했는가
- 알려진 단순화와 미검증 영역을 문서에 적었는가
- `notion/` 없이도 README와 docs만으로 현재 상태를 이해할 수 있는가
