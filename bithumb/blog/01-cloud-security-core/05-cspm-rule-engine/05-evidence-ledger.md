# 05 CSPM Rule Engine 근거 정리

Terraform plan과 운영 snapshot을 함께 읽어 triage 가능한 misconfiguration finding으로 바꾸는 규칙 엔진이다. 이 문서는 그 흐름을 글로 풀기 전에, 실제 근거를 phase 단위로 다시 세워 둔 정리 노트다.

한 phase를 읽을 때는 `당시 목표 -> 실제 조치 -> CLI -> 검증 신호` 순서로 보면 무엇이 먼저 굳어졌는지 빠르게 따라갈 수 있다.

## Phase 1. Terraform plan 규칙부터 세웠다

이 구간에서는 `Terraform plan 규칙부터 세웠다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 1
- 당시 목표: 정적 plan JSON만으로 설명 가능한 misconfiguration을 먼저 잡는다.
- 변경 단위: `python/src/cspm_rule_engine/scanner.py`의 `_resources`, `scan_plan`
- 처음 가설: 좋은 CSPM v1은 규칙 수를 늘리기보다 입력 스키마가 선명한 몇 개 규칙을 정확히 잡는 쪽이 낫다.
- 실제 조치: `planned_values.root_module.resources`를 읽는 helper를 만들고, S3 public access block 플래그, SSH/RDP 0.0.0.0/0 ingress, storage encryption 비활성화를 각각 다른 control로 매핑했다. 각 finding에는 `evidence_ref`와 `resource_id`를 남겨 triage를 바로 이어갈 수 있게 했다.
- CLI:
  - `PYTHONPATH=01-cloud-security-core/05-cspm-rule-engine/python/src .venv/bin/python -m cspm_rule_engine.cli 01-cloud-security-core/05-cspm-rule-engine/problem/data/insecure_plan.json 01-cloud-security-core/05-cspm-rule-engine/problem/data/access_keys_snapshot.json`
- 검증 신호:
  - CLI 출력에 `CSPM-001`, `CSPM-002`, `CSPM-003`이 한 번에 나타났다.
  - `study2-public-logs`, `ssh_open`, `study2-analytics`처럼 remediation에 바로 쓸 resource_id가 남았다.
- 핵심 코드 앵커: `01-cloud-security-core/05-cspm-rule-engine/python/src/cspm_rule_engine/scanner.py:23-79`
- 새로 배운 것: 좋은 rule은 왜 발동했는지를 운영자가 바로 이해할 수 있어야 한다. input schema가 명확해야 false positive도 줄어든다.
- 다음: 이제 CSPM을 static plan에만 가두지 않고, 운영 snapshot까지 확장해 볼 차례였다.

## Phase 2. access key snapshot으로 입력 범위를 넓혔다

이 구간에서는 `access key snapshot으로 입력 범위를 넓혔다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 2
- 당시 목표: CSPM이 선언형 plan만 읽는 정적 분석에 머무르지 않도록 한다.
- 변경 단위: `python/src/cspm_rule_engine/scanner.py`의 `scan_access_keys`
- 처음 가설: 실무의 CSPM은 plan만으로 끝나지 않는다. 계정 상태 snapshot 같은 운영 데이터도 같은 finding shape로 묶어야 한다.
- 실제 조치: snapshot payload의 `access_keys`를 순회하면서 age가 90일을 넘으면 `CSPM-004`를 추가했다. source만 `access-key-snapshot`으로 다르게 주고, 나머지 필드는 plan findings와 같은 구조를 유지했다.
- CLI:
  - `PYTHONPATH=01-cloud-security-core/05-cspm-rule-engine/python/src .venv/bin/python -m cspm_rule_engine.cli 01-cloud-security-core/05-cspm-rule-engine/problem/data/insecure_plan.json 01-cloud-security-core/05-cspm-rule-engine/problem/data/access_keys_snapshot.json`
- 검증 신호:
  - CLI 출력 마지막에 `CSPM-004`와 `AKIAOLD123`가 나타났다.
  - 같은 JSON 배열 안에 `terraform-plan` source와 `access-key-snapshot` source가 함께 들어갔다.
- 핵심 코드 앵커: `01-cloud-security-core/05-cspm-rule-engine/python/src/cspm_rule_engine/scanner.py:82-97`
- 새로 배운 것: CSPM의 가치는 입력 종류를 늘리는 데 있는 게 아니라, 서로 다른 입력을 같은 triage 언어로 묶는 데 있다.
- 다음: 이제 secure fixture 0건과 output consistency를 테스트로 잠가 rule 품질을 고정해야 했다.

## Phase 3. secure fixture 0건을 품질 기준으로 삼았다

이 구간에서는 `secure fixture 0건을 품질 기준으로 삼았다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 3
- 당시 목표: 불필요한 finding이 나오지 않는 기준선을 만든다.
- 변경 단위: `python/tests/test_scanner.py`
- 처음 가설: insecure fixture에서 많이 잡는 것보다 secure fixture에서 조용해야 rule engine이 실제로 쓸 만하다.
- 실제 조치: 테스트는 insecure plan에서 세 control이 모두 나오는지, secure plan에서는 0건인지, access key snapshot에서는 오래된 키 한 건만 잡히는지 확인했다. 이 세 축이 있어야 ruleset이 과하게 noisy해지지 않는다.
- CLI:
  - `PYTHONPATH=01-cloud-security-core/05-cspm-rule-engine/python/src .venv/bin/python -m pytest 01-cloud-security-core/05-cspm-rule-engine/python/tests`
- 검증 신호:
  - pytest가 `3 passed in 0.01s`로 통과했다.
  - `test_secure_plan_reports_no_findings`가 ruleset의 상한선을 정했다.
- 핵심 코드 앵커: `01-cloud-security-core/05-cspm-rule-engine/python/tests/test_scanner.py:12-26`
- 새로 배운 것: false positive는 rule 수보다 input 경계가 흐릴 때 생기기 쉽다. secure fixture는 그 경계를 테스트 코드로 고정하는 장치다.
- 다음: 다음 프로젝트는 이 finding을 바로 실행하지 않고, review 가능한 remediation plan으로 바꾼다.
