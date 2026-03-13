# auth-threat-modeling blog

이 디렉터리는 `auth-threat-modeling`을 `source-first` 방식으로 다시 읽는 프로젝트 단위 blog 시리즈다. chronology는 README, 시나리오 fixture, 개념 문서, evaluator, pytest, 실제 CLI 출력만으로 복원했다.

## source set

- [../../02-auth-threat-modeling/README.md](../../02-auth-threat-modeling/README.md)
- [../../02-auth-threat-modeling/problem/README.md](../../02-auth-threat-modeling/problem/README.md)
- [../../02-auth-threat-modeling/problem/data/scenario_bundle.json](../../02-auth-threat-modeling/problem/data/scenario_bundle.json)
- [../../02-auth-threat-modeling/problem/data/demo_profile.json](../../02-auth-threat-modeling/problem/data/demo_profile.json)
- [../../02-auth-threat-modeling/docs/README.md](../../02-auth-threat-modeling/docs/README.md)
- [../../02-auth-threat-modeling/docs/concepts/session-jwt-oauth-threats.md](../../02-auth-threat-modeling/docs/concepts/session-jwt-oauth-threats.md)
- [../../02-auth-threat-modeling/python/README.md](../../02-auth-threat-modeling/python/README.md)
- [../../02-auth-threat-modeling/python/src/auth_threat_modeling/evaluator.py](../../02-auth-threat-modeling/python/src/auth_threat_modeling/evaluator.py)
- [../../02-auth-threat-modeling/python/src/auth_threat_modeling/scenarios.py](../../02-auth-threat-modeling/python/src/auth_threat_modeling/scenarios.py)
- [../../02-auth-threat-modeling/python/src/auth_threat_modeling/cli.py](../../02-auth-threat-modeling/python/src/auth_threat_modeling/cli.py)
- [../../02-auth-threat-modeling/python/tests/test_evaluator.py](../../02-auth-threat-modeling/python/tests/test_evaluator.py)
- [../../02-auth-threat-modeling/python/tests/test_cli.py](../../02-auth-threat-modeling/python/tests/test_cli.py)

## 읽는 순서

1. [00-series-map.md](00-series-map.md)
2. [10-chronology-control-vocabulary-scenarios-and-demo-findings.md](10-chronology-control-vocabulary-scenarios-and-demo-findings.md)
3. [../../02-auth-threat-modeling/README.md](../../02-auth-threat-modeling/README.md)

## 검증 진입점

```bash
cd ../../..
make venv
PYTHONPATH=study/02-auth-threat-modeling/python/src \
  .venv/bin/python -m pytest study/02-auth-threat-modeling/python/tests
PYTHONPATH=study/02-auth-threat-modeling/python/src \
  .venv/bin/python -m auth_threat_modeling.cli check-scenarios \
  study/02-auth-threat-modeling/problem/data/scenario_bundle.json
PYTHONPATH=study/02-auth-threat-modeling/python/src \
  .venv/bin/python -m auth_threat_modeling.cli demo \
  study/02-auth-threat-modeling/problem/data/demo_profile.json
```

## chronology 메모

- chronology는 `control vocabulary 고정 -> scenario bundle 대조 -> hybrid demo 출력` 순으로 복원했다.
- 핵심 전환점은 JWT, cookie session, OAuth를 기능 이름이 아니라 `AUTH-*` finding vocabulary로 통일한 지점이다.
