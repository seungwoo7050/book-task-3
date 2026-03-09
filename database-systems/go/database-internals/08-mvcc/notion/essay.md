# MVCC — 잠금 없이 동시성을 얻는 법

## 들어가며

데이터베이스 내부 구조를 탐구하는 여정의 마지막 프로젝트다. 지금까지 SkipList로 메모리 쓰기를, SSTable로 디스크 영속화를, LSM Store로 그 둘을 조합했고, WAL로 장애 복구를, 컴팩션으로 디스크 정리를, 블룸 필터와 희소 인덱스로 읽기 최적화를, 버퍼 풀로 페이지 캐싱을 구현했다. 남은 질문은 하나다: **여러 트랜잭션이 동시에 같은 데이터를 읽고 쓸 때, 어떻게 일관성을 유지하는가?**

전통적 답은 잠금(lock)이다. 읽는 동안 쓰지 못하게, 쓰는 동안 읽지 못하게. 하지만 이 전략은 동시성을 심하게 제한한다. PostgreSQL이 선택한 답, 그리고 이 프로젝트에서 구현하는 답은 MVCC(Multi-Version Concurrency Control)다. 데이터의 여러 버전을 동시에 유지함으로써, 읽기와 쓰기가 서로 차단하지 않는 세계를 만든다.

## 스냅샷이라는 개념

MVCC의 핵심 아이디어는 간단하다. 트랜잭션이 시작되는 순간, 데이터베이스의 "사진"을 찍는다. 이 사진이 스냅샷(snapshot)이다. 트랜잭션은 이 사진 속의 세계만 보고, 이후에 다른 트랜잭션이 무엇을 바꾸든 관여하지 않는다.

구현에서 스냅샷은 숫자 하나다. `Begin()`이 호출될 때, 현재까지 커밋된 트랜잭션 중 가장 큰 ID를 기록한다. 이 숫자가 그 트랜잭션의 "시야 한계선"이 된다.

```go
maxCommitted := 0
for id := range manager.Committed {
    if id > maxCommitted {
        maxCommitted = id
    }
}
manager.Transactions[txID] = &Transaction{
    Snapshot: maxCommitted,
    Status:   txActive,
    WriteSet: map[string]bool{},
}
```

이 코드가 말하는 것: "나는 txID=maxCommitted까지의 세계만 보겠다."

## 버전 체인의 설계

하나의 키에 여러 값이 공존할 수 있으려면, 값을 덮어쓰는 대신 **쌓아야** 한다. `VersionStore`는 키마다 `[]Version` 슬라이스를 유지한다. 각 Version에는 값, 그것을 쓴 트랜잭션 ID, 삭제 여부가 담긴다.

새로운 버전을 추가할 때 단순히 append하지 않는다. TxID 내림차순으로 삽입 정렬한다. 가장 최근 버전이 슬라이스 앞에 온다. 이렇게 하면 `GetVisible`에서 체인을 앞에서부터 순회하다 스냅샷 조건을 만족하는 첫 버전을 반환하면 되기 때문이다.

```go
func (store *VersionStore) Append(key string, value any, txID int, deleted bool) {
    chain := store.Store[key]
    index := 0
    for index < len(chain) && chain[index].TxID > txID {
        index++
    }
    chain = append(chain, Version{})
    copy(chain[index+1:], chain[index:])
    chain[index] = Version{Value: value, TxID: txID, Deleted: deleted}
    store.Store[key] = chain
}
```

삽입 정렬이라는 선택이 흥미롭다. 대부분의 경우 새 트랜잭션의 ID가 가장 크므로 `index`는 0이 되고, 실질적으로 맨 앞에 삽입된다. O(1)에 가까운 연산이다.

## 읽기: 보이는 것과 보이지 않는 것

`Read`는 두 가지 경로를 탄다.

**자기 자신의 쓰기(Read-Your-Own-Writes)**: 내가 이 트랜잭션에서 쓴 키라면, 내 TxID로 쓴 버전을 직접 찾는다. 아직 커밋되지 않았지만, 나 자신이 쓴 것이니까 보여야 한다.

**스냅샷 기반 읽기**: 자기가 쓴 게 아니라면, `GetVisible`을 통해 스냅샷 이하이면서 커밋된 버전 중 가장 최신을 반환한다.

```go
func (store *VersionStore) GetVisible(key string, snapshot int, committed map[int]bool) *Version {
    chain := store.Store[key]
    for _, version := range chain {
        if version.TxID <= snapshot && committed[version.TxID] {
            copyVersion := version
            return &copyVersion
        }
    }
    return nil
}
```

체인이 TxID 내림차순이므로 조건을 만족하는 첫 번째가 곧 "스냅샷 시점의 최신 커밋 값"이다. 한 가지 세심한 부분: 반환 시 `copyVersion := version`으로 복사본을 만든다. 포인터로 원본을 넘기면 외부에서 수정할 수 있기 때문이다.

