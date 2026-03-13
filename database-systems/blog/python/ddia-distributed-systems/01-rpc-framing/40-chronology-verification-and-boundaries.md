# 40 Verification And Boundaries

## Day 1
### Session 6

최종 검증은 다음 두 명령으로 닫는다.

```bash
cd python/ddia-distributed-systems/projects/01-rpc-framing
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m rpc_framing
```

검증 신호:

- `5 passed`
- demo 출력: `{'msg': 'hello'}`

테스트가 커버하는 경계:

- framing: 단일 frame, split chunk
- RPC: round-trip, concurrent call 분리
- 오류: handler 예외 전파, timeout 전파

boundary 정리:

- 다루는 것:
  - length-prefixed frame decode
  - correlation id 기반 요청-응답 매칭
  - timeout/error 표면
- 다루지 않는 것:
  - authn/authz
  - stream/bidirectional RPC
  - transport-level encryption

다음 질문:

- retry를 붙일 때 duplicate request 처리(멱등성)는 어느 계층에서 책임질까
- leader-follower 복제로 올라갈 때 timeout과 watermark를 어떻게 함께 다뤄야 할까