# 05 CSPM Rule Engine

## 풀려는 문제

Terraform plan과 운영 snapshot을 읽고, 운영자가 바로 triage할 수 있는 misconfiguration finding을 만들어야 합니다.
이 프로젝트는 CSPM을 막연한 제품명이 아니라, 설명 가능한 규칙 묶음으로 재구성하는 데 집중합니다.

## 내가 낸 답

- Terraform plan JSON과 access key snapshot을 함께 읽어 인프라와 계정 위험을 한 흐름에서 평가합니다.
- S3 public access, open ingress, storage encryption, access key age를 규칙으로 구현합니다.
- 결과를 `severity`, `control_id`, `evidence_ref`가 있는 finding으로 반환합니다.
- insecure fixture에서 위험을 잡고 secure fixture에서 조용히 통과하는 기준을 같이 검증합니다.

## 입력과 출력

- 입력: `problem/data/insecure_plan.json`, `problem/data/secure_plan.json`, `problem/data/access_keys_snapshot.json`
- 출력: triage 가능한 misconfiguration finding 목록과 remediation 힌트 필드

## 검증 방법

```bash
make venv
PYTHONPATH=01-cloud-security-core/05-cspm-rule-engine/python/src .venv/bin/python -m cspm_rule_engine.cli 01-cloud-security-core/05-cspm-rule-engine/problem/data/insecure_plan.json 01-cloud-security-core/05-cspm-rule-engine/problem/data/access_keys_snapshot.json
PYTHONPATH=01-cloud-security-core/05-cspm-rule-engine/python/src .venv/bin/python -m pytest 01-cloud-security-core/05-cspm-rule-engine/python/tests
```

## 현재 상태

- `verified`
- Terraform plan과 snapshot을 함께 읽는 규칙 묶음을 fixture와 테스트로 재현할 수 있습니다.
- 06번 remediation과 10번 캡스톤에서 그대로 이어받을 finding 구조를 제공합니다.

## 한계와 다음 단계

- v1 rule set은 S3, Security Group, encryption, access key age로 제한합니다.
- 실제 계정 전체 스캔이나 drift detection은 다루지 않고, local fixture 기반 규칙 설계에 집중합니다.

## 더 깊게 읽을 문서

- [problem/README.md](problem/README.md)
- [python/README.md](python/README.md)
- [docs/README.md](docs/README.md)
- [notion/README.md](notion/README.md)
