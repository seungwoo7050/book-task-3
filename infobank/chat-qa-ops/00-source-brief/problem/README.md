# 00 문제 정의와 방향 고정 문제 정의

legacy 감사 결과와 최종 capstone 방향을 실행 가능한 source brief contract로 고정하는 단계다.

## 문제 해석

이 트랙이 무엇을 만들고 어떤 sequence와 stack을 따르는지 코드를 통해 어떻게 고정할 것인가?

## 입력

- 루트 `README.md`와 `docs/legacy-intent-audit.md`의 프로젝트 의도
- `docs/project-selection-rationale.md`, `docs/curriculum-map.md`, `docs/reference-spine.md`의 커리큘럼 근거
- `08-capstone-submission/v0-initial-demo`를 baseline으로 삼는 버전 전략

## 기대 산출물

- `python/src/stage00/source_brief.py`의 `SourceBrief` dataclass
- reference spine tuple과 baseline version contract
- stage-local pytest로 검증되는 stack/sequence snapshot

## 완료 기준

- 주제, capstone goal, baseline version, primary stack이 코드 객체 하나에 정리된다.
- reference spine이 임의 서술이 아니라 테스트 가능한 상수로 유지된다.
- 후속 stage가 이 brief를 설계 기준으로 재사용할 수 있다.

## 현재 확인 가능한 증거

- `python/tests/test_source_brief.py`가 baseline version과 stack contract를 검증한다.
- 생성된 stage README가 `00 -> 08` 순서를 repository-level index로 연결한다.

## 이 pack에서 바로 확인할 수 있는 것

- 구현 디렉터리: reference source manifest, project selection rationale snapshot
- 이번 단계에서 일부러 제외한 범위: capstone runtime 없음
- 검증 명령: `cd python && UV_PYTHON=python3.12 uv run pytest -q`
