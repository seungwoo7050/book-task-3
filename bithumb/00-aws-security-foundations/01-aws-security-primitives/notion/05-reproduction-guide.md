# 재현 가이드

## 무엇을 재현하나

- allow 요청이 실제로 허용되는지
- 더 구체적인 deny statement가 allow를 뒤집는지
- 매칭되는 allow가 없을 때 어떤 설명이 남는지

## 사전 조건

- `python3`가 3.13 이상이어야 `make venv`와 저장소 의존성 설치가 정상 동작합니다.
- 명령은 모두 레포 루트에서 실행합니다.

## 가장 짧은 재현 경로

```bash
make venv
PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src .venv/bin/python -m aws_security_primitives.cli explain 00-aws-security-foundations/01-aws-security-primitives/problem/data/policy_allow_read.json 00-aws-security-foundations/01-aws-security-primitives/problem/data/request_read.json
PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src .venv/bin/python -m pytest 00-aws-security-foundations/01-aws-security-primitives/python/tests
```

## 기대 결과

- CLI JSON에 `"allowed": true`와 `"reason": "at least one allow matched"`가 포함돼야 합니다.
- pytest는 `test_allow_matches_when_action_and_resource_match`, `test_explicit_deny_overrides_allow`, `test_request_denied_when_no_allow_statement_matches` 3개 테스트를 통과해야 합니다.
- 즉, allow/deny/implicit deny 세 규칙이 모두 고정돼야 이 프로젝트를 재현한 것으로 볼 수 있습니다.

## 결과가 다르면 먼저 볼 파일

- 평가 규칙이 이상하면: [../python/src/aws_security_primitives/engine.py](../python/src/aws_security_primitives/engine.py)
- CLI 출력 형식이 이상하면: [../python/src/aws_security_primitives/cli.py](../python/src/aws_security_primitives/cli.py)
- 입력 fixture가 기대와 다른지 확인하려면: [../problem/data/](../problem/data/)
- 검증 기준을 다시 보려면: [../python/tests/test_engine.py](../python/tests/test_engine.py)
- Python 버전 요구사항을 다시 보려면: [../../../pyproject.toml](../../../pyproject.toml)

## 이 재현이 증명하는 것

- 이 재현은 IAM 전부를 구현했다는 뜻이 아니라, 뒤 분석기와 캡스톤이 기대는 최소 평가 semantics를 안전하게 고정했다는 뜻입니다.
- 학습자가 이 단계에서 가져가야 할 핵심은 “policy를 읽는 법”보다 “결과를 설명하는 법”입니다.
