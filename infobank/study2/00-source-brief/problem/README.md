# Stage 00 Source Brief Problem

legacy 감사 결과와 최종 capstone 방향을 실행 가능한 source brief contract로 고정하는 단계다.

## Stage Question

이 트랙이 무엇을 만들고 어떤 sequence와 stack을 따르는지 코드를 통해 어떻게 고정할 것인가?

## Inputs

- 루트 `README.md`와 `docs/legacy-intent-audit.md`의 프로젝트 의도
- `docs/project-selection-rationale.md`, `docs/curriculum-map.md`, `docs/reference-spine.md`의 커리큘럼 근거
- `08-capstone-submission/v0-initial-demo`를 baseline으로 삼는 버전 전략

## Required Output

- `python/src/stage00/source_brief.py`의 `SourceBrief` dataclass
- reference spine tuple과 baseline version contract
- stage-local pytest로 검증되는 stack/sequence snapshot

## Success Criteria

- 주제, capstone goal, baseline version, primary stack이 코드 객체 하나에 정리된다.
- reference spine이 임의 서술이 아니라 테스트 가능한 상수로 유지된다.
- 후속 stage가 이 brief를 설계 기준으로 재사용할 수 있다.

## Actual Status

- implementation directory가 생성되어 있음
- README/docs/problem 문서가 코드와 테스트 명령에 맞춰 업데이트됨
- 검증 명령: `cd python && UV_PYTHON=python3.12 uv run pytest -q`
