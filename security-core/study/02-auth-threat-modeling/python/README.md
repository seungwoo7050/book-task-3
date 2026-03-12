# Python 구현

## 구현 개요

이 구현은 auth scenario manifest를 읽어 control gap을 `AUTH-*` finding으로 바꾸는 Python evaluator 패키지입니다.

## 핵심 모듈

- `src/auth_threat_modeling/evaluator.py`: control meta와 scenario 판정 로직
- `src/auth_threat_modeling/scenarios.py`: manifest 로딩, summary 계산, demo profile 변환
- `src/auth_threat_modeling/cli.py`: `check-scenarios`, `demo` 명령 공개

## CLI 계약

```bash
PYTHONPATH=study/02-auth-threat-modeling/python/src \
  .venv/bin/python -m auth_threat_modeling.cli check-scenarios \
  study/02-auth-threat-modeling/problem/data/scenario_bundle.json
```

- `check-scenarios <manifest>`: `passed`, `failed`, `scenarios`를 JSON으로 출력합니다.
- `demo <profile>`: `control_ids`와 `findings`를 JSON으로 출력합니다.

## 테스트

```bash
make test-unit
```

실제 login server, provider callback, JWKS fetch 없이도 auth control vocabulary를 설명 가능한 finding으로 바꾸는 데 집중합니다.
