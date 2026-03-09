# Problem Framing

TCP stream 위에서 message boundary를 복원하고, 동시에 여러 요청을 보낸 뒤 각 응답을 correlation id로 올바른 caller에게 되돌리는 최소 RPC 계층을 구현한다.

## Success Criteria

- 4-byte big-endian length prefix framing
- split chunk와 multi-frame chunk 모두 decode
- pending call map 기반 동시 요청 처리
- unknown method, handler error, timeout, disconnect 전파

## Source Provenance

- 원본 문제: `legacy/distributed-cluster/rpc-network/problem/README.md`
- 원본 테스트 의미: `legacy/distributed-cluster/rpc-network/solve/test/rpc.test.js`
- 원본 구현 참고: `legacy/distributed-cluster/rpc-network/solve/solution/rpc.js`
