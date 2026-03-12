# 04 SQL And Data Modeling — Notion 문서 안내

이 폴더는 프로젝트 04를 수행하면서 겪은 과정, 판단, 시행착오를 기록한 에세이 모음이다.
SQL 스키마 설계, join, transaction을 Go에서 처음 다룬 경험이 담겨 있다.

## 읽기 순서

| 순서 | 파일 | 언제 읽으면 좋은가 |
|------|------|---------------------|
| 1 | [00-problem-framing.md](00-problem-framing.md) | 왜 "게임 상점 스키마"를 문제로 골랐는지 알고 싶을 때. |
| 2 | [01-approach-log.md](01-approach-log.md) | 스키마 설계와 트랜잭션 구현 흐름을 따라갈 때. |
| 3 | [02-debug-log.md](02-debug-log.md) | SQLite, FK, ON CONFLICT 관련 문제에서 막혔을 때. |
| 4 | [03-retrospective.md](03-retrospective.md) | SQL 모델링 감각이 뒤 과제에 어떻게 이어지는지 볼 때. |
| 5 | [04-knowledge-index.md](04-knowledge-index.md) | SQL 패턴이나 database/sql 사용법을 빠르게 찾을 때. |
| 6 | [05-development-timeline.md](05-development-timeline.md) | 전체 개발 과정을 시간순으로 재현하고 싶을 때. |

## 이 문서들의 성격

- **블로그형 에세이**: 처음 보는 사람이 흐름을 따라오게 만드는 문체로 쓰였다.
- **소스코드 보완**: SQLite 드라이버 선택, 의존성 설치, 스키마 설계 이유 등 코드에서 드러나지 않는 결정을 포함한다.
- **재현 가능성**: 이 문서와 소스코드를 함께 보면 프로젝트를 처음부터 다시 만들 수 있다.
