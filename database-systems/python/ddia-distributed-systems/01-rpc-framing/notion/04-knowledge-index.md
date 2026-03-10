# 지식 인덱스

## 핵심 용어
- `framing`: 스트림 위에서 메시지 하나의 경계를 복원하는 규칙입니다.
- `correlation id`: 요청과 응답을 서로 매칭하기 위한 식별자입니다.
- `pending map`: 아직 응답을 기다리는 호출을 저장하는 client 측 상태입니다.
- `timeout`: 정해진 시간 안에 응답이 오지 않을 때 실패로 처리하는 규칙입니다.
- `handler error`: server가 요청을 처리하다 실패했을 때 response로 전달하는 오류입니다.

## 다시 볼 파일
- `../src/rpc_framing/core.py`: length-prefixed decoder와 frame encode/decode 경로를 확인할 수 있습니다.
- `../src/rpc_framing/core.py`: pending map, correlation id, timeout handling이 모여 있습니다.
- `../tests/test_rpc_framing.py`: split chunk, concurrent call, timeout/error propagation을 검증합니다.
- `../docs/concepts/pending-map.md`: 동시 요청이 많아질 때 pending map이 왜 필요한지 정리합니다.

## 개념 문서
- `../docs/concepts/frame-boundary.md`: 스트림 위에서 메시지 경계를 복원하는 framing 방식을 설명합니다.
- `../docs/concepts/pending-map.md`: correlation id로 동시 요청과 응답을 맞추는 구조를 설명합니다.

## 검증 앵커
- 확인일: 2026-03-10
- 테스트 파일: `../tests/test_rpc_framing.py`
- 다시 돌릴 테스트 이름: `test_decoder_handles_single_message`, `test_decoder_handles_split_chunks`, `test_rpc_server_client_round_trip`, `test_rpc_handles_concurrent_calls`, `test_rpc_propagates_server_errors_and_timeout`
- 데모 경로: `../src/rpc_framing/__main__.py`
- 데모가 보여 주는 장면: Go 데모는 간단한 요청을 보내 `reply` 값을 출력합니다. Python 데모도 client/server round trip 결과를 그대로 print합니다.

- 더 긴 이전 기록은 `../notion-archive/`에 남겨 두고, 여기에는 다시 읽을 때 바로 쓸 정보만 남깁니다.
