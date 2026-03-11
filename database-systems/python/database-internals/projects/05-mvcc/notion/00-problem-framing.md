# 문제 프레이밍

## 왜 이 프로젝트를 하는가
01~04 단계까지는 현재 값 중심의 저장 구조를 다뤘다면, 여기서는 같은 key를 서로 다른 트랜잭션이 서로 다른 시점에서 어떻게 보느냐를 다룹니다. 목표는 production-grade MVCC를 만드는 것이 아니라 snapshot isolation의 핵심 규칙을 직접 구현하고 테스트로 재현하는 것입니다.

## 커리큘럼 안에서의 위치
- 트랙: Database Internals / Python
- 이전 단계: 04 Buffer Pool
- 다음 단계: 이 트랙의 마지막 프로젝트
- 지금 답하려는 질문: 같은 key에 대해 여러 transaction이 겹칠 때, 누가 어떤 version을 볼 수 있고 어떤 commit은 거절되어야 하는가?

## 이번 재현에서 먼저 고정할 시나리오
### 시나리오 1. read-your-own-write
- 트랜잭션 하나가 `x=10`을 쓴 직후 같은 트랜잭션에서 `x`를 읽으면 10이 보여야 합니다.
- 데모 기대 출력: `{'tx': 1, 'read_your_own_write': 10}`

### 시나리오 2. snapshot isolation
- `t1`이 `x=100`을 commit합니다.
- `t2`가 시작한 뒤 `t3`가 `x=200`을 commit해도 `t2`는 여전히 100을 읽어야 합니다.

### 시나리오 3. write-write conflict
- `t1`과 `t2`가 둘 다 `x`를 수정합니다.
- `t1`이 먼저 commit하면 `t2` commit은 `write-write conflict`로 실패해야 합니다.

### 시나리오 4. GC
- `v1`, `v2`, `v3`가 차례로 쌓인 뒤 GC를 수행합니다.
- 최신 읽기 결과는 유지하면서 version chain 길이는 줄어야 합니다.

## 이번 구현에서 성공으로 보는 것
- key별 version chain이 tx_id 내림차순으로 유지되어야 합니다.
- `begin()` 시점에 snapshot이 고정되어 이후 commit이 바로 보이지 않아야 합니다.
- `read()`가 read-your-own-write를 먼저 처리한 뒤 visible version을 찾아야 합니다.
- `commit()`이 first-committer-wins 충돌 검사를 해야 합니다.
- `abort()`가 자신의 version을 제거하고, `gc()`가 오래된 version을 정리해야 합니다.

## 먼저 열어 둘 파일
- `../src/mvcc_lab/core.py`: version chain, snapshot visibility, commit/abort/GC가 한 파일 안에서 어떻게 이어지는지 확인합니다.
- `../src/mvcc_lab/__main__.py`: read-your-own-write 경로를 가장 짧은 출력으로 보여 주는 데모 진입점입니다.
- `../tests/test_mvcc.py`: snapshot isolation, conflict, abort, GC 시나리오를 직접 검증합니다.
- `../docs/concepts/snapshot-visibility.md`: visible version 선택 규칙을 먼저 복기할 때 좋습니다.

## 의도적으로 남겨 둔 범위 밖 항목
- predicate read, phantom 방지, lock manager는 다루지 않습니다.
- disk persistence, WAL, index integration도 이 프로젝트에서는 다루지 않습니다.
- write skew, serializable isolation 같은 더 강한 격리 수준은 범위 밖입니다.

## 데모에서 바로 확인할 장면
- `PYTHONPATH=src python -m mvcc_lab`를 실행했을 때 `{'tx': 1, 'read_your_own_write': 10}` 한 줄이 나오면 기본 가시성 경로는 맞습니다.
