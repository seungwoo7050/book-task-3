# 06 Go API Standard — Notion 문서 안내

이 폴더는 프로젝트 06을 수행하면서 겪은 과정, 판단, 시행착오를 기록한 에세이 모음이다.
표준 라이브러리만으로 본격적인 REST API를 설계한 경험이 담겨 있다.

## 읽기 순서

| 순서 | 파일 | 언제 읽으면 좋은가 |
|------|------|---------------------|
| 1 | [00-problem-framing.md](00-problem-framing.md) | 왜 Movie CRUD를 문제로 골랐는지, 05번과 뭐가 다른지 알고 싶을 때. |
| 2 | [01-approach-log.md](01-approach-log.md) | application 구조, middleware 체인, graceful shutdown 설계를 따라갈 때. |
| 3 | [02-debug-log.md](02-debug-log.md) | middleware 순서, PATCH 부분 업데이트, shutdown 문제에서 막혔을 때. |
| 4 | [03-retrospective.md](03-retrospective.md) | 이 과제가 뒤 과제에 어떤 구조적 토대가 되는지 볼 때. |
| 5 | [04-knowledge-index.md](04-knowledge-index.md) | middleware, JSON envelope, graceful shutdown 패턴을 빠르게 찾을 때. |
| 6 | [05-timeline.md](05-timeline.md) | 전체 개발 과정을 시간순으로 재현하고 싶을 때. |

## 이 문서들의 성격

- **블로그형 에세이**: 처음 보는 사람이 흐름을 따라오게 만드는 문체로 쓰였다.
- **소스코드 보완**: 환경변수 설정, 미들웨어 체인 순서 결정, 코드 구조 분리 이유 등을 포함한다.
- **재현 가능성**: 이 문서와 소스코드를 함께 보면 프로젝트를 처음부터 다시 만들 수 있다.
