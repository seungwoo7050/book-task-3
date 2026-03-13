# 05 CSPM Rule Engine 구조 메모

이 문서는 최종 글을 쓰기 전에 서사 배치를 점검하는 메모다. 독자에게 무엇을 먼저 설명하고 어디서 코드와 CLI를 꺼내 올지 한눈에 보이도록 정리한다.

## 이번 문서가 맡는 일
- Terraform plan과 운영 snapshot에서 triage 가능한 misconfiguration을 뽑는 규칙 엔진으로 프로젝트를 읽는다.
- 서사는 `plan 규칙 -> snapshot 확장 -> secure fixture 0건` 순서를 유지해 범위 확장과 품질 상한선을 함께 보이게 한다.

## 먼저 붙들 소스 묶음
- [`../../../01-cloud-security-core/05-cspm-rule-engine/README.md`](../../../01-cloud-security-core/05-cspm-rule-engine/README.md)
- [`../../../01-cloud-security-core/05-cspm-rule-engine/problem/README.md`](../../../01-cloud-security-core/05-cspm-rule-engine/problem/README.md)
- [`../../../01-cloud-security-core/05-cspm-rule-engine/docs/concepts/rule-design.md`](../../../01-cloud-security-core/05-cspm-rule-engine/docs/concepts/rule-design.md)
- [`../../../01-cloud-security-core/05-cspm-rule-engine/python/README.md`](../../../01-cloud-security-core/05-cspm-rule-engine/python/README.md)
- [`../../../01-cloud-security-core/05-cspm-rule-engine/python/src/cspm_rule_engine/scanner.py`](../../../01-cloud-security-core/05-cspm-rule-engine/python/src/cspm_rule_engine/scanner.py)
- [`../../../01-cloud-security-core/05-cspm-rule-engine/python/src/cspm_rule_engine/cli.py`](../../../01-cloud-security-core/05-cspm-rule-engine/python/src/cspm_rule_engine/cli.py)
- [`../../../01-cloud-security-core/05-cspm-rule-engine/python/tests/test_scanner.py`](../../../01-cloud-security-core/05-cspm-rule-engine/python/tests/test_scanner.py)

## 본문을 배치하는 순서

- `00-series-map.md`
  - plan JSON과 snapshot 두 입력이 왜 같은 프로젝트에 묶이는지, 어떤 verify로 읽을지 먼저 고정한다.
- `10-development-timeline.md`
  - 도입: CSPM을 단순 policy lint가 아니라 triage engine으로 보는 시점을 잡는다.
  - Phase 1. Terraform plan 규칙부터 세웠다.
  - Phase 2. access key snapshot으로 입력 범위를 넓혔다.
  - Phase 3. secure fixture 0건을 품질 기준으로 삼았다.
  - 마무리: 다음 remediation runner가 왜 finding control ID를 입력 계약으로 쓰게 되는지 넘긴다.

## 강조할 코드와 CLI
- 코드 앵커: resource dispatch, `CSPM-001`/`002`/`003`/`010` rule blocks, CLI output schema, secure fixture assertions
- CLI 앵커: `python -m cspm_rule_engine.cli ...`, `pytest 01-cloud-security-core/05-cspm-rule-engine/python/tests`
- 개념 훅: good CSPM rule은 많이 잡는 규칙이 아니라 triage 가능한 finding을 내는 규칙이라는 점

## 리라이트 기준
- chronology는 실제 commit timestamp보다 source, test, CLI가 묶이는 순서를 기준으로 읽는다.
- 이 문서는 메타 기록보다 서사 배치와 강조점에 집중한다.
