# 접근 기록

## 읽기 순서 제안
1. `../problem/README.md`에서 요구와 현재 재구성 범위를 먼저 확인합니다.
2. 구현 핵심 파일을 열어 어떤 타입과 함수가 중심인지 확인합니다.
3. `../tests/`를 읽어 이 프로젝트가 실제로 고정한 계약을 확인합니다.
4. 데모를 실행해 테스트가 말하는 계약이 출력으로도 드러나는지 봅니다.
5. 마지막에 개념 문서를 읽으며 용어와 설계 판단을 정리합니다.

## 코드가 택한 분해 방식
### 프레이밍과 RPC 상태를 분리한다
- 관련 파일: `../src/rpc_framing/core.py`, `../src/rpc_framing/core.py`
- 판단: decoder는 메시지 경계 복원만 담당하고, client/server는 그 위에서 correlation id와 handler 호출을 관리합니다.

### pending map을 correlation id 기준으로 유지한다
- 관련 파일: `../src/rpc_framing/core.py`
- 판단: 응답은 요청 순서와 다르게 도착할 수 있으므로, 요청 순번이 아니라 correlation id를 키로 잡아야 합니다.

### timeout과 connection close를 explicit failure로 정리한다
- 관련 파일: `../src/rpc_framing/core.py`
- 판단: 지연되거나 끊긴 요청을 침묵 속에 두지 않고, pending entry를 정리하면서 호출자에게 에러를 돌려주는 쪽을 택했습니다.

## 검증 명령
```bash
cd python/ddia-distributed-systems/projects/01-rpc-framing
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev]'
PYTHONPATH=src python -m pytest
PYTHONPATH=src python -m rpc_framing
```

## 포트폴리오 설명으로 바꿀 때 남길 장면
- decoder와 pending map을 분리해 둔 구조는 transport와 protocol state를 어떻게 나눴는지 보여 줍니다.
- split chunk test와 concurrent call test를 함께 제시하면 framing과 correlation이 왜 둘 다 필요한지 설명하기 좋습니다.
- timeout cleanup은 눈에 띄지 않지만 실제 시스템 감각을 보여 주는 좋은 포인트입니다.
