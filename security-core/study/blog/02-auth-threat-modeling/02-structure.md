# Structure Design — auth-threat-modeling

이 outline는 최종 글이 “인증 방식 비교”가 아니라 “finding vocabulary가 어떻게 생겨나는가”를 중심으로 읽히게 만들기 위한 뼈대다.

## opening

- 시작 질문: 왜 이 프로젝트는 “JWT를 쓴다”보다 “어떤 control이 빠졌는가”를 먼저 말하게 되었는가.
- 첫 증거: `docs/concepts/session-jwt-oauth-threats.md`와 `evaluator.py::CONTROL_META`
- 서술 원칙: auth 방식을 나열하기보다 finding vocabulary가 어떻게 생겼는지부터 따라간다.

## Session 1 — control vocabulary를 고정했다

- 다룰 표면: `python/src/auth_threat_modeling/evaluator.py`
- 먼저 던질 질문: “auth는 한 종류가 아니라 공격면이 다른 몇 개의 설계를 묶어 부르는 이름이다.”
- 꼭 넣을 CLI: `PYTHONPATH=study/02-auth-threat-modeling/python/src .venv/bin/python -m pytest study/02-auth-threat-modeling/python/tests`
- 꼭 남길 검증 신호: `8 passed in 0.04s`
- 핵심 전환 문장: JWT validation 누락을 한 줄 bool이 아니라 여러 체크 누락 목록으로 드러낸 순간 설명력이 커졌다.

## Session 2 — scenario bundle로 finding을 반복 가능하게 만들었다

- 다룰 표면: `python/src/auth_threat_modeling/scenarios.py`
- 먼저 던질 질문: “control은 정의만으로 끝나지 않고, 기대한 finding set과 비교돼야 한다.”
- 꼭 넣을 CLI: `... cli check-scenarios ... scenario_bundle.json`
- 꼭 남길 검증 신호: `passed=5`, `failed=0`
- 핵심 전환 문장: `actual_control_ids == expected_control_ids` 비교가 baseline과 취약 사례를 같은 언어로 묶는다.

## Session 3 — demo output과 CLI 테스트로 고정했다

- 다룰 표면: `python/src/auth_threat_modeling/cli.py`, `python/tests/test_cli.py`
- 먼저 던질 질문: “시나리오 평가기가 있어도 사람이 한 번에 읽을 demo가 없으면 학습용 surface가 닫히지 않는다.”
- 꼭 넣을 CLI: `... cli demo ... demo_profile.json`
- 꼭 남길 검증 신호: `oidc_cookie_hybrid_demo`의 7개 control ID
- 핵심 전환 문장: baseline 0 finding과 hybrid demo의 다중 finding이 같이 있어야 control gap 설명이 끝까지 살아남는다.

## ending

- 마지막 단락에서는 범위 밖인 `WebAuthn`, `device trust`, `risk-based auth`를 짧게 남긴다.
- 다음 질문은 “auth control vocabulary를 backend route defense vocabulary로 어떻게 확장할까”로 넘긴다.
