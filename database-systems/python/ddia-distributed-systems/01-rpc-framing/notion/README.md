# 학습 노트 안내

네트워크 위의 나머지 분산 프로젝트를 위해, framed transport와 correlation id 기반 최소 RPC 계층을 먼저 고정하는 단계입니다.

## 이 노트를 읽기 전에 잡을 질문
- 스트림에서 메시지 경계를 복원하고 여러 동시 요청의 응답을 섞지 않으려면 client와 server는 어떤 최소 상태를 가져야 하는가?
- 다음 단계 `02 Leader-Follower Replication`에 무엇을 넘기는가?

## 권장 읽기 순서
1. `../problem/README.md`로 요구와 범위를 먼저 확인합니다.
2. `../src/rpc_framing/core.py`, `../src/rpc_framing/core.py`, `../tests/test_rpc_framing.py`를 열어 실제 구현 표면을 먼저 잡습니다.
3. `../tests/`에서 이 프로젝트가 무엇을 보장하는지 확인합니다. 핵심 테스트는 `test_decoder_handles_single_message`, `test_decoder_handles_split_chunks`, `test_rpc_server_client_round_trip`, `test_rpc_handles_concurrent_calls`입니다.
4. 데모 경로 `../src/rpc_framing/__main__.py`를 실행해 전체 흐름을 빠르게 눈으로 확인합니다.
5. 마지막으로 `./00-problem-framing.md`부터 `./04-knowledge-index.md`까지 읽으며 판단과 연결 지점을 정리합니다.

## 이번 노트가 담는 것
- `00-problem-framing.md`: 스트림에서 메시지 경계를 복원하고 여러 동시 요청의 응답을 섞지 않으려면 client와 server는 어떤 최소 상태를 가져야 하는가?에 대한 범위와 성공 기준을 정리합니다.
- `01-approach-log.md`: 프레이밍과 RPC 상태를 분리한다, pending map을 correlation id 기준으로 유지한다 같은 실제 구현 선택을 기록합니다.
- `02-debug-log.md`: split chunk에서 frame boundary가 깨지는 경우, 동시 요청 응답이 서로 바뀌는 경우처럼 다시 깨질 수 있는 지점을 모아 둡니다.
- `03-retrospective.md`: 이 단계에서 얻은 것, 남긴 단순화, 다음 확장 방향을 정리합니다.
- `04-knowledge-index.md`: 용어, 핵심 파일, 개념 문서, 검증 앵커를 빠르게 다시 찾는 인덱스입니다.

## 검증 앵커
- 테스트: `test_decoder_handles_single_message`, `test_decoder_handles_split_chunks`, `test_rpc_server_client_round_trip`, `test_rpc_handles_concurrent_calls`
- 데모 경로: `../src/rpc_framing/__main__.py`
- 데모가 보여 주는 장면: Go 데모는 간단한 요청을 보내 `reply` 값을 출력합니다. Python 데모도 client/server round trip 결과를 그대로 print합니다.
- 개념 문서: `../docs/concepts/frame-boundary.md`, `../docs/concepts/pending-map.md`

- 이전 장문 기록은 `../notion-archive/`에 보존돼 있습니다.
