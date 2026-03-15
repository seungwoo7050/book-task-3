# 30 검증과 경계: 공식은 맞지만 구현은 더 작다

이번 Todo에서는 공식 설명보다 실행 신호를 더 중시했다. `W + R > N`이 맞다는 말을 반복하는 대신, 테스트와 demo가 실제로 어떤 responder 집합과 어떤 version 선택을 보여 주는지 다시 확인했다.

## Session 1 — 재실행 결과

```bash
$ GOWORK=off go test ./...
?   	study.local/go/ddia-distributed-systems/projects/06-quorum-and-consistency/cmd/quorum-demo	[no test files]
?   	study.local/go/ddia-distributed-systems/projects/06-quorum-and-consistency/internal/quorum	[no test files]
ok  	study.local/go/ddia-distributed-systems/projects/06-quorum-and-consistency/tests	(cached)
```

```bash
$ GOWORK=off go run ./cmd/quorum-demo
N=3 W=2 R=2 selected=v2:v2 responders=[replica-2=v2:v2, replica-3=v1:v1]
N=3 W=1 R=1 selected=v1:v1 responders=[replica-3=v1:v1]
```

첫 줄은 read quorum 안에 stale responder가 하나 있어도 latest version을 고른다는 걸 보여 준다. 둘째 줄은 stale responder만 읽어도 read가 성공할 수 있음을 그대로 보여 준다. 이 대비가 project의 핵심 검증 신호다.

## Session 2 — 추가로 확인한 구현 경계

임시 테스트를 넣었다가 제거하면서 두 가지를 더 확인했다.

```text
replicated=[replica-1 replica-2 replica-3]
responders=replica-2,replica-3
```

이 결과가 뜻하는 것은 다음과 같다.

- successful write는 `W`개까지만 쓰는 게 아니라 살아 있는 replica 전부에 fanout한다.
- read quorum은 "아무 R개"가 아니라 replica order 기준 첫 `R`개다.

즉 공식 자체는 quorum theory를 따르지만, 구현 모델은 교육용으로 더 결정적이고 단순하다.

## Session 3 — 이번 Todo에서 남긴 한계

- write quorum failure는 partial replicate 뒤 rollback하는 모델이 아니다. `available < W`면 mutation 전에 바로 실패한다.
- read repair가 없어서 stale replica는 read만으로 최신화되지 않는다.
- hinted handoff, sloppy quorum, anti-entropy가 없어 write/read 이후 background healing이 없다.
- single-version register만 다루므로 concurrent write conflict를 표현하지 못한다.
- multi-key invariant가 없어서 transaction이나 atomic batch를 설명할 수 없다.
- replica health는 수동 `DownReplica/UpReplica` 토글이며 failure detector가 없다.

그래서 이 project는 "quorum storage engine"이 아니라 "quorum overlap이 읽기 결과를 어떻게 바꾸는지 보여 주는 최소 모델"로 읽는 편이 정확하다.
