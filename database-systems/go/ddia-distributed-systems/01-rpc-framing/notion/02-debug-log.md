# 디버그 포인트

이 파일은 과거를 꾸며내는 로그가 아니라, 다시 읽거나 다시 구현할 때 가장 먼저 의심할 지점을 프로젝트 기준으로 정리한 메모입니다.

## 먼저 확인할 세부 지점
### 1. split chunk에서 frame boundary가 깨지는 경우
- 의심 파일: `../internal/framing/framing.go`
- 깨지는 징후: 헤더와 payload가 여러 번에 나눠 들어올 때 decoder가 조합을 잘못하면 이후 모든 응답이 무너집니다.
- 확인 테스트: `TestDecoderHandlesSplitChunks`
- 다시 볼 질문: 길이 헤더를 읽은 뒤 payload가 충분히 모일 때까지 state를 유지하는가?

### 2. 동시 요청 응답이 서로 바뀌는 경우
- 의심 파일: `../internal/rpc/rpc.go`
- 깨지는 징후: pending map 키나 cleanup 시점이 틀리면 응답이 엉뚱한 호출자에게 돌아갑니다.
- 확인 테스트: `TestRPCHandlesConcurrentCalls`
- 다시 볼 질문: 응답 수신 시 correlation id로 pending entry를 pop하는가?

### 3. server error나 timeout이 침묵 속에 사라지는 경우
- 의심 파일: `../internal/rpc/rpc.go`
- 깨지는 징후: 호출자가 실패를 알 수 없으면 상위 replication/consensus 단계 디버깅이 매우 어려워집니다.
- 확인 테스트: `TestRPCPropagatesServerErrorsAndTimeout`
- 다시 볼 질문: timeout, connection close, handler error가 모두 pending call cleanup과 함께 외부로 전파되는가?
