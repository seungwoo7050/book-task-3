# Series Map — auth-threat-modeling

이 시리즈는 session cookie, bearer JWT, OAuth/OIDC redirect flow를 한꺼번에 “인증”이라고 부르지 않고, 어떤 control이 빠졌을 때 어떤 finding이 생기는지로 다시 읽는다. 읽는 순서도 그 흐름을 따른다. 먼저 control vocabulary를 세우고, 그 vocabulary를 scenario bundle로 고정한 다음, demo output으로 한 설계의 구멍을 한 번에 읽게 만든다.

## 범위

- 핵심 질문: session cookie, bearer JWT, OAuth/OIDC redirect flow를 기능 이름이 아니라 control gap과 finding으로 어떻게 고정할 것인가.
- 글의 단위: control vocabulary 정의 -> scenario bundle summary -> demo/CLI 계약.
- chronology 표지: 세부 commit 흐름이 없어서 `Session 1`부터 `Session 3`까지로 복원한다.

## source set

이 시리즈는 README와 개념 문서로 질문을 고정하고, `evaluator.py`, `scenarios.py`, CLI 테스트로 실제 판단 surface를 확인한다.

- `../../02-auth-threat-modeling/README.md`
- `../../02-auth-threat-modeling/problem/README.md`
- `../../02-auth-threat-modeling/docs/README.md`
- `../../02-auth-threat-modeling/docs/concepts/session-jwt-oauth-threats.md`
- `../../02-auth-threat-modeling/python/README.md`
- `../../02-auth-threat-modeling/python/src/auth_threat_modeling/evaluator.py`
- `../../02-auth-threat-modeling/python/src/auth_threat_modeling/scenarios.py`
- `../../02-auth-threat-modeling/python/src/auth_threat_modeling/cli.py`
- `../../02-auth-threat-modeling/python/tests/test_evaluator.py`
- `../../02-auth-threat-modeling/python/tests/test_cli.py`

## canonical CLI

```bash
PYTHONPATH=study/02-auth-threat-modeling/python/src \
  .venv/bin/python -m pytest study/02-auth-threat-modeling/python/tests

PYTHONPATH=study/02-auth-threat-modeling/python/src \
  .venv/bin/python -m auth_threat_modeling.cli check-scenarios \
  study/02-auth-threat-modeling/problem/data/scenario_bundle.json

PYTHONPATH=study/02-auth-threat-modeling/python/src \
  .venv/bin/python -m auth_threat_modeling.cli demo \
  study/02-auth-threat-modeling/problem/data/demo_profile.json
```

## series

1. [01-evidence-ledger.md](01-evidence-ledger.md)
2. [02-structure.md](02-structure.md)
3. [10-chronology-turning-auth-controls-into-deterministic-findings.md](10-chronology-turning-auth-controls-into-deterministic-findings.md)
