# Scope, Surface, And First Ordered Output

## 1. 문제는 자료구조 일반론보다 MemTable semantics를 고정하는 쪽에 있다

[`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/01-memtable-skiplist/problem/README.md)는 다섯 가지를 요구한다. ordered `Put`, 상태를 구분하는 `Get`, tombstone 기반 `Delete`, 전체 ordered iteration, 그리고 flush threshold 판단용 byte-size tracking이다.

중요한 건 일부러 빠진 범위다. 동시성 제어, lock-free 구현, 확률적 tuning, benchmark는 다루지 않는다. 즉 이 랩은 skip list를 최고 성능으로 만드는 단계가 아니라, 저장 엔진이 기대하는 MemTable contract를 작게 고정하는 단계다.

## 2. 코드 표면은 단순하지만 의도가 분명하다

핵심 구현은 [`skiplist.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/01-memtable-skiplist/internal/skiplist/skiplist.go) 하나에 모여 있다.

- `Put(key, value)`
- `Delete(key)`
- `Get(key) (string, ValueState)`
- `Entries() []Entry`
- `Size() int`
- `ByteSize() int`
- `Clear()`

이 표면을 보면 곧바로 알 수 있다. API는 range query나 iterator abstraction보다 "flush 직전 상태를 어떻게 읽을 것인가"에 맞춰져 있다. 실제로 docs의 [`skiplist-invariants.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/01-memtable-skiplist/docs/concepts/skiplist-invariants.md)도 level-0 ordered list, tombstone 유지, byte-size 근사치를 핵심 invariant로 잡는다.

## 3. deterministic level generation을 일부러 택했다

`New()`는 `rand.New(rand.NewSource(7))`로 고정 시드를 만든다. 즉 이 skip list는 완전히 무작위인 production structure라기보다, 테스트와 학습 설명에서 재현 가능한 level 배치를 택한다.

이 선택 덕분에 자료구조 내부는 여전히 probabilistic shape를 쓰지만, 테스트와 demo는 매번 같은 이야기로 반복된다. 학습용 repo에서 꽤 중요한 선택이다.

## 4. demo 출력이 보여 주는 첫 사실

2026-03-14에 아래 명령을 다시 실행했다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/01-memtable-skiplist
GOWORK=off go run ./cmd/skiplist-demo
```

출력은 아래와 같았다.

```text
ordered entries:
- apple => green
- banana => <tombstone>
- carrot => orange
size=3 byteSize=220
```

이 출력만으로도 세 가지가 보인다.

- insertion 순서와 무관하게 iteration은 key 오름차순이다
- delete된 `banana`는 사라지지 않고 tombstone으로 남는다
- tombstone도 logical size에 포함되며 byte size 추적도 함께 갱신된다

즉 demo는 "skip list가 동작한다"보다 "flush 직전에 어떤 ordered view가 손에 남는가"를 보여 주는 데 더 가깝다.
