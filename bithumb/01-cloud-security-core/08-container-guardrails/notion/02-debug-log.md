# 디버그 로그

## 실제로 자주 막히는 지점

- Deployment는 `spec.template.spec.containers`를 읽어야 합니다. `spec.containers`만 보면 컨테이너를 찾지 못합니다.
- `runAsUser`가 명시되지 않으면 기본값을 0으로 해석하는 현재 규칙 때문에 오탐/과탐 기준을 스스로 설명해야 합니다.
- `privileged: true`와 `capabilities.add: ["ALL"]`은 비슷해 보여도 별도 규칙으로 유지해야 합니다.

## 이미 확인된 테스트 시나리오

- `test_insecure_inputs_report_expected_findings`: insecure manifest + image에서 여덟 규칙 집합이 모두 나오는지 확인합니다.
- `test_secure_inputs_report_no_findings`: secure 입력에서 finding 0건인지 확인합니다.

## 다시 검증할 명령

```bash
PYTHONPATH=01-cloud-security-core/08-container-guardrails/python/src .venv/bin/python -m pytest 01-cloud-security-core/08-container-guardrails/python/tests
```

## 실패하면 먼저 볼 곳

- 테스트 코드: [../python/tests/test_scanner.py](../python/tests/test_scanner.py)
- 구현 진입점: [../python/src/container_guardrails/scanner.py](../python/src/container_guardrails/scanner.py)
- 이전 설명: [../notion-archive/essay.md](../notion-archive/essay.md)
