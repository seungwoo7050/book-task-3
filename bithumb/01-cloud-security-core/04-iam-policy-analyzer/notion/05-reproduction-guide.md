# 재현 가이드

## 무엇을 재현하나

- broad policy가 여러 finding으로 분해되는지
- `iam:PassRole`이 별도 escalation risk로 잡히는지
- scoped policy가 0건으로 통과해 오탐 억제 기준이 유지되는지

## 사전 조건

- `python3` 3.13+와 `make venv`가 필요합니다.
- 명령은 모두 레포 루트에서 실행합니다.

## 가장 짧은 재현 경로

```bash
make venv
PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src .venv/bin/python -m iam_policy_analyzer.cli analyze 01-cloud-security-core/04-iam-policy-analyzer/problem/data/broad_admin_policy.json
PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src .venv/bin/python -m pytest 01-cloud-security-core/04-iam-policy-analyzer/python/tests
```

## 기대 결과

- CLI JSON에는 최소한 `IAM-001`과 `IAM-002` control이 포함돼야 합니다.
- pytest는 3개 테스트를 통과하면서 broad admin, passrole escalation, scoped safe policy를 각각 검증해야 합니다.
- safe policy에서 결과가 빈 리스트가 아니면 이 analyzer의 품질 설명이 무너집니다.

## 결과가 다르면 먼저 볼 파일

- 분석 규칙이 이상하면: [../python/src/iam_policy_analyzer/analyzer.py](../python/src/iam_policy_analyzer/analyzer.py)
- CLI 출력 형식이 이상하면: [../python/src/iam_policy_analyzer/cli.py](../python/src/iam_policy_analyzer/cli.py)
- 입력 fixture를 다시 보려면: [../problem/data/](../problem/data/)
- 검증 기준을 다시 보려면: [../python/tests/test_analyzer.py](../python/tests/test_analyzer.py)
- 루트 검증 흐름을 다시 보려면: [../../../Makefile](../../../Makefile)

## 이 재현이 증명하는 것

- 이 재현은 정책 평가 결과를 운영자가 읽는 finding으로 바꾸는 첫 단계가 안정적으로 동작한다는 뜻입니다.
- 학습자는 여기서 “잡아내는 것”뿐 아니라 “안전한 것은 조용히 통과시키는 것”도 같은 비중으로 설명할 수 있어야 합니다.
