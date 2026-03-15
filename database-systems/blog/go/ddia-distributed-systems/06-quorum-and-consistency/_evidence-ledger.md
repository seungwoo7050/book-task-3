# Evidence Ledger

## Source files used

- `problem/README.md`
  - 이번 단계가 일부러 빼는 범위를 먼저 고정했다.
- `README.md`
  - 검증 명령과 demo surface를 다시 확인했다.
- `docs/concepts/quorum-read-write.md`
  - overlap 공식이 이 구현에서 무엇을 뜻하는지 문장으로 확인했다.
- `docs/concepts/versioned-register.md`
  - single-version register 모델의 단순화 범위를 확인했다.
- `internal/quorum/quorum.go`
  - `Write`, `Read`, `availableReplicas`, `LatestVersion`를 직접 추적했다.
- `tests/quorum_test.go`
  - overlap / stale / version freeze / availability 저하 시나리오를 확인했다.
- `cmd/quorum-demo/main.go`
  - safe/stale 두 시나리오가 어떤 출력으로 드러나는지 다시 확인했다.

## Commands rerun

```bash
GOWORK=off go test ./...
GOWORK=off go run ./cmd/quorum-demo
```

## Key outputs

```text
ok  	study.local/go/ddia-distributed-systems/projects/06-quorum-and-consistency/tests	(cached)
N=3 W=2 R=2 selected=v2:v2 responders=[replica-2=v2:v2, replica-3=v1:v1]
N=3 W=1 R=1 selected=v1:v1 responders=[replica-3=v1:v1]
```

## Manual boundary check

임시 테스트를 추가했다가 제거하고 아래를 기록했다.

```text
replicated=[replica-1 replica-2 replica-3]
responders=replica-2,replica-3
```

이 결과는 write가 `W`개만 쓰는 모델이 아니라 available replica 전체 fanout이라는 점, read responder가 고정 order 기반이라는 점을 실행으로 확인한 것이다.

## Inferences called out explicitly

- read repair 부재는 `Read`가 선택만 하고 어떤 replica도 갱신하지 않는 코드에서 나왔다.
- responder determinism은 `available[:R]` 구현과 위 임시 실행 결과를 함께 근거로 삼았다.
- write quorum failure가 partial write를 남기지 않는다는 점은 `len(available) < W` pre-check와 `TestWriteFailureDoesNotAdvanceVersion`를 함께 보고 판단했다.
