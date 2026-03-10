# Leader-Follower Replication — 상태가 아니라 변화를 보내라

## 들어가며

RPC 프레이밍으로 머신 간 통신의 기초를 놓았다면, 이제 그 통신으로 무엇을 할 것인가? 분산 시스템에서 가장 먼저 대면하는 문제는 **데이터 복제(replication)**다. 한 대의 서버가 죽어도 데이터가 살아남으려면, 같은 데이터가 여러 곳에 있어야 한다.

가장 직관적인 복제 방식은 "리더의 전체 상태를 복사하는 것"이다. 하지만 이건 비효율적이다. 키 100만 개 중 하나만 바뀌었는데 100만 개를 다 보낼 수는 없다. 더 근본적인 문제는, 상태 전체를 언제 복사할지 타이밍을 잡기 어렵다는 점이다.

이 프로젝트의 답: **상태를 보내지 말고, 상태를 만든 변화(mutation)를 보내라.** Leader는 모든 쓰기를 append-only log에 기록하고, Follower는 자신이 마지막으로 적용한 지점 이후의 로그만 가져와 재생한다.

## Append-Only Mutation Log

모든 것의 중심은 `ReplicationLog`다. 단순한 슬라이스에 `LogEntry`를 쌓는 것뿐이지만, 이 단순함이 강력하다.

```go
type LogEntry struct {
    Offset    int
    Operation string
    Key       string
    Value     *string
}
```

각 entry에는 순차 offset이 부여된다. offset은 슬라이스의 인덱스 그 자체다—`Append`가 호출될 때 `len(entries)`를 offset으로 사용한다. 이 덕분에 `From(offset)` 메서드는 슬라이스 슬라이싱만으로 O(1)에 원하는 지점부터의 entry를 반환할 수 있다.

```go
func (log *ReplicationLog) From(offset int) []LogEntry {
    if offset >= len(log.entries) {
        return []LogEntry{}
    }
    return append([]LogEntry(nil), log.entries[offset:]...)
}
```

`append([]LogEntry(nil), ...)` 패턴은 RPC framing에서도 봤던 방어적 복사다. 원본 슬라이스를 외부에 노출하지 않는다.

`Value`가 `*string` 포인터인 것도 의도적이다. `put` 연산에는 값이 있지만, `delete` 연산에는 값이 없다. `nil`이 "값 없음"을 자연스럽게 표현한다.

## Leader의 책임

Leader는 두 가지를 동시에 한다: **로컬 상태 적용 + 로그 기록**.

```go
func (leader *Leader) Put(key string, value string) int {
    leader.store[key] = value
    return leader.log.Append("put", key, stringPtr(value))
}

func (leader *Leader) Delete(key string) int {
    delete(leader.store, key)
    return leader.log.Append("delete", key, nil)
}
```

`Put`은 맵에 저장하고 로그에 기록한다. `Delete`은 맵에서 지우고 로그에 기록한다. 반환값은 offset이다—caller가 어디까지 기록됐는지 알 수 있다.

이 설계에서 로그는 "부수적인 기록"이 아니라, 복제의 **유일한 소스**다. Follower는 Leader의 `store` 맵에 직접 접근하지 않는다. 오직 `LogFrom(offset)`을 통해 로그만 받는다.

## Follower와 Watermark

Follower의 핵심 상태는 `lastAppliedOffset`이다. 이것이 **watermark**다. "나는 여기까지 적용했다"를 기억하는 숫자.

```go
func (follower *Follower) Apply(entries []LogEntry) int {
    applied := 0
    for _, entry := range entries {
        if entry.Offset <= follower.lastAppliedOffset {
            continue
        }
        switch entry.Operation {
        case "put":
            if entry.Value != nil {
                follower.store[entry.Key] = *entry.Value
            }
        case "delete":
            delete(follower.store, entry.Key)
        }
        follower.lastAppliedOffset = entry.Offset
        applied++
    }
    return applied
}
```

세 가지가 이 코드에 담겨 있다:

1. **Incremental sync**: `offset <= lastAppliedOffset`인 entry는 건너뛴다. 이미 적용한 것을 다시 적용하지 않는다.

2. **Idempotent apply**: 같은 batch를 두 번 보내도 결과가 같다. 두 번째에는 모든 entry가 skip 조건에 걸리므로 `applied`가 0이 된다. 네트워크 재시도가 안전해진다.

3. **Delete 복제**: delete도 put과 동일한 경로로 처리된다. "키 삭제"라는 사실 자체가 로그 entry로 기록되고, Follower가 그대로 재생한다.

## ReplicateOnce: 복제의 한 사이클

```go
func ReplicateOnce(leader *Leader, follower *Follower) int {
    entries := leader.LogFrom(follower.Watermark() + 1)
    return follower.Apply(entries)
}
```

이 함수 하나가 전체 복제 메커니즘을 요약한다. Follower의 watermark 다음 offset부터 Leader의 로그를 가져오고, Follower에 적용한다. 실제 분산 환경에서는 이 함수를 주기적으로 호출하거나, Leader가 push하는 형태로 만들 것이다.

## 테스트가 증명하는 것들

3개 테스트가 복제의 핵심 속성을 검증한다:

1. **ReplicationLogAssignsSequentialOffsets**: 로그에 append할 때마다 offset이 0, 1, 2, ... 순차 증가
2. **FollowerApplyIsIdempotent**: 같은 entry batch를 두 번 적용해도 두 번째는 0건 적용, 상태 불변
3. **ReplicateOnceIncrementalAndDeletes**: Put → 복제 → Put + Delete → 복제. Follower가 증분만 받고, delete 결과도 반영됨

특히 테스트 2번이 실전에서 중요하다. 네트워크 불안정으로 같은 batch가 재전송되는 상황을 시뮬레이션한다.

## 돌아보며

이 프로젝트는 130줄도 안 되는 코드로 복제의 핵심을 구현한다. 하지만 이 130줄에 들어 있는 아이디어는—log shipping, watermark, idempotent replay—PostgreSQL의 streaming replication, Kafka의 consumer offset, MySQL의 binlog replication에서 똑같이 등장한다.

남은 질문은: 데이터가 많아지면 한 대의 Leader가 모든 쓰기를 감당할 수 있는가? 다음 프로젝트(Shard Routing)에서 이 질문에 답한다.
