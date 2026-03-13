# auth-threat-modeling series map

이 시리즈는 `auth-threat-modeling`을 "인증 방식 비교표"가 아니라, 어떤 control이 빠졌을 때 어떤 finding이 나와야 하는지를 JSON scenario로 고정하는 lab으로 다시 읽기 위한 지도다.

## 이 프로젝트가 답하는 질문

- cookie session, bearer JWT, OAuth/OIDC redirect flow를 한 evaluator 안에 넣으면서도 공격면 차이를 어떻게 잃지 않을까
- secure baseline과 negative scenario를 같이 두면 auth 설명이 제품 기능 소개가 아니라 threat review로 어떻게 바뀔까

## 읽는 순서

1. [10-chronology-control-vocabulary-scenarios-and-demo-findings.md](10-chronology-control-vocabulary-scenarios-and-demo-findings.md)

## 참조한 실제 파일

- `study/02-auth-threat-modeling/README.md`
- `study/02-auth-threat-modeling/problem/README.md`
- `study/02-auth-threat-modeling/problem/data/scenario_bundle.json`
- `study/02-auth-threat-modeling/problem/data/demo_profile.json`
- `study/02-auth-threat-modeling/docs/concepts/session-jwt-oauth-threats.md`
- `study/02-auth-threat-modeling/python/README.md`
- `study/02-auth-threat-modeling/python/src/auth_threat_modeling/evaluator.py`
- `study/02-auth-threat-modeling/python/src/auth_threat_modeling/scenarios.py`
- `study/02-auth-threat-modeling/python/src/auth_threat_modeling/cli.py`
- `study/02-auth-threat-modeling/python/tests/test_evaluator.py`
- `study/02-auth-threat-modeling/python/tests/test_cli.py`

## Canonical CLI

```bash
cd study/02-auth-threat-modeling
PYTHONPATH=python/src ../../.venv/bin/python -m pytest python/tests
PYTHONPATH=python/src ../../.venv/bin/python -m auth_threat_modeling.cli check-scenarios problem/data/scenario_bundle.json
PYTHONPATH=python/src ../../.venv/bin/python -m auth_threat_modeling.cli demo problem/data/demo_profile.json
```

## Git Anchor

- `2026-03-12 e3be503 Track Appendix 에 대한 전반적인 개선 완료 (mobile / security)`

## 추론 원칙

- 날짜 단위 이력은 얇으므로 chronology는 `CONTROL_META`, scenario fixture, CLI summary의 의존 관계를 따라 복원했다.
- 이 lab의 끝은 OAuth state 하나를 잡는 데 있지 않고, secure baseline과 insecure scenario들이 모두 `actual_control_ids == expected_control_ids`로 닫히는 지점으로 본다.
