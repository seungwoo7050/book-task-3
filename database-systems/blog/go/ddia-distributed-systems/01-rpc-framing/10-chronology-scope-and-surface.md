# Scope, Transport Surface, And First Round Trip

## 1. 문제 범위는 transport semantics에만 집중한다

[`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/01-rpc-framing/problem/README.md)는 length-prefixed framing, split/multi-frame decode, pending call map, unknown method/handler error/timeout/disconnect 전파를 요구한다. TLS, auth, streaming RPC, service discovery, load balancing은 뺀다.

즉 이 랩은 분산 시스템의 business protocol 이전 단계, 곧 "request/response를 안전하게 주고받는 최소 껍데기"에만 집중한다.

## 2. 코드 표면은 framing과 RPC 두 층으로 나뉜다

핵심 구현은 두 파일에 나뉜다.

- [`framing.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/01-rpc-framing/internal/framing/framing.go): length-prefixed encode/decode
- [`rpc.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/01-rpc-framing/internal/rpc/rpc.go): server dispatch, client pending map, call lifecycle

이 분리 덕분에 "byte stream에서 frame을 복구하는 일"과 "그 frame을 request/response lifecycle에 연결하는 일"을 따로 읽을 수 있다.

## 3. demo는 가장 작은 successful round trip만 보여 준다

2026-03-14에 아래 명령을 다시 실행했다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/01-rpc-framing
GOWORK=off go run ./cmd/rpc-framing
```

출력은 아래였다.

```text
pong:hello
```

짧은 출력이지만 의미는 선명하다. `ping` request가 JSON params를 싣고 서버로 전달되고, correlation id가 붙은 response가 client pending entry로 다시 돌아와 결과를 unmarshalling한 뒤 caller에 전달됐다는 뜻이다.

## 4. 추가 재실행으로 split chunk와 failure path를 고정했다

이번에 project root 내부 임시 Go 파일로 추가 재실행을 돌린 결과는 아래였다.

```text
split_payloads 0 1
errors true true
```

이 결과는 두 가지를 보여 준다.

- frame을 절반씩 나눠 넣었을 때 첫 chunk에서는 payload가 안 나오고, 둘째 chunk가 붙은 뒤에야 하나의 complete payload가 나온다
- server error와 context timeout이 모두 caller-visible error로 전파된다

즉 decoder는 byte boundary와 message boundary를 분리해서 다루고, client는 pending call map을 통해 failure도 정상 response처럼 정리한다.
