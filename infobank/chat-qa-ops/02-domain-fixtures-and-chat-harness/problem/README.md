# 02 도메인 픽스처와 리플레이 하니스 문제 정의

seeded knowledge base와 replay harness를 분리해 상담 품질 실험을 재현 가능한 입력 집합 위에서 수행하도록 만드는 단계다.

## 문제 해석

fixture와 replay를 어떻게 분리해야 회귀 테스트와 golden set 생성이 흔들리지 않는가?

## 입력

- 환불, 해지, 본인확인 같은 한국어 상담 도메인 샘플 문서
- 예상 evidence 문서를 가진 replay 세션 목록

## 기대 산출물

- `python/data/knowledge_base/*.md` seeded KB
- `python/data/replay_sessions.json` replay fixture
- `python/src/stage02/harness.py` deterministic replay runner

## 완료 기준

- 같은 replay 입력에 대해 항상 같은 retrieved doc order가 나온다.
- fixture 파일과 harness 코드가 분리되어 수정 범위가 명확하다.
- 후속 golden set과 version compare 입력으로 이어질 수 있다.

## 현재 확인 가능한 증거

- `python/tests/test_harness.py`가 fixture loading과 replay 결과를 검증한다.
- fixture 파일은 markdown과 JSON으로 분리되어 사람이 직접 검토하기 쉽다.

## 이 pack에서 바로 확인할 수 있는 것

- 구현 디렉터리: seeded KB loader, deterministic replay harness
- 이번 단계에서 일부러 제외한 범위: database 없음
- 검증 명령: `cd python && UV_PYTHON=python3.12 uv run pytest -q`
