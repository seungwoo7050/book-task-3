# 10 범위를 다시 좁히기: 이 슬롯의 중심은 저장이 아니라 가시성 규칙이다

이전 슬롯들까지는 bytes, pages, eviction, filters처럼 눈에 보이는 비용 문제가 중심이었다. 그런데 `05 MVCC`는 질문 자체가 바뀐다. 여기서 중요한 건 "어디에 저장되는가"가 아니라 "누가 어떤 version을 볼 수 있는가"다.

## Phase 1. 테스트가 이미 네 가지 규칙을 분리해서 잠근다

`tests/test_mvcc.py`를 다시 훑어 보면 이 프로젝트의 범위가 꽤 명확하게 나뉜다.

- 기본 read/write와 read-your-own-write
- snapshot isolation
- latest committed value
- write-write conflict
- abort/delete cleanup
- GC

즉 이 슬롯은 generic transaction manager가 아니다. snapshot isolation에 필요한 최소 규칙 집합을 deliberately small하게 구현한다. predicate locking, phantom, distributed transaction은 일부러 빼고, version chain과 committed watermark만으로 설명 가능한 경계만 남긴다.

이번 재실행:

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/05-mvcc
PYTHONPATH=src python3 -m pytest
```

결과:

```text
7 passed, 1 warning in 0.02s
```

## Phase 2. 문제 정의가 "트랜잭션 전체"가 아니라 snapshot isolation core로 범위를 자른다

`problem/README.md`를 다시 보면 이 프로젝트가 일부러 뺀 것도 분명하다.

- predicate locking 없음
- phantom read 제어 없음
- distributed transaction 없음
- full SQL lock table 없음

이건 오히려 장점이다. 덕분에 지금 이 슬롯의 핵심이 어디인지 흐려지지 않는다. transaction은 결국 세 가지를 잘해야 한다.

1. 시작 시점의 snapshot을 정한다
2. 내 write는 내가 바로 본다
3. 같은 key에 대해 뒤늦은 commit은 막는다

이 세 가지가 곧 이 프로젝트의 중심이다.
