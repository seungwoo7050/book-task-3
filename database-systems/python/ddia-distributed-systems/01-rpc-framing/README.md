# 01 RPC Framing

length-prefixed framing과 correlation id 기반 pending map으로 최소 RPC 계층을 구현합니다.

## 이 프로젝트에서 배우는 것

- TCP stream에서 message boundary를 복구하는 방법을 익힙니다.
- correlation id와 pending call map으로 동시 요청을 구분합니다.
- timeout, disconnect, handler error를 호출자에게 전달하는 흐름을 이해합니다.

## 먼저 알고 있으면 좋은 것

- 기본적인 socket/TCP 개념을 알고 있으면 좋습니다.
- request/response 모델이 어떻게 비동기적으로 이어지는지 감을 잡고 있으면 읽기 쉽습니다.

## 추천 읽기 순서

1. `problem/README.md`로 문제 해석과 현재 범위를 먼저 확인합니다.
2. `docs/README.md`와 개념 노트를 읽어, 코드에 들어가기 전 핵심 용어를 맞춥니다.
3. `src/`와 `tests/`를 함께 읽고, 마지막에 패키지 entry point를 실행해 전체 흐름을 확인합니다.
4. `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 구현 표면

- `problem/`: 현재 프로젝트 문제 해석과 제공 자료
- `docs/`: 개념 메모와 설명형 참고자료 목록
- `src/rpc_framing/`, `tests/`: 실제 구현과 검증 코드
- `notion/`: 현재 공개용 학습 노트
- `notion-archive/`: 이전 세대 문서 보관본

## 검증 명령

```bash
cd python/ddia-distributed-systems/01-rpc-framing
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -U pytest
PYTHONPATH=src python -m pytest
PYTHONPATH=src python -m rpc_framing
```

## 구현에서 집중할 포인트

- split chunk와 multi-frame chunk가 모두 decoder에서 제대로 복원되는지 확인합니다.
- pending map에서 응답 매칭과 timeout 정리가 일관적인지 봅니다.
- server와 client가 같은 frame contract를 공유하는지 확인합니다.

## 포트폴리오로 발전시키려면

- codec pluggability, tracing id, retry policy를 추가하면 네트워크 계층 설계 경험을 보여 주기 좋습니다.
- streaming RPC나 observability를 붙이면 다음 분산 프로젝트와 연결하기 쉬워집니다.
