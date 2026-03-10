# 02-leader-follower-replication — notion 폴더 가이드

이 폴더는 Leader-Follower Replication 프로젝트의 학습 과정과 설계 사고를 기록한 문서 모음입니다.

## 문서 구성

| 문서 | 내용 | 언제 읽으면 좋은가 |
|------|------|-------------------|
| [essay.md](essay.md) | Log shipping과 idempotent follower 설계를 서사적으로 풀어낸 에세이 | 복제의 "왜 상태가 아니라 로그를 보내는가"를 이해하고 싶을 때 |
| [timeline.md](timeline.md) | 프로젝트 개발의 전체 과정을 시간순으로 재현한 타임라인 | 동일한 프로젝트를 처음부터 따라 구현하고 싶을 때 |

## 프로젝트 한 줄 요약

Leader가 append-only mutation log를 기록하고, Follower가 watermark 이후의 entry만 가져와 idempotent하게 적용하는 log-shipping 기반 복제를 구현한다.

## 키워드

`leader-follower` · `log-shipping` · `append-only-log` · `mutation-log` · `watermark` · `idempotent-apply` · `incremental-sync` · `offset`
