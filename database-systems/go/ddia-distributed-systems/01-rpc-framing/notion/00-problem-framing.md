# 문제 프레이밍

## 왜 이 프로젝트를 하는가
네트워크 위의 나머지 분산 프로젝트를 위해, framed transport와 correlation id 기반 최소 RPC 계층을 먼저 고정하는 단계입니다.

## 커리큘럼 안에서의 위치
- 트랙: DDIA Distributed Systems / Go
- 이전 단계: 없음
- 다음 단계: 02 Leader-Follower Replication
- 지금 답하려는 질문: 스트림에서 메시지 경계를 복원하고 여러 동시 요청의 응답을 섞지 않으려면 client와 server는 어떤 최소 상태를 가져야 하는가?

## 이번 구현에서 성공으로 보는 것
- decoder가 한 프레임 또는 여러 조각으로 들어온 payload를 정확히 복원해야 합니다.
- client와 server가 request/response round trip을 수행해야 합니다.
- 동시 요청이 있어도 correlation id로 응답을 올바르게 매칭해야 합니다.
- server error와 client timeout이 호출자에게 전달되어야 합니다.
- connection close 시 남은 pending call이 정리되어야 합니다.

## 먼저 열어 둘 파일
- `../internal/framing/framing.go`: length-prefixed decoder와 frame encode/decode 경로를 확인할 수 있습니다.
- `../internal/rpc/rpc.go`: pending map, correlation id, timeout handling이 모여 있습니다.
- `../tests/rpc_test.go`: split chunk, concurrent call, timeout/error propagation을 검증합니다.
- `../docs/concepts/pending-map.md`: 동시 요청이 많아질 때 pending map이 왜 필요한지 정리합니다.

## 의도적으로 남겨 둔 범위 밖 항목
- retransmission, retry budget, authentication, TLS는 포함하지 않습니다.
- streaming RPC와 connection pooling도 아직 구현하지 않습니다.

## 데모에서 바로 확인할 장면
- 간단한 RPC round trip 후 `reply`를 출력합니다.
