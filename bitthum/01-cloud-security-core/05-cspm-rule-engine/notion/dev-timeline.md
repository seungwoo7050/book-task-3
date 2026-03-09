# 05 CSPM Rule Engine — 개발 타임라인

이 문서는 프로젝트를 처음부터 다시 재현할 때 필요한 모든 단계를 순서대로 기록한다.

---

## 1단계: 환경 준비

기존 가상환경을 그대로 사용한다. 이 과제에서 추가로 필요한 외부 패키지는 `typer`뿐이다.

```bash
cd study2
make venv
```

---

## 2단계: 프로젝트 디렉토리 구조 생성

```
05-cspm-rule-engine/
├── README.md
├── docs/
│   ├── README.md
│   ├── concepts/
│   │   └── rule-design.md
│   └── references/
│       └── README.md
├── problem/
│   ├── README.md
│   └── data/
│       ├── access_keys_snapshot.json
│       ├── insecure_plan.json
│       └── secure_plan.json
└── python/
    ├── README.md
    ├── src/
    │   └── cspm_rule_engine/
    │       ├── __init__.py
    │       ├── cli.py
    │       └── scanner.py
    └── tests/
        └── test_scanner.py
```

```bash
mkdir -p 01-cloud-security-core/05-cspm-rule-engine/{docs/{concepts,references},problem/data,python/{src/cspm_rule_engine,tests}}
```

---

## 3단계: fixture 데이터 준비

### insecure_plan.json

과제 02의 `terraform/insecure/`에서 생성한 plan JSON을 기반으로 만들었다.
직접 Terraform을 실행하지 않고도 테스트할 수 있도록, plan JSON의 핵심 구조를 fixture로 복사했다.

핵심 구조:
```json
{
  "planned_values": {
    "root_module": {
      "resources": [
        { "type": "aws_s3_bucket_public_access_block", "name": "...", "values": { ... } },
        { "type": "aws_security_group", "name": "...", "values": { "ingress": [...] } },
        { "type": "aws_ebs_volume", "name": "...", "values": { "storage_encrypted": false } }
      ]
    }
  }
}
```

### secure_plan.json

같은 구조에서 안전한 설정값을 가진 fixture.
규칙 엔진이 이 입력에서 finding 0개를 반환하는지 확인하는 negative test용.

### access_keys_snapshot.json

```json
{
  "access_keys": [
    { "access_key_id": "AKIA...", "user": "deploy-bot", "age_days": 120 },
    { "access_key_id": "AKIA...", "user": "dev-user", "age_days": 30 }
  ]
}
```

120일짜리 키는 CSPM-004 finding이 발생하고, 30일짜리는 발생하지 않아야 한다.

---

## 4단계: 규칙 엔진 구현

### scanner.py 작성

구현 순서:

1. **Finding 데이터 클래스** — 과제 04와 동일한 7개 필드 구조

2. **_resources() 헬퍼** — plan JSON에서 `planned_values.root_module.resources` 추출

3. **scan_plan() 함수** — 네 가지 리소스 타입별 규칙:
   - `aws_s3_bucket_public_access_block`: 4개 플래그 전부 true인지 확인
   - `aws_security_group`: ingress에서 22/3389 포트 + 0.0.0.0/0 확인
   - `aws_db_instance` / `aws_ebs_volume`: `storage_encrypted` false 확인

4. **scan_access_keys() 함수** — `age_days > max_age_days` 확인
   - `max_age_days`는 기본 90일, 파라미터로 변경 가능

5. **findings_as_dicts() 유틸** — 직렬화

### cli.py 작성

두 개의 입력 경로를 받아서 plan scan + access key scan 결과를 합쳐 출력.

```bash
touch python/src/cspm_rule_engine/__init__.py
```

---

## 5단계: 테스트 작성

### test_scanner.py

세 가지 테스트:

1. **insecure plan → CSPM-001, 002, 003 동시 발동**
   - `controls == {"CSPM-001", "CSPM-002", "CSPM-003"}`

2. **secure plan → finding 없음**
   - `findings == []`

3. **access key snapshot → CSPM-004**
   - 120일 키에서만 finding 1개

---

## 6단계: 실행과 검증

### CLI 실행

```bash
cd python
PYTHONPATH=src python -m cspm_rule_engine.cli ../problem/data/insecure_plan.json ../problem/data/access_keys_snapshot.json
```

### 테스트 실행

```bash
cd study2
PYTHONPATH=01-cloud-security-core/05-cspm-rule-engine/python/src .venv/bin/python -m pytest 01-cloud-security-core/05-cspm-rule-engine/python/tests
```

또는:
```bash
make test-unit
```

### 타입 체크

```bash
.venv/bin/python -m mypy 01-cloud-security-core/05-cspm-rule-engine/python/src
```

---

## 환경 요약

| 항목 | 값 |
|------|-----|
| Python | 3.13+ |
| 핵심 의존성 | typer |
| 테스트 프레임워크 | pytest |
| AWS 계정 필요 여부 | 불필요 |
| 외부 서비스 의존 | 없음 |
| 입력 데이터 | Terraform plan JSON + access key snapshot JSON |
| 테스트 카테고리 | Unit |

---

## 주의사항

- insecure_plan.json과 secure_plan.json은 과제 02의 Terraform 설정에서 파생된 fixture다.
  실제 `terraform show -json` 출력의 전체 필드가 아닌, 규칙 엔진이 필요로 하는 최소 필드만 포함한다.
- `scan_plan`과 `scan_access_keys`는 독립적이다. 둘 중 하나만 실행해도 된다.
- 규칙 ID(CSPM-001~004)는 이 트랙 내에서만 유효한 커스텀 ID다. CIS나 AWS Config rule ID와 무관하다.
