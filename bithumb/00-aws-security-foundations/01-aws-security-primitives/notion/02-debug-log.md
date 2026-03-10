# 디버그 로그

## 실제로 자주 막히는 지점

- `explicit deny`는 statement의 위치가 아니라 우선순위로 동작합니다. allow 뒤에 deny가 와도 결과를 뒤집습니다.
- `Action`만 맞고 `Resource`가 다르면 부분 성공이 아니라 불일치입니다. archive 기록에서도 이 지점을 초기에 착각했습니다.
- wildcard는 편하지만, 어떤 값이 매칭되는지 눈으로만 판단하면 실수하기 쉽습니다. 테스트 fixture로 고정해 두는 편이 낫습니다.

## 이미 확인된 테스트 시나리오

- `test_allow_matches_when_action_and_resource_match`: 가장 기본적인 allow 경로가 살아 있는지 확인합니다.
- `test_explicit_deny_overrides_allow`: deny가 전체 결과를 뒤집는 핵심 규칙을 고정합니다.
- `test_request_denied_when_no_allow_statement_matches`: allow 부재 시 implicit deny가 동작하는지 확인합니다.

## 다시 검증할 명령

```bash
PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src .venv/bin/python -m pytest 00-aws-security-foundations/01-aws-security-primitives/python/tests
```

## 실패하면 먼저 볼 곳

- 테스트 근거: [../python/tests/test_engine.py](../python/tests/test_engine.py)
- 실행 예시: [../python/README.md](../python/README.md)
- 이전 장문 설명: [../notion-archive/essay.md](../notion-archive/essay.md)
