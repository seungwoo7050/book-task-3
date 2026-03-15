# 20 핵심 상태 전이: eager leader apply, quorum commit, idempotent follower retry

이 lab에서 중요한 건 메시지 종류가 세 개라는 사실보다, 어떤 상태가 언제 바뀌는가다. leader는 append 순간 local state를 바꾸고, commit은 ack quorum이 모인 뒤에야 오르며, follower는 duplicate/retry를 idempotent하게 흡수한다.

## Session 1 — leader local state는 commit보다 먼저 바뀐다

가장 먼저 눈에 들어와야 하는 함수는 `AppendPut`다.

```go
func (leader *Leader) AppendPut(key string, value string) LogEntry {
	entry := LogEntry{
		Index:     len(leader.log),
		Operation: "put",
		Key:       key,
		Value:     stringPtr(value),
	}
	leader.log = append(leader.log, entry)
	leader.store[key] = value
	return entry
}
```

여기서는 commit을 기다리지 않는다. log append와 동시에 leader local store가 바뀐다. 임시 검증에서도 양쪽 follower append를 모두 drop한 뒤 `commit=-1 leader_read=true:1`이 나왔다. 즉 이 구현에서 leader read visibility는 quorum commit과 분리돼 있다.

이 점을 문서에 남겨야 하는 이유는, commit index를 "누구나 읽어도 되는 시점"으로 혼동하기 쉽기 때문이다. 이 lab에서 commit은 majority replication 진척을 뜻할 뿐, leader local apply와 같은 사건은 아니다.

## Session 2 — quorum commit은 lagging follower를 그냥 남겨 둘 수 있다

leader 쪽 quorum 계산은 `advanceCommit()`에 있다.

```go
func (leader *Leader) advanceCommit() {
	for index := len(leader.log) - 1; index > leader.commitIndex; index-- {
		replicated := 1
		for _, matchIndex := range leader.matchIndex {
			if matchIndex >= index {
				replicated++
			}
		}
		if replicated >= majority(len(leader.matchIndex)+1) {
			leader.commitIndex = index
			return
		}
	}
}
```

leader 자신이 이미 `1표`로 들어가고, follower 둘 중 하나만 ack해도 majority가 된다. 그래서 demo 첫 줄의 `drop tick commit=0 node-2=-1 node-3=0`이 가능하다. `node-2`는 완전히 lagging인데도 commit은 이미 0으로 올라간다.

이게 바로 docs의 `quorum-commit-and-retry.md`가 말하는 핵심이다. commit은 "성공으로 인정할 수 있는가"의 질문이고, convergence는 "뒤처진 follower가 결국 따라오는가"의 질문이다.

## Session 3 — duplicate와 retry는 follower idempotency 위에서 성립한다

follower 쪽 핵심은 `HandleAppend`다.

```go
func (follower *Follower) HandleAppend(entry LogEntry) int {
	if entry.Index < len(follower.log) {
		if equalEntry(follower.log[entry.Index], entry) {
			return follower.Watermark()
		}
		follower.log = append([]LogEntry(nil), follower.log[:entry.Index]...)
		follower.rebuildStore()
	}
	if entry.Index > len(follower.log) {
		return follower.Watermark()
	}
	if entry.Index == len(follower.log) {
		follower.log = append(follower.log, entry)
		follower.apply(entry)
	}
	return follower.Watermark()
}
```

여기서 세 갈래가 중요하다.

- 같은 index에 같은 entry가 오면 watermark만 돌려주고 끝낸다.
- 더 작은 index에 다른 entry가 오면 suffix를 자르고 store를 rebuild한다.
- 너무 앞선 index가 오면 현재 watermark만 돌려준다.

이 덕분에 duplicate delivery는 `log length`와 `appliedCount`를 두 번 늘리지 않고, lagging follower는 `nextIndex` 기반 retry로 결국 수렴한다. demo의 `duplicate tick commit=1 node-3-log=2 node-3-applied=2`는 index 1 entry가 중복 전달돼도 follower가 총 두 entry만 가진다는 사실을 보여 준다.
