# Verification And Boundaries

## 1. 자동 검증은 작지만 방향이 선명하다

2026-03-14 기준으로 아래 명령을 다시 실행했다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication
PYTHONPATH=src python3 -m pytest
```

결과는 아래와 같았다.

```text
3 passed, 1 warning in 0.02s
```

테스트 범위는 세 갈래다.

- sequential offset이 실제로 `0, 1, ...` 순서를 지키는가
- follower가 같은 batch를 두 번 적용할 때 두 번째는 `0`을 돌려주는가
- leader의 추가 write와 delete가 incremental sync 뒤 follower state에 반영되는가

이 테스트 셋은 작지만, 적어도 이 랩의 핵심 질문과 정확히 맞닿아 있다.

## 2. 수동 재실행으로 확인한 관찰

demo와 추가 snippet 재실행 결과는 아래처럼 정리된다.

- demo: `{'applied': 1, 'value': '1'}`
- 첫 full sync: `initial_apply 2 1 {'a': '1', 'b': '2'}`
- 중복 replay: `duplicate_apply 0 1 {'a': '1', 'b': '2'}`
- leader 변경 후 incremental sync: `incremental_apply 2 3 {'b': '3'}`
- 이미 본 batch 재적용: `replay_batch 0 3 {'b': '3'}`

이 관찰을 합치면 현재 구현은 최소한 아래 계약을 만족한다.

- follower는 자신의 watermark 이후 entry만 본다
- delete는 replicated mutation으로 정상 반영된다
- 이미 본 offset 범위는 다시 와도 무시된다

## 3. 하지만 이 랩을 "복제 시스템 완성본"으로 읽으면 안 된다

현재 검증에서 확인되지 않았거나 아예 범위 밖인 항목은 분명하다.

- leader crash 뒤 log durability
- follower가 일부 batch만 받고 중간에서 멈춘 상황
- log truncation이나 snapshot install
- network partition, leader failover, split brain
- commit ack, majority replication, read consistency

즉, 이 랩의 품질 기준은 "분산 시스템의 모든 문제를 다 풀었는가"가 아니라, replication chapter의 첫 번째 발판을 source-first로 분해해 설명했는가에 있어야 한다.

## 4. 이 문서에서 일부러 피한 서술

이번 재작성에서는 아래 같은 표현을 피했다.

- "leader-follower replication을 완성했다"
- "장애 상황에서도 안전하다"
- "eventual consistency를 포괄적으로 검증했다"

현재 소스와 테스트가 보여 주는 사실은 그보다 더 좁고 더 명확하다. ordered mutation stream과 watermark replay의 기본 mechanics를 작은 Python 모델로 재현했다는 것, 그게 전부이자 이 랩의 정확한 강점이다.
