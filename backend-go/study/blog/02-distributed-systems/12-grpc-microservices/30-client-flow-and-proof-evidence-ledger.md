# 12 gRPC Microservices Evidence Ledger

## 30 client-flow-and-proof

- 시간 표지: 8단계: 클라이언트 구현 (client/client.go) -> 9단계: 실행 및 검증 -> 10단계: 테스트
- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/client/client.go`, `solution/go/server/store/store_test.go`
- 처음 가설: client와 server를 분리해 retry, auth, logging interceptor를 서로 다른 관점에서 읽게 했다.
- 실제 조치: `grpc.Dial` with insecure credentials Round-robin load balancing Retry interceptor (max 3, exponential backoff) Logging interceptor 서버 시작 클라이언트 테스트 (별도 터미널) Store 테스트: CRUD, List 필터, 동시 접근 안전성.

CLI:

```bash
go run ./server/cmd
# starting gRPC server port=50051

go run ./client/cmd
```

- 검증 신호:
- 2026-03-07 기준 세 명령이 모두 통과했다.
- store 패키지 테스트는 정상 통과했고, client/server cmd 패키지는 smoke build 수준으로 검증했다.
- 남은 선택 검증: generated `.pb.go` 자동 생성 파이프라인은 아직 별도로 마련하지 않았다.
- 핵심 코드 앵커: `solution/go/client/client.go`
- 새로 배운 것: unary 중심 예제라도 client/server 분리와 retry 로직을 같이 보면 gRPC 특성이 더 잘 드러난다.
- 다음: generated `.pb.go` 자동 생성 파이프라인은 아직 별도로 마련하지 않았다.
