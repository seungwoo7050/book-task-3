# 분산 시스템 완전 가이드

분산 시스템을 처음 읽을 때 가장 흔한 실수는 "서버가 여러 대니까 그냥 복잡한 백엔드"라고 생각하는 것이다. 실제로는 **부분 실패(partial failure)**, **복제(replication)**, **합의된 권한(authority)**, **일관성(consistency)** 문제를 따로 봐야 한다. 이 문서는 `database-systems` Go 분산 트랙을 읽기 전에 그 큰 그림을 먼저 고정하기 위한 가이드다. 이 문서를 읽고 나면 quorum, leader election, partial failure, idempotency가 각각 어떤 문제를 해결하기 위해 존재하는지를 설명할 수 있다.

---

## 1. 먼저 고정할 질문

분산 시스템을 읽을 때는 기능보다 아래 질문 순서가 중요하다.

1. **어디까지가 한 node의 로컬 상태인가?**
2. **그 상태를 다른 node와 어떻게 복제하는가?**
3. **여러 replica 중 어떤 값을 최신이라고 믿을 것인가?**
4. **누가 write authority를 가지는가?**
5. **메시지가 빠지거나 중복될 때 어떻게 수렴하는가?**

이 순서를 거꾸로 읽으면 용어가 섞인다. 예를 들어 leader election은 “누가 쓸 수 있나”의 문제이고, quorum consistency는 “무엇을 최신으로 읽나”의 문제다. 둘 다 분산 시스템이지만 같은 계층의 질문은 아니다.

---

## 2. Partial Failure부터 생각하기

단일 프로세스 안에서는 보통 성공/실패가 한곳에서 보인다. 분산 시스템에서는 일부 node만 죽고, 일부 메시지만 사라지고, 일부 replica만 뒤처질 수 있다.

이 차이가 중요한 이유는 다음과 같다.

- client는 “전체 시스템이 죽었는지”보다 “내 요청 경로 일부가 실패했는지”를 더 자주 겪는다.
- leader는 정상이어도 follower 하나는 lagging replica일 수 있다.
- read는 성공했는데 stale read일 수 있다.
- quorum commit은 성공했는데 모든 follower가 아직 converged하지 않았을 수 있다.

핵심은 **가용성(응답 여부)** 과 **일관성(응답 내용의 최신성)** 을 분리해서 읽는 것이다.
```
단일 프로세스:  성공 OR 실패 (이분법)
분산 시스템:    성공했지만 최신이 아닐 수 있음 (가용성 ≠ 일관성)

대표 상황:
  - write quorum(2/3) 성공 → 3번째 replica는 아직 뒤처짐
  - read quorum(2/3) → 2번째와 3번째 replica에서 응답 → 둘 다 old version
  - 이 경우 read가 성공해도 stale 값을 반환할 수 있음
```
---

## 3. Replication과 Quorum

replication은 로컬 상태를 여러 node에 복사하는 과정이다. 그런데 “복제했다”만으로는 충분하지 않다. 어느 replica가 최신인지, 몇 개 응답이 모이면 성공으로 볼지 정해야 한다.

### 기억할 최소 식

- `N`: 전체 replica 수
- `W`: write를 성공으로 인정하는 최소 ack 수
- `R`: read 시 확인할 replica 수

`W + R > N`이면 read quorum과 write quorum이 반드시 겹친다. 그래서 read quorum 안에 최신 version을 가진 replica가 최소 하나는 포함된다. 반대로 `W + R <= N`이면 stale replica만 보고도 read가 성공할 수 있다.

이 식이 의미하는 것은 “항상 모든 replica가 최신”이 아니라, **read가 최신 write의 흔적을 반드시 한 번은 만난다**는 것이다.

```go
// quorum 겹침 여부를 판단하는 간단한 예시 (Go 스타일)
func quorumOverlaps(n, w, r int) bool {
    return w+r > n
}

// N=3, W=2, R=2 → 2+2=4 > 3 → overlap 보장
// N=3, W=1, R=1 → 1+1=2 ≤ 3 → stale read 가능

// 실제 read 시 가장 높은 version tag를 가진 응답을 선택
type VersionedValue struct {
    Value   string
    Version int64  // logical timestamp 또는 log index
}

func readLatest(responses []VersionedValue) VersionedValue {
    latest := responses[0]
    for _, r := range responses[1:] {
        if r.Version > latest.Version {
            latest = r
        }
    }
    return latest
}
```

### 여기서 자주 헷갈리는 것

| 혼동 | 실제 |
|------|------|
| quorum commit = 모든 replica 동기화 | quorum commit = W개 ack. 나머지는 나중에 catch-up |
| stale read = 네트워크 장애 발생 | stale read = read quorum이 write quorum과 겹치지 않은 것 |
| leader 있으면 consistency 보장 | leader write path에 있어도 read path 설계에 따라 stale 가능 |

---

## 4. Heartbeat와 Leader Election

replication이나 quorum만으로는 “누가 authority를 갖는가”가 해결되지 않는다. 그래서 many-replica 시스템은 보통 leader를 둔다.

leader election을 읽을 때는 아래 네 가지 용어를 먼저 고정하면 된다.

- `heartbeat`: leader가 살아 있음을 알리는 주기적 신호
- `suspicion`: follower가 “leader가 죽었을 수 있다”고 판단한 상태
- `term` 또는 `epoch`: authority 세대를 구분하는 번호
- `majority`: leader 승격을 인정하는 최소 표 수

