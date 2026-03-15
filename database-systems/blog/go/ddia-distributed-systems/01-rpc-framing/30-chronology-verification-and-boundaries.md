# Verification And Boundaries

## 1. 자동 검증은 framing, round trip, concurrency, timeout을 넓게 덮는다

2026-03-14 기준 재실행 명령은 아래와 같다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/01-rpc-framing
GOWORK=off go test ./...
```

결과는 아래처럼 통과했다.

```text
ok  	study.local/go/ddia-distributed-systems/projects/01-rpc-framing/tests	(cached)
```

테스트가 잡는 항목은 다음과 같다.

- single message decode
- split chunk decode
- server/client round trip
- concurrent calls
- server error propagation
- timeout propagation

즉 framing layer와 client/server lifecycle을 함께 검증한다.

## 2. demo와 추가 재실행 관찰값

demo 출력:

```text
pong:hello
```

추가 재실행 출력:

```text
split_payloads 0 1
errors true true
```

이 결과를 합치면 현재 구현은 아래 사실을 만족한다.

- split chunk는 complete frame이 모일 때까지 대기한다
- successful round trip은 correlation id 기반 pending map으로 되돌아온다
- server error와 timeout은 caller-visible error로 전파된다

## 3. 현재 구현이 일부러 다루지 않는 것

이 랩을 production RPC stack으로 읽으면 안 된다.

- TLS가 없다
- auth가 없다
- streaming RPC가 없다
- discovery나 load balancing이 없다
- retry/backoff 정책이 없다

즉 지금 focus는 transport minimum viable path다.

## 4. 이 문서에서 피한 과장

이번 재작성에서는 아래 같은 표현을 쓰지 않았다.

- "실전 RPC 프레임워크를 구현했다"
- "네트워크 장애를 포괄적으로 해결했다"
- "production service mesh의 기반을 만들었다"

현재 소스와 테스트가 실제로 보여 주는 것은 framing boundary recovery, correlation id pending map, error/timeout/disconnect propagation까지다. 그보다 큰 네트워크 stack claim은 근거가 없다.
