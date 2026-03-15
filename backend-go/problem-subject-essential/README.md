# backend-go 서버 개발 필수 문제지

`backend-go`는 웹 백엔드 비중이 큰 트랙이라, 엄격한 서버 공통 필수 기준으로 남는 문제가 많지 않습니다.
여기서는 웹 백엔드와 게임 서버를 함께 놓고 봐도 직접성이 높은 문제만 남깁니다.
이 트랙의 종합 과제는 [`../problem-subject-capstone/README.md`](../problem-subject-capstone/README.md)로 분리합니다.

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [10-concurrency-patterns-go](10-concurrency-patterns-go.md) | 시작 위치의 구현을 완성해 worker pool이 job 제출, 결과 수집, graceful shutdown을 지원한다, pipeline이 Generator -> Filter -> Sink 3단계로 동작한다, 모든 단계가 context cancellation을 존중한다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/10-concurrency-patterns/problem test` |
| [15-event-pipeline-go](15-event-pipeline-go.md) | 시작 위치의 구현을 완성해 purchase transaction 안에서 outbox row를 함께 기록한다, relay가 미발행 이벤트를 읽어 Kafka topic으로 전달한다, aggregate_id 기준 ordering을 유지한다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/backend-go/study/03-platform-engineering/15-event-pipeline/problem test` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
