# 12 gRPC Microservices Structure

## 이 글이 답할 질문

- Product Catalog용 gRPC 서비스 계약을 설계해야 한다.
- generated code 자동화보다 계약과 호출 흐름을 먼저 이해시키기 위해 hand-written shim 예제를 택했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `02-distributed-systems/12-grpc-microservices` 안에서 `10-proto-contract-and-service-shape.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 1단계: 프로젝트 초기화 -> 2단계: gRPC 의존성 설치 -> 3단계: 디렉토리 구조 생성 -> 4단계: Proto 정의 (proto/catalog.proto)
- 세션 본문: `solution/go/proto/catalog.proto, solution/go/server/store/store.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/proto/catalog.proto`
- 코드 앵커 2: `solution/go/server/store/store.go`
- 코드 설명 초점: 이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.
- 개념 설명: proto-first는 API 계약을 코드보다 먼저 고정하는 접근이다.
- 마지막 단락: 다음 글에서는 `20-server-store-and-interceptors.md`에서 이어지는 경계를 다룬다.
