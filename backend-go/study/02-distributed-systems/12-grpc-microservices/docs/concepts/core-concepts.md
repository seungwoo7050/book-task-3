# Core Concepts

## 핵심 개념

- proto-first는 API 계약을 코드보다 먼저 고정하는 접근이다.
- interceptor는 HTTP middleware와 비슷하지만 RPC 레벨의 횡단 관심사를 다룬다.
- unary 중심 예제라도 client/server 분리와 retry 로직을 같이 보면 gRPC 특성이 더 잘 드러난다.

## Trade-offs

- hand-written shim은 학습에는 빠르지만 실제 generated code workflow를 숨긴다.
- round-robin과 retry는 감각을 보여 주지만, production-grade observability나 timeout 정책은 더 필요하다.

## 실패하기 쉬운 지점

- `protoc` 산출물이 없는 구조에서 문서와 build 명령이 어긋나기 쉽다.
- unary call만 보고 gRPC를 “HTTP와 크게 다르지 않다”고 오해하기 쉽다.

