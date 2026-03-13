# 12 gRPC Microservices Structure

## 이 글이 답할 질문

- 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- client와 server를 분리해 retry, auth, logging interceptor를 서로 다른 관점에서 읽게 했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `02-distributed-systems/12-grpc-microservices` 안에서 `30-client-flow-and-proof.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 8단계: 클라이언트 구현 (client/client.go) -> 9단계: 실행 및 검증 -> 10단계: 테스트
- 세션 본문: `solution/go/client/client.go, solution/go/server/store/store_test.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/client/client.go`
- 코드 앵커 2: `solution/go/server/store/store_test.go`
- 코드 설명 초점: 이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.
- 개념 설명: unary 중심 예제라도 client/server 분리와 retry 로직을 같이 보면 gRPC 특성이 더 잘 드러난다.
- 마지막 단락: generated `.pb.go` 자동 생성 파이프라인은 아직 별도로 마련하지 않았다.
