# Stage 02 Fixtures And Harness Docs

seeded knowledge base와 replay harness를 분리해 상담 품질 실험을 재현 가능한 입력 집합 위에서 수행하도록 만드는 단계다.

## Concept Focus

- seeded KB 설계
- deterministic replay harness
- expected evidence document 확인 방식

## Capstone Mapping

- v0의 replay harness와 seeded KB를 축소한 학습용 집중 구현본이다.
- v1/v2의 golden replay도 입력 fixture 분리가 핵심이다.

## Implementation Snapshot

- 구현됨: seeded KB loader, deterministic replay harness
- staged/known gap: database 없음

## Verification

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`

## Notes

- 테스트는 seeded KB 파일 집합과 첫 replay의 top-1 문서를 검증한다.
- DB나 vector store 없이도 회귀 입력 contract를 설명할 수 있어야 한다.
