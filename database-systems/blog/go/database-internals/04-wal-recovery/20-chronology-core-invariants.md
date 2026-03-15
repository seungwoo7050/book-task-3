# Core Invariants

## 1. append-before-apply는 store 메서드의 첫 줄에서 보장된다

`DurableStore.Put()`과 `Delete()`는 둘 다 memtable 전에 WAL을 먼저 쓴다.

```go
if err := store.writeAheadLog.AppendPut(key, value); err != nil {
    return err
}
store.Memtable.Put(key, value)
```

```go
if err := store.writeAheadLog.AppendDelete(key); err != nil {
    return err
}
store.Memtable.Delete(key)
```

즉 acknowledged write가 memtable에만 존재하는 상태를 만들지 않겠다는 계약이 분명하다. 이 랩의 durability는 바로 이 순서에서 시작한다.

## 2. WAL record format은 `[crc32][type][keyLen][valLen][key][value]`다

docs의 [`wal-record-format.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery/docs/concepts/wal-record-format.md)가 말하는 형식은 소스와 정확히 맞는다.

- CRC32 4바이트
- type 1바이트
- key length 4바이트
- value length 4바이트
- key bytes
- value bytes

delete는 shared serializer의 `TombstoneMarker`를 `valLen`에 넣어 표현한다. payload CRC는 type부터 value bytes까지 전체 payload에 대해 계산된다. 즉 replay 중 길이와 무결성을 동시에 검증할 수 있다.

## 3. replay는 첫 손상 지점에서 멈춘다

`Recover()`는 세 가지 상황에서 즉시 loop를 멈춘다.

- header가 13바이트보다 짧을 때
- payload 전체 길이가 부족할 때
- CRC mismatch가 날 때

여기서 중요한 건 "에러를 반환하지 않고 stop한다"는 점이다. docs의 [`recovery-policy.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery/docs/concepts/recovery-policy.md)가 설명하는 stop-on-corruption 정책이 그대로 구현돼 있다.

즉 손상 이전까지의 레코드는 살리고, 그 뒤쪽 bytes는 신뢰하지 않는다.

## 4. reopen recovery는 SSTable 복원 다음, WAL replay 다음, active WAL reopen 순서다

`Open()`의 순서는 꽤 중요하다.

1. `.sst` 파일을 읽어 index를 적재한다
2. 기존 `active.wal`을 `Recover()`로 읽어 memtable에 반영한다
3. 새 `writeAheadLog.Open()`으로 active append handle을 연다

즉 reopen 뒤 store는 "이전 disk snapshot + 이전 active WAL replay + 새 append handle"의 조합으로 시작한다. SSTable만으로는 최근 write를 잃을 수 있으니, WAL replay가 반드시 그 뒤를 메운다.

## 5. flush는 WAL을 닫고 지운 뒤 새 empty WAL을 연다

`ForceFlush()`는 memtable 내용을 SSTable로 내린 뒤 아래 순서를 따른다.

1. 기존 WAL close
2. `active.wal` 삭제
3. memtable clear
4. 같은 경로에 새 WAL 인스턴스 생성
5. 새 handle open

그래서 추가 재실행에서도 `wal_size_after_flush 0`이 나왔다. flush 이후 active WAL은 과거 replay 기록이 아니라 다음 write를 받는 빈 파일이 된다.
