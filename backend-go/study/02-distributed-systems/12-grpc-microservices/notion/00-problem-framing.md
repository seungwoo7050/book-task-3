# 문제 정의 — 왜 gRPC인가

## HTTP/JSON의 한계

05-09에서 만든 API는 전부 HTTP + JSON이었다. 클라이언트가 JSON을 만들고, 서버가 JSON을 파싱하고, 응답을 다시 JSON으로 직렬화한다. 사람이 읽을 수 있다는 장점이 있지만:

1. **타입 안전성 부족**: JSON에는 스키마가 없다. 클라이언트가 `"price": "not a number"`를 보내면 런타임에서야 발견된다.
2. **성능**: 텍스트 기반 직렬화/역직렬화는 바이너리보다 느리다.
3. **스트리밍 미지원**: HTTP/1.1에서 서버가 데이터를 점진적으로 보내기 어렵다.
4. **코드 생성 없음**: 클라이언트와 서버가 같은 API 규약을 따르려면 문서에 의존한다.

gRPC는 이 네 가지를 모두 해결한다.

## 핵심 과제

**Product Catalog 마이크로서비스**를 gRPC로 구현한다:

| RPC | 유형 | 설명 |
|-----|------|------|
| GetProduct | Unary | ID로 단일 상품 조회 |
| CreateProduct | Unary | 상품 생성 |
| UpdateProduct | Unary | 상품 수정 |
| DeleteProduct | Unary | 상품 삭제 |
| ListProducts | Server stream | 전체 상품을 하나씩 스트리밍 |
| PriceWatch | Bidirectional stream | 가격 변동 실시간 감시 |

추가로:
- **Interceptor**: gRPC 버전의 미들웨어 (로깅, 인증)
- **클라이언트**: 재시도(exponential backoff) + round-robin 로드밸런싱

## 02-distributed-systems의 시작

12는 분산 시스템 섹션의 첫 프로젝트다. 01-backend-core(05~11)에서 HTTP API, SQL, 동시성, rate limiting을 다뤘고, 이제 서비스 간 통신으로 넘어간다. gRPC는 마이크로서비스 아키텍처에서 가장 널리 쓰이는 RPC 프레임워크다.

## 의존성

- `google.golang.org/grpc` v1.62.0 — gRPC Go 구현체
- `google.golang.org/protobuf` — Protocol Buffers 런타임
