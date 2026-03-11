# Python 구현

아래 내용은 모두 레포 루트 기준입니다.

## 구현한 답의 범위

- Terraform plan JSON misconfiguration을 탐지합니다.
- S3 public access, open ingress, storage encryption, access key age를 검사합니다.
- 운영자가 바로 triage할 수 있는 finding 형태로 결과를 반환합니다.

## 핵심 엔트리포인트

- `python/src/cspm_rule_engine/scanner.py`
- `python/src/cspm_rule_engine/cli.py`

## 실행

```bash
make venv
PYTHONPATH=01-cloud-security-core/05-cspm-rule-engine/python/src .venv/bin/python -m cspm_rule_engine.cli 01-cloud-security-core/05-cspm-rule-engine/problem/data/insecure_plan.json 01-cloud-security-core/05-cspm-rule-engine/problem/data/access_keys_snapshot.json
```

## 테스트

```bash
PYTHONPATH=01-cloud-security-core/05-cspm-rule-engine/python/src .venv/bin/python -m pytest 01-cloud-security-core/05-cspm-rule-engine/python/tests
```

## 대표 출력 예시

```json
[
  {
    "source": "terraform-plan",
    "control_id": "CSPM-001",
    "severity": "HIGH",
    "resource_type": "aws_s3_bucket_public_access_block",
    "resource_id": "study2-public-logs",
    "title": "S3 bucket does not fully block public access",
    "evidence_ref": "public_logs"
  }
]
```

## 구현 메모

규칙 엔진은 입력 스키마가 분명한 fixture를 전제로 해서 테스트와 데모에서 반복 사용하기 쉽습니다.
