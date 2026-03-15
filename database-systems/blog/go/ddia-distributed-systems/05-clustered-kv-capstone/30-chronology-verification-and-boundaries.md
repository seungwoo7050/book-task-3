# 30 검증과 경계: 무엇이 확인됐고 무엇은 아직 없다

이번 Todo에서는 테스트 pass 숫자만 적지 않고, 실제 출력과 on-disk 흔적이 무엇을 말해 주는지까지 같이 남겼다. 이 project는 분산 시스템이라는 이름을 달고 있지만, 검증 신호는 의외로 로컬하고 구체적이다.

## Session 1 — 재실행 결과

다시 실행한 명령과 결과는 아래와 같다.

```bash
$ GOWORK=off go test ./...
?   	study.local/go/ddia-distributed-systems/projects/05-clustered-kv-capstone/cmd/clustered-kv	[no test files]
?   	study.local/go/ddia-distributed-systems/projects/05-clustered-kv-capstone/internal/capstone	[no test files]
ok  	study.local/go/ddia-distributed-systems/projects/05-clustered-kv-capstone/tests	(cached)
```

```bash
$ rm -rf .demo-data && GOWORK=off go run ./cmd/clustered-kv
key=alpha shard=shard-a follower=node-2 value=1 ok=true
```

이 출력이 확인해 주는 사실은 생각보다 명확하다.

- `alpha`는 실제로 `shard-a`로 라우팅된다.
- leader write 뒤 follower `node-2`가 같은 값을 읽을 수 있다.
- demo 수준에서도 replication 결과가 공개 표면으로 드러난다.

여기서도 표현을 조금 더 줄여야 한다. demo가 follower visibility를 보여 주는 건 일반 `Read()`가 follower에 fan-out 하기 때문이 아니라, `cmd/clustered-kv/main.go`가 `group.Followers[0]`에 대해 `ReadFromNode(...)`를 명시적으로 호출하기 때문이다. 즉 ordinary read path는 여전히 leader 기준이고, stale follower나 replicated follower 상태를 보는 건 의도적으로 debug-style surface를 열었을 때만 가능하다.

## Session 2 — demo가 남긴 파일이 더 직접적인 증거가 되는 부분

demo 실행 뒤 `.demo-data`를 직접 보면 routing과 replication이 파일 레벨에서도 보인다.

```bash
$ find .demo-data -type f | sort
.demo-data/node-1/shard-a.log
.demo-data/node-2/shard-a.log
.demo-data/node-2/shard-b.log
.demo-data/node-3/shard-b.log
```

```bash
$ sed -n '1,20p' .demo-data/node-1/shard-a.log
{"offset":0,"type":"put","key":"alpha","value":"1"}

$ sed -n '1,20p' .demo-data/node-2/shard-a.log
{"offset":0,"type":"put","key":"alpha","value":"1"}
```

같은 entry가 leader와 follower 양쪽 log에 남아 있다는 점이 중요하다. 반면 `shard-b` 쪽 파일은 비어 있으므로, demo는 "두 shard 전체"가 아니라 하나의 routed write만 보여 준다. 이것도 좋은 경계 신호다. demo가 작기 때문에 오히려 무엇을 아직 보여 주지 않는지 분명하다.

## Session 3 — 현재 한계

이번 Todo에서 최종적으로 남긴 경계는 다음과 같다.

- topology는 초기화 시점에 고정된다. shard 추가/삭제, membership change가 없다.
- follower sync는 직접 `SyncFollower`를 호출하는 방식이며, background replication worker가 없다.
- restart는 local log replay일 뿐이다. lagging follower는 restart만으로 최신 상태가 되지 않는다.
- default `Read`는 leader를 읽기 때문에, follower freshness 문제는 `ReadFromNode`를 일부러 호출할 때만 표면에 올라온다.
- transport, timeout, quorum, leader election, split-brain handling이 없다.
- read surface는 `Read`와 `ReadFromNode` 두 메서드뿐이며, stale follower read를 막는 안전장치가 없다.

그래서 이 project는 "작은 production cluster"가 아니라 "분산 저장 경로의 최소 통합본"으로 읽는 편이 맞다. routing, append-only log, follower catch-up, restart replay가 한 경로에서 만나는 감각을 익히는 것이 이 capstone의 실제 목적이다.
