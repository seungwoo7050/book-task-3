# 재현 가이드

## 무엇을 재현하나

- Terraform misconfiguration 세 가지와 오래된 access key 한 가지가 모두 찾아지는지
- secure plan이 0건으로 통과해 rule precision이 유지되는지
- finding 출력이 remediation으로 넘길 수 있는 형태인지

## 사전 조건

- `python3` 3.13+와 `make venv`가 필요합니다.
- 명령은 모두 레포 루트에서 실행합니다.
- 이 프로젝트는 학습 재현성에 가장 직접적인 문서이므로, CLI 결과와 테스트 결과를 둘 다 확인하는 편이 좋습니다.

## 가장 짧은 재현 경로

```bash
make venv
PYTHONPATH=01-cloud-security-core/05-cspm-rule-engine/python/src .venv/bin/python -m cspm_rule_engine.cli scan 01-cloud-security-core/05-cspm-rule-engine/problem/data/insecure_plan.json 01-cloud-security-core/05-cspm-rule-engine/problem/data/access_keys_snapshot.json
PYTHONPATH=01-cloud-security-core/05-cspm-rule-engine/python/src .venv/bin/python -m pytest 01-cloud-security-core/05-cspm-rule-engine/python/tests
```

## 기대 결과

- CLI JSON에는 최소한 `CSPM-001`, `CSPM-002`, `CSPM-003`, `CSPM-004` 네 control이 포함돼야 합니다.
- pytest는 3개 테스트를 통과해야 하며, insecure plan 3건, secure plan 0건, old access key 1건이라는 세 기준을 동시에 검증합니다.
- 이때 secure plan에서 결과가 비어 있지 않다면, 규칙 엔진을 재현한 것이 아니라 오탐을 늘린 것입니다.

## 결과가 다르면 먼저 볼 파일

- rule 구현을 다시 보려면: [../python/src/cspm_rule_engine/scanner.py](../python/src/cspm_rule_engine/scanner.py)
- CLI 진입 흐름을 다시 보려면: [../python/src/cspm_rule_engine/cli.py](../python/src/cspm_rule_engine/cli.py)
- insecure/secure 입력을 비교하려면: [../problem/data/](../problem/data/)
- 검증 기준을 다시 보려면: [../python/tests/test_scanner.py](../python/tests/test_scanner.py)
- 루트 공통 검증 흐름을 다시 보려면: [../../../Makefile](../../../Makefile)

## 이 재현이 증명하는 것

- 이 재현은 CSPM이 “설정을 읽어 설명 가능한 finding을 만드는 작은 규칙 엔진”이라는 것을 가장 압축적으로 보여 줍니다.
- 학습자가 이 문서를 통해 얻어야 할 핵심은 검출 건수 자랑이 아니라, insecure와 secure를 같은 기준으로 다루는 rule 설계 습관입니다.
