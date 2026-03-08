# Stage 02 Fixtures And Harness Problem

seeded knowledge base와 replay harness를 분리해 상담 품질 실험을 재현 가능한 입력 집합 위에서 수행하도록 만드는 단계다.

## Stage Question

fixture와 replay를 어떻게 분리해야 회귀 테스트와 golden set 생성이 흔들리지 않는가?

## Inputs

- 환불, 해지, 본인확인 같은 한국어 상담 도메인 샘플 문서
- 예상 evidence 문서를 가진 replay 세션 목록

## Required Output

- `python/data/knowledge_base/*.md` seeded KB
- `python/data/replay_sessions.json` replay fixture
- `python/src/stage02/harness.py` deterministic replay runner

## Success Criteria

- 같은 replay 입력에 대해 항상 같은 retrieved doc order가 나온다.
- fixture 파일과 harness 코드가 분리되어 수정 범위가 명확하다.
- 후속 golden set과 version compare 입력으로 이어질 수 있다.

## Actual Status

- implementation directory가 생성되어 있음
- README/docs/problem 문서가 코드와 테스트 명령에 맞춰 업데이트됨
- 검증 명령: `cd python && UV_PYTHON=python3.12 uv run pytest -q`
