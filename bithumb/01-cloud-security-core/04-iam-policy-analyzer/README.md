# 04 IAM Policy Analyzer

## 풀려는 문제

정책 평가 결과만으로는 운영자가 무엇이 위험한지 바로 알기 어렵습니다.
이 프로젝트는 IAM policy를 least privilege 관점의 finding으로 바꿔, 정책 위험을 triage 가능한 형태로 설명하는 것을 목표로 합니다.

## 내가 낸 답

- broad admin 정책과 scoped policy를 구분합니다.
- `iam:PassRole` 같은 privilege escalation 패턴을 별도 고위험 finding으로 분리합니다.
- finding마다 `control_id`, `severity`, `resource_id`, `evidence_ref`를 반환해 remediation으로 연결하기 쉽게 만듭니다.
- safe fixture에서 0건이 나오는 조건을 함께 검증해 false positive를 줄입니다.

## 입력과 출력

- 입력: `problem/data/broad_admin_policy.json`, `problem/data/passrole_policy.json`, `problem/data/scoped_policy.json`
- 출력: least privilege finding 목록과 severity, 설명, 근거 필드

## 검증 방법

```bash
make venv
PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src .venv/bin/python -m iam_policy_analyzer.cli 01-cloud-security-core/04-iam-policy-analyzer/problem/data/broad_admin_policy.json
PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src .venv/bin/python -m pytest 01-cloud-security-core/04-iam-policy-analyzer/python/tests
```

## 현재 상태

- `verified`
- broad admin, escalation, safe policy 0건 시나리오를 테스트로 고정했습니다.
- 06번 remediation runner와 10번 캡스톤이 이 finding 구조를 그대로 재사용합니다.

## 한계와 다음 단계

- SCP, permission boundary, condition-based privilege narrowing은 v1 범위 밖입니다.
- 조직 전체 권한 그래프 분석까지는 하지 않고, remediation과 control plane 연결에 필요한 finding layer까지만 다룹니다.

## 더 깊게 읽을 문서

- [problem/README.md](problem/README.md)
- [python/README.md](python/README.md)
- [docs/README.md](docs/README.md)
- [notion/README.md](notion/README.md)
