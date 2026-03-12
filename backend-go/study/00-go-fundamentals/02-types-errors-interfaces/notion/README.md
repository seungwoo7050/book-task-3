# 02 Types Errors Interfaces — Notion 문서 안내

이 폴더는 프로젝트 02를 수행하면서 겪은 과정, 판단, 시행착오를 기록한 에세이 모음이다.
struct, interface, custom error를 처음 분리해 본 경험이 담겨 있다.

## 읽기 순서

| 순서 | 파일 | 언제 읽으면 좋은가 |
|------|------|---------------------|
| 1 | [00-problem-framing.md](00-problem-framing.md) | 왜 "상품 카탈로그"를 문제로 골랐는지 알고 싶을 때. |
| 2 | [01-approach-log.md](01-approach-log.md) | struct, interface, error 설계 흐름을 따라가고 싶을 때. |
| 3 | [02-debug-log.md](02-debug-log.md) | pointer receiver나 에러 비교에서 막혔을 때 참고할 때. |
| 4 | [03-retrospective.md](03-retrospective.md) | 이 과제가 뒤 과제에 어떤 토대가 되는지 정리하고 싶을 때. |
| 5 | [04-knowledge-index.md](04-knowledge-index.md) | interface, errors.As 등 특정 패턴을 빠르게 찾고 싶을 때. |
| 6 | [05-development-timeline.md](05-development-timeline.md) | 전체 개발 과정을 시간순으로 재현하고 싶을 때. |

## 이 문서들의 성격

- **블로그형 에세이**: 처음 보는 사람이 흐름을 따라오게 만드는 문체로 쓰였다.
- **소스코드 보완**: 코드에서 드러나지 않는 설계 결정과 에러 처리 선택의 이유를 포함한다.
- **재현 가능성**: 이 문서와 소스코드를 함께 보면 프로젝트를 처음부터 다시 만들 수 있다.
