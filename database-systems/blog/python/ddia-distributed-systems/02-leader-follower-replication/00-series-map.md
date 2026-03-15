# 02 Leader-Follower Replication

## 왜 이 랩을 다시 읽어야 하나

이 프로젝트의 표면은 단순한 key-value 복제처럼 보이지만, 실제로는 "현재 상태"를 보내지 않고 "상태를 만든 ordered mutation log"를 follower가 watermark 이후부터 따라가게 만드는 연습이다. 그래서 핵심 질문도 `dict` 두 개를 맞추는 일이 아니라, leader가 어떤 순서로 log를 쌓는지, follower가 어디까지 적용했는지를 어떻게 기억하는지, 같은 batch를 다시 받아도 왜 결과가 변하지 않는지를 확인하는 쪽에 있다.

이번 시리즈는 기존 blog를 입력으로 삼지 않고 [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/problem/README.md), [`core.py`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/src/leader_follower/core.py), [`test_replication.py`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/tests/test_replication.py), 그리고 2026-03-14 재실행 결과만으로 다시 구성했다.

## 이번 랩에서 끝까지 붙들 질문

- leader는 local state와 replication log를 어떤 순서로 함께 갱신하는가
- follower는 어떤 기준으로 incremental sync 범위를 자르는가
- duplicate batch replay가 실제로 왜 무해한가
- 반대로 이 랩이 아직 다루지 않는 failure model은 어디까지인가

## 문서 지도

- [10-chronology-scope-and-surface.md](/Users/woopinbell/work/book-task-3/database-systems/blog/python/ddia-distributed-systems/02-leader-follower-replication/10-chronology-scope-and-surface.md): 문제 범위, 코드 표면, 첫 replication 흐름을 시간순으로 정리한다.
- [20-chronology-core-invariants.md](/Users/woopinbell/work/book-task-3/database-systems/blog/python/ddia-distributed-systems/02-leader-follower-replication/20-chronology-core-invariants.md): sequential offset, watermark, idempotent apply라는 핵심 invariant를 소스 기준으로 설명한다.
- [30-chronology-verification-and-boundaries.md](/Users/woopinbell/work/book-task-3/database-systems/blog/python/ddia-distributed-systems/02-leader-follower-replication/30-chronology-verification-and-boundaries.md): pytest와 수동 replay 결과를 묶어 현재 검증 범위와 남은 경계를 정리한다.
- [_evidence-ledger.md](/Users/woopinbell/work/book-task-3/database-systems/blog/python/ddia-distributed-systems/02-leader-follower-replication/_evidence-ledger.md): 이번 재작성에 사용한 근거와 재실행 명령을 기록한다.
- [_structure-outline.md](/Users/woopinbell/work/book-task-3/database-systems/blog/python/ddia-distributed-systems/02-leader-follower-replication/_structure-outline.md): 문서 구조를 왜 이렇게 잡았는지와 탈락시킬 서술을 남긴다.

## 지금 기준의 결론

이 랩은 leader election이나 quorum 없이도 "append-only log + follower watermark"만으로 incremental replication을 설명할 수 있음을 보여준다. 동시에 정확히 그만큼만 한다. follower lag metric, snapshot install, log truncation, consensus는 아직 일부러 비워 두었다.
