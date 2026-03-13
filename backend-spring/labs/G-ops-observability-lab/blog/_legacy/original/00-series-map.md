# G-ops-observability-lab 시리즈 지도

`G-ops-observability-lab`은 운영성을 다른 프로젝트의 부록으로 숨기지 않고, health endpoint, trace ID, JSON logging, metrics exposure를 독립 학습 대상으로 분리한 랩이다. macOS + VSCode 통합 터미널에서 `make test`를 다시 돌려 보면 이 랩이 말하는 운영 기본기는 거대한 플랫폼이 아니라 애플리케이션이 스스로를 어떤 표면으로 드러내느냐에 가깝다.

## 이 프로젝트가 푸는 문제

- health/live, health/ready를 분리한다.
- 구조화 로그와 trace ID를 남긴다.
- actuator Prometheus endpoint를 열고 ops summary에서 핵심 링크를 보여 준다.
- 현재 실제 근거가 있는 운영 표면과 아직 문서 단계인 영역을 나눠 적는다.

## 이 시리즈의 근거

- `problem/README.md`
- `docs/README.md`
- `spring/README.md`
- `HealthController`, `TraceIdFilter`, `OpsController`
- `application.yml`, `logback-spring.xml`
- `OpsApiTest`
- `2026-03-13` `make test` 재실행, `2026-03-09` 검증 보고

## 읽는 순서

1. `10-development-timeline.md`
2. `_evidence-ledger.md`
3. `_structure-outline.md`

## 시리즈의 중심 질문

- 운영성은 어떤 코드와 설정이 있어야 "있다"고 말할 수 있는가
- trace ID와 JSON logging은 왜 같은 이야기인가
- 현재 문서에만 있고 아직 파일 근거가 없는 운영 요소는 무엇인가
