# 05 CSPM Rule Engine evidence ledger

- 복원 원칙: 기존 blog 본문은 제외하고 `README/problem/docs`, scanner 소스, fixture JSON, CLI, pytest 재실행 결과만 근거로 썼다.
- 날짜 고정: 아래 실행 결과는 `2026-03-14` 기준이다.
- 프로젝트 성격: 이 engine은 plan과 snapshot을 하나의 finding 배열로 합친다.

## 사용한 입력 근거

- 설명 문서
  - `README.md`
  - `problem/README.md`
  - `python/README.md`
  - `docs/concepts/rule-design.md`
- 구현
  - `python/src/cspm_rule_engine/scanner.py`
  - `python/src/cspm_rule_engine/cli.py`
  - `problem/data/insecure_plan.json`
  - `problem/data/secure_plan.json`
  - `problem/data/access_keys_snapshot.json`
- 테스트
  - `python/tests/test_scanner.py`

## 다시 실행한 명령

```bash
PYTHONPATH=01-cloud-security-core/05-cspm-rule-engine/python/src \
  .venv/bin/python -m cspm_rule_engine.cli \
  01-cloud-security-core/05-cspm-rule-engine/problem/data/insecure_plan.json \
  01-cloud-security-core/05-cspm-rule-engine/problem/data/access_keys_snapshot.json

PYTHONPATH=01-cloud-security-core/05-cspm-rule-engine/python/src \
  .venv/bin/python -m pytest \
  01-cloud-security-core/05-cspm-rule-engine/python/tests
```

## 재실행 결과

- insecure plan + snapshot CLI -> `CSPM-001`, `CSPM-002`, `CSPM-003`, `CSPM-004`
- pytest -> `3 passed in 0.01s`

## 단계별 근거

### 1. plan resource dispatch로 misconfiguration을 잡았다

- 근거 소스: `_resources()`, `scan_plan()`
- 확인한 사실:
  - 입력은 `planned_values.root_module.resources`만 읽는다.
  - `aws_s3_bucket_public_access_block` 네 플래그 중 하나라도 false면 `CSPM-001`
  - `aws_security_group` ingress에서 22/3389와 `0.0.0.0/0` 조합이면 `CSPM-002`
  - `aws_db_instance`, `aws_ebs_volume`에서 `storage_encrypted == false`면 `CSPM-003`

### 2. snapshot rule을 같은 finding shape로 합쳤다

- 근거 소스: `scan_access_keys()`, access key snapshot, CLI 출력
- 확인한 사실:
  - `age_days > 90`이면 `CSPM-004`
  - source만 `access-key-snapshot`으로 다르고 나머지 필드 shape는 같다.
  - `AKIAOLD123` 한 건만 finding이 나온다.

### 3. secure plan 0건은 "plan scan" 기준이다

- 근거 소스: `test_secure_plan_reports_no_findings()`, CLI 구조
- 확인한 사실:
  - 테스트의 secure 0건은 `scan_plan(secure_plan)`만 검증한다.
  - CLI는 항상 `scan_plan(plan) + scan_access_keys(snapshot)`를 합치므로, secure plan에 같은 aged snapshot을 넣으면 여전히 `CSPM-004`가 남는다.
  - 따라서 "secure fixture 0건"은 plan layer의 false positive 기준이지, combined CLI 전체가 항상 0건이라는 뜻은 아니다. 이 문장은 테스트와 CLI 소스를 함께 본 source-based inference다.

## 남은 한계

- `problem/README.md`가 명시한 대로 drift detection, multi-account scan은 없다.
- `_resources()`는 root module만 읽기 때문에 nested module resource는 현재 규칙 대상이 아니다. 이 문장은 `scanner.py` 소스를 읽고 적은 source-based inference다.
- encryption rule은 `aws_db_instance`, `aws_ebs_volume` 두 타입만 본다.