## 쓰기와 삭제

`Write`와 `Delete`는 구조가 동일하다. 버전 체인에 새 Version을 추가하고, 해당 키를 트랜잭션의 WriteSet에 기록한다. 차이는 `Deleted` 플래그뿐이다.

```go
func (manager *TransactionManager) Write(txID int, key string, value any) {
    tx := manager.activeTx(txID)
    manager.VersionStore.Append(key, value, txID, false)
    tx.WriteSet[key] = true
}
```

WriteSet은 나중에 두 곳에서 쓰인다: 커밋 시 충돌 감지와, abort 시 롤백.

## First-Committer-Wins: 충돌의 판정

두 트랜잭션이 동시에 같은 키를 쓸 때, 누가 이기는가? 이 프로젝트는 "먼저 커밋한 쪽이 이긴다"(First-Committer-Wins)를 선택한다.

커밋 시점에 WriteSet의 모든 키를 검사한다. 내 스냅샷 이후에 다른 트랜잭션이 그 키를 커밋했는가? 그렇다면 내 쓰기는 "stale snapshot 위에 쓴 것"이므로 충돌이다.

```go
func (manager *TransactionManager) Commit(txID int) error {
    tx := manager.activeTx(txID)
    for key := range tx.WriteSet {
        for _, version := range manager.VersionStore.Store[key] {
            if version.TxID > tx.Snapshot && version.TxID != txID && manager.Committed[version.TxID] {
                manager.abortInternal(txID, tx)
                return fmt.Errorf("write-write conflict on key %q", key)
            }
        }
    }
    tx.Status = txCommitted
    manager.Committed[txID] = true
    return nil
}
```

충돌이 감지되면 해당 트랜잭션을 자동으로 abort한다. abort는 WriteSet의 모든 키에 대해 이 트랜잭션이 쓴 버전을 체인에서 **물리적으로 제거**한다. 커밋되지 않은 쓰레기가 체인에 남지 않도록.

## 가비지 컬렉션

버전이 계속 쌓이면 메모리가 바닥난다. `GC()`는 현재 활성 트랜잭션 중 가장 낮은 스냅샷을 찾고, 그 시점보다 오래된 버전들 중 **가장 최신 하나만** 남기고 나머지를 버린다.

```go
func (store *VersionStore) GC(minSnapshot int) {
    for key, chain := range store.Store {
        recent := []Version{}
        old := []Version{}
        for _, version := range chain {
            if version.TxID >= minSnapshot {
                recent = append(recent, version)
            } else {
                old = append(old, version)
            }
        }
        if len(old) > 0 {
            recent = append(recent, old[0])
        }
        // ...
    }
}
```

왜 하나를 남기는가? 아직 활성 중인 트랜잭션의 스냅샷이 그 시점 근처를 가리킬 수 있기 때문이다. 완전히 버리면 해당 트랜잭션의 읽기가 깨진다. old[0]은 체인이 내림차순이므로 "오래된 것 중 가장 최신", 즉 스냅샷 직전의 마지막 유효 값이다.

## 테스트가 증명하는 불변식들

7개 테스트가 MVCC의 핵심 불변식을 하나씩 검증한다:

1. **BasicReadWrite**: read-your-own-writes와 missing key에 대한 nil 반환
2. **SnapshotIsolation**: 다른 트랜잭션이 커밋한 변경이 내 스냅샷에 보이지 않음
3. **LatestCommittedValue**: 순차 커밋 후 최신 값이 제대로 보이는지
4. **WriteWriteConflict**: 같은 키에 대한 동시 쓰기 → 후커밋자 실패
5. **DifferentKeysNoConflict**: 다른 키 쓰기는 충돌하지 않음
6. **AbortAndDelete**: abort 시 쓰기 롤백, delete 후 nil 반환
7. **GC**: 가비지 컬렉션 후에도 최신 값 유지, 체인 길이 감소 확인

## 돌아보며

MVCC의 구현은 생각보다 작다. 200줄 남짓. 하지만 이 200줄에 데이터베이스 동시성 제어의 핵심 아이디어가 모두 들어 있다. 잠금 없이 격리를 달성하는 스냅샷, 쓰기 충돌을 뒤늦게 발견하는 optimistic concurrency control, 그리고 무한 증식을 막는 GC.

이 시리즈의 8개 프로젝트를 모두 거치면서, 하나의 키-값 데이터베이스 엔진이 필요로 하는 거의 모든 핵심 구성요소를 구현한 셈이다. SkipList → SSTable → LSM → WAL → Compaction → Index/Filter → Buffer Pool → MVCC. 각각은 독립적인 문제처럼 보이지만, 결국 하나의 시스템을 이루는 층위들이다.
