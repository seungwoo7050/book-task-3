# 03 Testing And Debugging — Notion 문서 안내

이 폴더는 프로젝트 03을 수행하면서 겪은 과정, 판단, 시행착오를 기록한 에세이 모음이다.
테스트 전략, 벤치마크, race detector를 처음 실전에 적용한 경험이 담겨 있다.

## 읽기 순서

| 순서 | 파일 | 언제 읽으면 좋은가 |
|------|------|---------------------|
| 1 | [00-problem-framing.md](00-problem-framing.md) | 왜 "로그 파싱"을 테스트 연습 문제로 골랐는지 알고 싶을 때. |
| 2 | [01-approach-log.md](01-approach-log.md) | table-driven test, subtest, benchmark를 어떻게 설계했는지 볼 때. |
| 3 | [02-debug-log.md](02-debug-log.md) | race condition이나 테스트 실패에서 막혔을 때. |
| 4 | [03-retrospective.md](03-retrospective.md) | Go 테스트 철학에 대한 정리를 읽고 싶을 때. |
| 5 | [04-knowledge-index.md](04-knowledge-index.md) | `go test` 플래그나 sync 패턴을 빠르게 찾을 때. |
| 6 | [05-timeline.md](05-timeline.md) | 전체 개발 과정을 시간순으로 재현하고 싶을 때. |

## 이 문서들의 성격

- **블로그형 에세이**: 처음 보는 사람이 흐름을 따라오게 만드는 문체로 쓰였다.
- **소스코드 보완**: 코드에서 드러나지 않는 테스트 전략 결정과 race detector 사용 경험을 포함한다.
- **재현 가능성**: 이 문서와 소스코드를 함께 보면 프로젝트를 처음부터 다시 만들 수 있다.