### split-brain을 막는 최소 규칙

```go
// follower가 선거를 시작하는 조건
func (f *Follower) checkElectionTimeout() {
    if time.Since(f.lastHeartbeat) < f.electionTimeout {
        return  // healthy leader heartbeat 수신 중 → 선거 시작 안 함
    }
    f.startElection()   // timeout → leader가 죽었을 수 있음
}

// candidate가 leader가 되는 조건
func (c *Candidate) collectVotes(peers []Node) bool {
    votes := 1  // 자기 자신에게 vote
    for _, peer := range peers {
        if peer.GrantVote(c.term, c.lastLogIndex) {
            votes++
        }
    }
    return votes > len(peers)/2  // majority 필요
}

// old leader가 더 높은 term을 보면 즉시 step-down
func (l *Leader) handleMessage(msg Message) {
    if msg.Term > l.currentTerm {
        l.currentTerm = msg.Term
        l.stepDown()    // split-brain 방지
    }
}
```

split-brain을 막는 핵심은 **term 단조 증가 + majority vote** 두 가지다. term이 낮은 메시지는 무시하므로 동시에 두 leader가 authority를 주장할 수 없다.

### term과 epoch의 역할

```
term/epoch은 "who was in charge when"을 기록한다.
  - leader_A가 term=5에서 쓴 로그 엔트리는 (term=5, index=42)로 식별
  - leader_B가 term=6에서 당선되면 term=5의 uncommitted 엔트리는 무효
  - follower는 자신의 log에 있는 (term, index)와 새 leader의 것을 비교해
    어디서부터 덮어써야 할지 결정
```

---

## 5. Retry, Duplicate, Idempotency

네트워크는 메시지를 한 번에 정확히 전달해 주지 않는다. 그래서 replication path는 보통 세 가지 실패를 먼저 견뎌야 한다.

- `drop`: 메시지가 아예 사라짐
- `duplicate`: 같은 메시지가 두 번 옴
- `pause`: 한 node로 가는 메시지가 잠시 막힘

이때 핵심은 다음 두 가지다.

- leader는 follower별 진행 위치를 기억하고 retry해야 한다.
- follower는 같은 entry를 두 번 받아도 idempotent하게 처리해야 한다.

즉, **retry가 있으려면 duplicate safety가 먼저 필요하다.**

```go
// leader가 follower별 nextIndex를 추적하며 retry
type ReplicationState struct {
    nextIndex  map[NodeID]int  // 다음에 보낼 log entry index
    matchIndex map[NodeID]int  // 이미 복제 확인된 마지막 index
}

func (r *ReplicationState) sendEntries(followerID NodeID, log []LogEntry) {
    start := r.nextIndex[followerID]
    entries := log[start:]   // follower 진행 위치부터 retry
    // send entries to follower...
}

// follower의 idempotent apply
func (f *Follower) applyEntries(entries []LogEntry, leaderCommit int) {
    for _, entry := range entries {
        if entry.Index <= f.lastApplied {
            continue    // 이미 적용된 entry → 중복이므로 skip
        }
        f.applyToStateMachine(entry)
        f.lastApplied = entry.Index
    }
    // commitIndex 업데이트
    if leaderCommit > f.commitIndex {
        f.commitIndex = min(leaderCommit, f.lastApplied)
    }
}
```

**at-least-once + idempotent apply = exactly-once semantics**: retry로 at-least-once를 보장하고, duplicate skip으로 중복 적용을 막으면 결과적으로 exactly-once 효과를 얻는다.

---

## 6. 이 개념을 현재 워크스페이스에서 읽는 순서

`database-systems` Go 분산 트랙 기준으로는 아래 순서가 가장 자연스럽다.

1. `01-rpc-framing`: 메시지 경계와 transport 감각
2. `02-leader-follower-replication`: append-only log와 follower catch-up
3. `03-shard-routing`: key 공간 분할과 routing
4. `04-raft-lite`: term, vote, majority commit의 최소 합의 모델
5. `05-clustered-kv-capstone`: routing, replication, storage를 한 write path로 묶기
6. `06-quorum-and-consistency`: 어떤 read가 최신을 보장하는가
7. `07-heartbeat-and-leader-election`: 누가 authority를 가지는가
8. `08-failure-injected-log-replication`: partial failure 뒤에 어떻게 수렴하는가

중요한 점은 06, 07, 08이 “더 큰 기능 추가”라기보다, 이미 본 분산 시스템을 **consistency / authority / failure handling** 세 질문으로 다시 분해해서 읽게 해 주는 심화 슬롯이라는 것이다.

---

## 빠른 참조

| 질문 | 먼저 볼 개념 | 핵심 규칙 |
|------|------------|----------|
| 왜 stale read가 생기나? | quorum overlap, `W + R > N` | read quorum이 write quorum과 겹치지 않으면 stale 가능 |
| 누가 leader가 되나? | heartbeat, suspicion, majority, term | majority vote + term 단조 증가 |
| 메시지 유실 뒤 왜 retry가 필요하나? | `nextIndex`, ack, idempotent apply | retry + duplicate skip = exactly-once |
| commit과 convergence는 왜 다른가? | quorum commit vs follower catch-up | W개 ack = commit, 나머지는 나중에 따라옴 |
| split-brain을 어떻게 막나? | term 비교, step-down | 더 높은 term 보면 즉시 step-down |
