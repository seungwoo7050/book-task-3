# 접근 기록

## 읽기 순서 제안
1. `../problem/README.md`에서 요구와 현재 재구성 범위를 먼저 확인합니다.
2. 구현 핵심 파일을 열어 어떤 타입과 함수가 중심인지 확인합니다.
3. `../tests/`를 읽어 이 프로젝트가 실제로 고정한 계약을 확인합니다.
4. 데모를 실행해 테스트가 말하는 계약이 출력으로도 드러나는지 봅니다.
5. 마지막에 개념 문서를 읽으며 용어와 설계 판단을 정리합니다.

## 코드가 택한 분해 방식
### 정적 topology로 shard와 replica group을 먼저 고정한다
- 관련 파일: `../src/clustered_kv/core.py`
- 판단: membership churn까지 넣으면 핵심이 흐려지므로, 현재는 shard 배치와 replica 구성을 명시적으로 선언하는 쪽을 택했습니다.

### write pipeline을 leader local apply와 follower catch-up으로 나눈다
- 관련 파일: `../src/clustered_kv/core.py`
- 판단: leader가 먼저 local disk-backed store에 기록하고, follower는 watermark 이후 entry를 당겨오는 구조로 end-to-end 흐름을 단순화했습니다.

### HTTP boundary를 thin adapter로만 둔다
- 관련 파일: `../src/clustered_kv/app.py`, `../src/clustered_kv/core.py`
- 판단: `create_app`은 FastAPI를 core 로직 위에 얇게 얹고, 테스트에서는 `TestClient`로 boundary만 검증합니다.

## 검증 명령
```bash
cd python/ddia-distributed-systems/projects/04-clustered-kv-capstone
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev]'
PYTHONPATH=src python -m pytest
PYTHONPATH=src python -m clustered_kv
```

## 포트폴리오 설명으로 바꿀 때 남길 장면
- 하나의 key가 shard, leader, follower, disk를 거치는 흐름을 그림으로 보여 주면 캡스톤 가치가 바로 드러납니다.
- 정적 topology라는 의도적 단순화는 무엇을 아직 하지 않았는가를 솔직하게 설명하는 좋은 장치입니다.
- FastAPI를 얇은 경계로만 두고 핵심 상태 전이는 `core.py`에 모았다는 점도 설명 포인트가 됩니다.
