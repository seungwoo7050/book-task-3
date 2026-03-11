# 01 RPC Framing

length-prefixed framing과 correlation id 기반 pending map으로 최소 RPC 계층을 구현합니다.

## 문제

- 4-byte big-endian length prefix framing을 구현해야 합니다.
- split chunk와 multi-frame chunk를 모두 decode해야 합니다.
- pending call map 기반 동시 요청 처리가 필요합니다.
- unknown method, handler error, timeout, disconnect를 호출자에게 전파해야 합니다.

## 내 해법

- TCP stream에서 message boundary를 복구하는 방법을 익힙니다.
- correlation id와 pending call map으로 동시 요청을 구분합니다.
- timeout, disconnect, handler error를 호출자에게 전달하는 흐름을 이해합니다.

## 검증

```bash
cd go/ddia-distributed-systems/projects/01-rpc-framing
GOWORK=off go test ./...
GOWORK=off go run ./cmd/rpc-framing
```

## 코드 지도

- `problem/README.md`: 문제 정의, 제약, 제공 자료, provenance를 확인하는 시작점입니다.
- `docs/README.md`: 개념 메모와 참고자료 인덱스를 먼저 훑는 문서입니다.
- `internal/`: 핵심 구현이 들어 있는 패키지입니다.
- `tests/`: 회귀 테스트와 검증 시나리오를 모아 둔 위치입니다.
- `cmd/`: 직접 실행해 흐름을 확인하는 demo entry point입니다.
- `notion/README.md`: 현재 공개용 학습 노트와 설계 로그의 입구입니다.
- `notion-archive/README.md`: 이전 세대 문서를 보존하는 아카이브입니다.

## 읽는 순서

- `problem/README.md`로 문제 해석과 현재 범위를 먼저 확인합니다.
- `docs/README.md`와 개념 노트를 읽어, 코드에 들어가기 전 핵심 용어를 맞춥니다.
- `internal/`와 `tests/`를 함께 읽고, 마지막에 `cmd/rpc-framing/`로 동작 예시를 확인합니다.
- `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 한계와 확장

- 현재 범위 밖: TLS, 인증, streaming RPC는 포함하지 않습니다.
- 현재 범위 밖: 서비스 디스커버리나 로드 밸런싱은 다음 단계 범위입니다.
- 확장 아이디어: codec pluggability, tracing id, retry policy를 추가하면 네트워크 계층 설계 경험을 보여 주기 좋습니다.
- 확장 아이디어: streaming RPC나 observability를 붙이면 다음 분산 프로젝트와 연결하기 쉬워집니다.
