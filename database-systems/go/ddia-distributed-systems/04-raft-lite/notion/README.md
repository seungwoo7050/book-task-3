# 04-raft-lite — notion 폴더 가이드

이 폴더는 Raft Lite 프로젝트의 학습 과정과 설계 사고를 기록한 문서 모음입니다.

## 문서 구성

| 문서 | 내용 | 언제 읽으면 좋은가 |
|------|------|-------------------|
| [essay.md](essay.md) | Raft 합의 알고리즘의 핵심(선거, 로그 복제, 커밋)을 서사적으로 풀어낸 에세이 | 분산 합의의 "왜 필요하고 어떻게 작동하는가"를 이해하고 싶을 때 |
| [timeline.md](timeline.md) | 프로젝트 개발의 전체 과정을 시간순으로 재현한 타임라인 | 동일한 프로젝트를 처음부터 따라 구현하고 싶을 때 |

## 프로젝트 한 줄 요약

Tick 기반 동기 시뮬레이터에서 Raft의 leader election, AppendEntries consistency check, majority commit advancement, higher-term step-down을 구현한다.

## 키워드

`raft` · `leader-election` · `log-replication` · `majority-commit` · `term` · `step-down` · `heartbeat` · `RequestVote` · `AppendEntries` · `consensus`
