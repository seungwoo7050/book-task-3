# 30 다시 돌려 보기: 현재 MVCC가 실제로 보장하는 것

마지막으로 확인할 건 chain 모양과 경계다. MVCC는 말로만 설명하면 쉽게 과장된다. 실제로 어떤 version이 남고, 어떤 version이 지워지고, 어떤 read가 어떤 값을 보는지 다시 확인해야 현재 구현의 크기가 보인다.

## Phase 3-1. pytest는 핵심 visibility 계약은 꽤 잘 잠근다

이번 재실행에서 pytest는 `7 passed, 1 warning in 0.02s`였다. 경고는 앞과 같은 `pytest_asyncio` deprecation이라 핵심과는 무관했다.

테스트가 잠그는 건 이렇다.

- read-your-own-write
- snapshot isolation
- latest committed value
- first-committer-wins conflict
- abort cleanup
- delete tombstone semantics
- GC 이후 chain 축소

즉 이 프로젝트는 "MVCC toy example"로 끝나지 않고, visibility와 cleanup의 최소 contract는 꽤 분명하게 공개한다.

## Phase 3-2. demo는 가장 얇은 public surface만 보여 준다

demo entry point를 다시 돌리면 이런 출력이 나온다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/05-mvcc
PYTHONPATH=src python3 -m mvcc_lab
```

```text
{'tx': 1, 'read_your_own_write': 10}
```

이 한 줄은 snapshot이나 GC까지는 보여 주지 않지만, 이 슬롯의 가장 중요한 예외 규칙 하나를 분명히 드러낸다. "내가 아직 commit하지 않은 write라도 나는 읽을 수 있어야 한다"는 점이다.

## Phase 3-3. 보조 재실행이 conflict cleanup과 aggressive GC를 더 잘 보여 줬다

이번 Todo에서는 테스트 외에도 version chain 모양을 직접 출력해 봤다.

- snapshot read: `v1`
- conflict 후 chain: `[(4, 'a', False)]`
- GC 전 chain: `[(3, 'v3', False), (2, 'v2', False), (1, 'v1', False)]`
- GC 후 chain: `[(3, 'v3', False)]`

이 숫자들이 의미하는 건 분명하다.

1. snapshot은 begin 시점에서 고정된다
2. conflict loser의 version은 abort cleanup으로 사라진다
3. active snapshot이 없으면 GC는 체인을 최신 version 하나 수준까지 줄일 수 있다

즉 현재 MVCC 구현은 version retention을 매우 보수적으로 하지 않는다. long-running reader가 없으면 old versions를 거의 남기지 않는다.

## Phase 3-4. 지금 상태에서 비워 둔 것

- committed set은 bool map일 뿐 commit timestamp separate tracking은 없다
- lock table이 없다
- predicate conflict나 phantom protection이 없다
- distributed tx나 validation phase는 없다
- GC policy가 아주 단순해서 active reader workload를 세밀하게 모델링하지 않는다

그래도 이 프로젝트가 중요한 이유는 분명하다. 앞선 슬롯들이 storage engine의 물리적 경계를 다뤘다면, 여기선 처음으로 "같은 key의 여러 version 중 누가 무엇을 볼 수 있는가"를 명시적인 코드 규칙으로 다룬다. 이후 분산 트랙으로 넘어갈 때도 결국 이 visibility 감각이 바닥이 된다.
