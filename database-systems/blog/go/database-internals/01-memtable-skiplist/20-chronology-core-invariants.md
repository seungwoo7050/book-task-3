# Core Invariants

## 1. level 0 ordered list가 진짜 source of truth다

구현에서 상위 level은 shortcut일 뿐이고, `Entries()`는 언제나 `header.forward[0]`부터 순회한다.

```go
current := s.header.forward[0]
for current != nil {
    entries = append(entries, Entry{Key: current.key, Value: current.value})
    current = current.forward[0]
}
```

즉 실제 ordered view는 level 0에 있다. 상위 level이 어떻게 생겼든, flush나 scan에 쓰일 결과는 결국 level 0 전체 순회로 회수된다.

## 2. delete는 remove가 아니라 value=nil인 update다

`Delete(key)`는 노드를 삭제하지 않는다. 내부적으로 그냥 `put(key, nil)`을 호출한다.

```go
func (s *SkipList) Delete(key string) {
    s.put(key, nil)
}
```

이 선택 때문에 `Get()`은 세 상태를 구분할 수 있다.

- `Missing`
- `Present`
- `Tombstone`

테스트 [`TestDeleteProducesTombstone`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/01-memtable-skiplist/tests/skiplist_test.go)도 삭제 뒤 `Size()==1`이 유지되는지를 함께 본다. 즉 delete는 record removal이 아니라 deletion intent 보존이다.

## 3. update는 logical size를 늘리지 않고 byte size만 조정한다

키가 이미 존재하면 `put()`은 새 노드를 만들지 않는다. 대신 현재 노드의 `value`만 바꾸고 byte-size 차이만 더한다.

```go
if current != nil && current.key == key {
    s.byteSize += valueLen(value) - valueLen(current.value)
    current.value = value
    return
}
```

그래서 update는 `Size()`를 늘리지 않는다. 테스트 [`TestUpdateKeepsLogicalSize`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/01-memtable-skiplist/tests/skiplist_test.go)가 바로 이 계약을 잡는다. 이건 나중에 flush threshold를 entry count가 아니라 memory usage 관점에서 보게 해 주는 바닥이다.

## 4. byte size는 정확한 allocator accounting이 아니라 flush 근사치다

새 노드를 넣을 때는 `len(key) + valueLen(value) + nodeOverhead`를 더한다. `nodeOverhead`는 상수 `64`다.

즉 `ByteSize()`는 실제 Go heap usage를 재는 게 아니라 flush threshold 판단에 쓸 근사치다. docs도 이 점을 분명히 말한다. 그래서 demo의 `byteSize=220`은 "정확히 220 bytes 사용"이 아니라 "현재 memtable이 대략 이 정도 비용으로 커졌다"는 신호로 읽어야 한다.

## 5. deterministic random level은 테스트 편의가 아니라 설명 품질에도 기여한다

`randomLevel()`은 확률 `0.5`로 level을 높이되, RNG 자체는 seed `7`로 고정돼 있다. 이 덕분에 삽입 패턴이 재현 가능하고, ordered semantics 설명이 실행마다 달라지지 않는다. 이 랩은 performance randomness보다 source-first 설명 가능성을 우선한 셈이다.
