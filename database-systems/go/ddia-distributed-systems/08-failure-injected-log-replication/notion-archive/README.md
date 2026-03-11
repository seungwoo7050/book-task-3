# 08-failure-injected-log-replication — notion 폴더 가이드

이 폴더는 Failure-Injected Log Replication 프로젝트의 이전 세대 장문 기록을 보관하는 자리입니다.

## 문서 구성

| 문서 | 내용 | 언제 읽으면 좋은가 |
|------|------|-------------------|
| [essay.md](essay.md) | retry, duplicate safety, quorum commit을 partial failure 관점에서 설명한 에세이 | replication harness의 의미를 큰 그림으로 다시 읽고 싶을 때 |
| [timeline.md](timeline.md) | 프로젝트 개발의 전체 과정을 시간순으로 재현한 타임라인 | 같은 프로젝트를 처음부터 다시 구현하고 싶을 때 |

## 프로젝트 한 줄 요약

drop, duplicate, pause가 있는 작은 네트워크 하네스 위에서 append/ack replication과 quorum commit을 재현합니다.

## 키워드

`log-replication` · `failure-injection` · `retry` · `idempotency` · `quorum-commit` · `catch-up`
