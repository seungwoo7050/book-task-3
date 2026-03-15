# 01 RPC Framing

## 이 랩의 실제 초점

이 프로젝트는 RPC를 만든다기보다, byte stream 위에서 message boundary를 복구하고 여러 동시 요청의 응답을 correlation id로 다시 짝짓는 최소 transport layer를 구현한다. 4-byte big-endian length prefix framing이 split chunk와 multi-frame chunk를 복원하고, client는 `correlation_id -> pending call` map을 유지해 응답 순서가 뒤섞여도 올바른 caller에게 결과를 돌려준다. handler error, timeout, disconnect는 모두 호출자에게 전파돼야 한다.

즉 이 랩의 핵심은 business handler가 아니라, framing boundary와 pending map이 어떤 network semantics를 만들어 내는가에 있다.

이번 시리즈는 기존 blog를 입력 근거로 쓰지 않고 [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/01-rpc-framing/problem/README.md), [`rpc.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/01-rpc-framing/internal/rpc/rpc.go), [`framing.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/01-rpc-framing/internal/framing/framing.go), [`rpc_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/01-rpc-framing/tests/rpc_test.go), [`main.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/01-rpc-framing/cmd/rpc-framing/main.go), 그리고 2026-03-14 재실행 결과만으로 다시 썼다.

## 이번에 붙드는 질문

- framing decoder는 split/multi-frame chunk를 어떻게 복원하는가
- pending map은 concurrent call을 어떤 기준으로 구분하는가
- unknown method, handler error, timeout, disconnect는 어디서 실패로 바뀌는가
- 이 transport layer가 일부러 비워 둔 RPC 확장 범위는 무엇인가

## 문서 지도

- [10-chronology-scope-and-surface.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/ddia-distributed-systems/01-rpc-framing/10-chronology-scope-and-surface.md): 문제 범위, server/client 표면, demo 결과를 시간순으로 정리한다.
- [20-chronology-core-invariants.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/ddia-distributed-systems/01-rpc-framing/20-chronology-core-invariants.md): length prefix decoding, pending correlation map, error propagation, fail-all-on-close를 소스 기준으로 해부한다.
- [30-chronology-verification-and-boundaries.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/ddia-distributed-systems/01-rpc-framing/30-chronology-verification-and-boundaries.md): go test와 demo, 추가 재실행을 묶어 현재 검증 범위와 한계를 정리한다.
- [_evidence-ledger.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/ddia-distributed-systems/01-rpc-framing/_evidence-ledger.md): 근거 파일과 재실행 명령, 관찰값을 남긴다.
- [_structure-outline.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/ddia-distributed-systems/01-rpc-framing/_structure-outline.md): 문서 구조 선택 이유와 버린 접근을 적는다.

## 지금 기준의 결론

이 랩은 Go 분산 시스템 트랙의 첫 단계에서 "RPC before business logic"를 보여 준다. TLS, auth, streaming, discovery는 아직 없다. 대신 frame boundary recovery, correlation id pending map, timeout/error/disconnect propagation은 분명하게 드러난다.
