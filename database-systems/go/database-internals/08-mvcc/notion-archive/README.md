# 08-mvcc — notion 폴더 가이드

이 폴더는 MVCC(Multi-Version Concurrency Control) 프로젝트의 학습 과정과 설계 사고를 기록한 문서 모음입니다.

## 문서 구성

| 문서 | 내용 | 언제 읽으면 좋은가 |
|------|------|-------------------|
| [essay.md](essay.md) | 스냅샷 격리와 버전 체인의 설계 과정을 서사적으로 풀어낸 에세이 | MVCC의 "왜"와 "어떻게"를 깊이 이해하고 싶을 때 |
| [timeline.md](timeline.md) | 프로젝트 개발의 전체 과정을 시간순으로 재현한 타임라인 | 동일한 프로젝트를 처음부터 따라 구현하고 싶을 때 |

## 프로젝트 한 줄 요약

트랜잭션 매니저를 중심으로 스냅샷 격리(Snapshot Isolation)를 구현한다. 버전 체인으로 다중 버전을 관리하고, first-committer-wins 규칙으로 write-write 충돌을 감지하며, GC로 불필요한 구버전을 정리한다.

## 키워드

`MVCC` · `snapshot-isolation` · `version-chain` · `first-committer-wins` · `write-write-conflict` · `garbage-collection` · `read-your-own-writes` · `transaction-manager`
