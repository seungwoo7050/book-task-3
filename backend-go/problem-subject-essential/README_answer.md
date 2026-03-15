# backend-go 서버 개발 필수 답안지

이 문서는 Go 트랙에서 서버 공통성이 가장 높은 두 과제를 실제 `solution/go` 소스 기준으로 정리한 답안지다. 첫 문제는 goroutine 수명주기와 채널 조합을 안정적으로 끝내는 법을 다루고, 두 번째 문제는 DB write와 비동기 전달 사이의 정합성을 outbox와 멱등 소비자로 풀어낸다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [10-concurrency-patterns-go](10-concurrency-patterns-go_answer.md) | 시작 위치의 구현을 완성해 worker pool이 job 제출, 결과 수집, graceful shutdown을 지원한다, pipeline이 Generator -> Filter -> Sink 3단계로 동작한다, 모든 단계가 context cancellation을 존중한다를 한 흐름으로 설명하고 검증한다. 핵심은 main와 Generate, Filter 흐름을 구현하고 테스트를 통과시키는 것이다. | `make -C /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/10-concurrency-patterns/problem test` |
| [15-event-pipeline-go](15-event-pipeline-go_answer.md) | 시작 위치의 구현을 완성해 purchase transaction 안에서 outbox row를 함께 기록한다, relay가 미발행 이벤트를 읽어 Kafka topic으로 전달한다, aggregate_id 기준 ordering을 유지한다를 한 흐름으로 설명하고 검증한다. 핵심은 main와 New, Run 흐름을 구현하고 테스트를 통과시키는 것이다. | `make -C /Users/woopinbell/work/book-task-3/backend-go/study/03-platform-engineering/15-event-pipeline/problem test` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
