# 11 Rate Limiter Structure

## 이 글이 답할 질문

- Token Bucket 알고리즘을 직접 구현해야 한다.
- rate limiter 자체와 HTTP middleware를 분리해 알고리즘과 네트워크 표면을 따로 읽게 했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `01-backend-core/11-rate-limiter` 안에서 `10-token-bucket-core.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 1단계: 프로젝트 초기화 -> 2단계: 패키지 구조 -> 3단계: Limiter 구조체 (limiter.go) -> 4단계: Allow() 구현 -> 5단계: ClientLimiter 구현 -> 6단계: cleanup goroutine
- 세션 본문: `solution/go/limiter.go, solution/go/limiter_test.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/limiter.go`
- 코드 앵커 2: `solution/go/limiter_test.go`
- 코드 설명 초점: 이 블록은 병렬성과 보호 정책을 아이디어가 아니라 코드 invariant로 바꾼다. goroutine, channel, token을 어떤 경계로 묶었는지가 여기서 드러난다.
- 개념 설명: token bucket은 burst를 허용하면서 평균 처리율을 제한한다.
- 마지막 단락: 다음 글에서는 `20-http-middleware-and-bench.md`에서 이어지는 경계를 다룬다.
