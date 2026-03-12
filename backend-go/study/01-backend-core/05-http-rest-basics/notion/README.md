# 05 HTTP REST Basics — Notion 문서 안내

이 폴더는 프로젝트 05를 수행하면서 겪은 과정, 판단, 시행착오를 기록한 에세이 모음이다.
Go로 처음 JSON API를 만들어 본 경험이 담겨 있다.

## 읽기 순서

| 순서 | 파일 | 언제 읽으면 좋은가 |
|------|------|---------------------|
| 1 | [00-problem-framing.md](00-problem-framing.md) | 왜 이 네 개의 엔드포인트를 골랐는지 알고 싶을 때. |
| 2 | [01-approach-log.md](01-approach-log.md) | 라우팅, JSON I/O, idempotency 구현 과정을 따라갈 때. |
| 3 | [02-debug-log.md](02-debug-log.md) | 상태 코드 선택이나 pagination 경계에서 막혔을 때. |
| 4 | [03-retrospective.md](03-retrospective.md) | REST API 설계 감각에 대한 정리를 읽고 싶을 때. |
| 5 | [04-knowledge-index.md](04-knowledge-index.md) | net/http 패턴이나 httptest 사용법을 빠르게 찾을 때. |
| 6 | [05-development-timeline.md](05-development-timeline.md) | 전체 개발 과정을 시간순으로 재현하고 싶을 때. |

## 이 문서들의 성격

- **블로그형 에세이**: 처음 보는 사람이 흐름을 따라오게 만드는 문체로 쓰였다.
- **소스코드 보완**: curl 명령, 서버 실행, 상태 코드 선택 이유 등 코드에서 드러나지 않는 맥락을 포함한다.
- **재현 가능성**: 이 문서와 소스코드를 함께 보면 프로젝트를 처음부터 다시 만들 수 있다.
