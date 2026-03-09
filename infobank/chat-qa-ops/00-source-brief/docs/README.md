# Stage 00 Source Brief Docs

legacy 감사 결과와 최종 capstone 방향을 실행 가능한 source brief contract로 고정하는 단계다.

## Concept Focus

- 문서 중심 기획을 코드 계약으로 고정하는 방법
- baseline snapshot과 curriculum rationale의 분리
- reference spine을 stable navigation으로 유지하는 원칙

## Capstone Mapping

- `08/v0`를 기준점으로 삼는 이유를 stage 단위에서 먼저 고정한다.
- 이후 모든 README와 verification 문서는 이 source brief를 따라야 한다.

## Implementation Snapshot

- 구현됨: reference source manifest, project selection rationale snapshot
- staged/known gap: capstone runtime 없음

## Verification

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`

## Notes

- 테스트는 topic, baseline version, primary stack, reference spine 길이를 고정한다.
- runtime을 검증하는 단계는 아니므로 build보다 contract drift 방지가 핵심이다.
