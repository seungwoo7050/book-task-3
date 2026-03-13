# 12 gRPC Microservices Evidence Ledger

## 10 proto-contract-and-service-shape

- 시간 표지: 1단계: 프로젝트 초기화 -> 2단계: gRPC 의존성 설치 -> 3단계: 디렉토리 구조 생성 -> 4단계: Proto 정의 (proto/catalog.proto)
- 당시 목표: Product Catalog용 gRPC 서비스 계약을 설계해야 한다.
- 변경 단위: `solution/go/proto/catalog.proto`, `solution/go/server/store/store.go`
- 처음 가설: generated code 자동화보다 계약과 호출 흐름을 먼저 이해시키기 위해 hand-written shim 예제를 택했다.
- 실제 조치: 메시지: Product, 각 RPC별 Request/Response, PriceUpdate 등.

CLI:

```bash
cd study/02-distributed-systems/12-grpc-microservices/go
go mod init github.com/woopinbell/go-backend/study/02-distributed-systems/12-grpc-microservices

go get google.golang.org/grpc@v1.62.0
go get google.golang.org/protobuf
```

- 검증 신호:
- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.
- 핵심 코드 앵커: `solution/go/proto/catalog.proto`
- 새로 배운 것: proto-first는 API 계약을 코드보다 먼저 고정하는 접근이다.
- 다음: 다음 글에서는 `20-server-store-and-interceptors.md`에서 이어지는 경계를 다룬다.
