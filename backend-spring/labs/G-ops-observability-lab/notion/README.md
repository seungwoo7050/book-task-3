# G-ops-observability-lab — Notion 문서 가이드

이 디렉토리는 Ops & Observability Lab의 학습 과정을 기록한 문서들을 담고 있다.

## 문서 구성

| 순서 | 파일 | 내용 |
|------|------|------|
| 0 | [00-problem-framing.md](./00-problem-framing.md) | 운영을 별도 주제로 분리한 이유, 범위와 제약 조건 |
| 1 | [01-approach-log.md](./01-approach-log.md) | 세 가지 방향 비교, 운영 기본기(health, logging, metrics, CI) 중심 선택 |
| 2 | [02-debug-log.md](./02-debug-log.md) | "Observability Lab" 이름과 실제 구현 depth의 괴리 |
| 3 | [03-retrospective.md](./03-retrospective.md) | 잘한 것(운영 분리), 약한 것(alert/dashboard 없음), 개선 방향 |
| 4 | [04-knowledge-index.md](./04-knowledge-index.md) | Health/Readiness, Structured Logging, Trace ID, Prometheus, Observability 세 기둥 |
| 5 | [05-timeline.md](./05-timeline.md) | Docker Compose, Prometheus, logback-spring.xml 등 소스코드에 없는 작업 기록 |

## 읽는 순서

처음이라면 **00 → 01 → 03** 순서로 읽으면 "왜 운영을 별도 랩으로 만들었고, 무엇이 부족한지"를 빠르게 파악할 수 있다.

운영 개념을 학습하려면 **04-knowledge-index.md**에서 Health vs Readiness, Structured Logging, Trace ID, Prometheus metrics, Observability 세 기둥의 정의와 현재 구현 상태를 확인한다.

## 이 랩의 핵심 포인트

- **운영은 "나중에 붙는 것"이 아니라 백엔드 기본기**라는 선언
- **JSON logging + Trace ID + Health endpoints + Prometheus scrape**가 현재 증명된 범위
- **Alert rules, 대시보드, 분산 트레이싱, IaC는 아직 미완** — 이것을 숨기지 않는 것이 핵심
- 다른 랩들의 `global/` 패키지에 있는 운영 코드의 **why를 설명하는 장소**

## 관련 문서

- [docs/README.md](../docs/README.md) — 구현 범위, simplification, next improvements
- [problem/README.md](../problem/README.md) — 랩 출제 의도
