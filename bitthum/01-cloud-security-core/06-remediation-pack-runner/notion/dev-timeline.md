# 06 Remediation Pack Runner — 개발 타임라인

이 문서는 프로젝트를 처음부터 다시 재현할 때 필요한 모든 단계를 순서대로 기록한다.

---

## 1단계: 환경 준비

```bash
cd study2
make venv
```

이 과제에서 추가 패키지는 필요 없다. `typer`만 사용.

---

## 2단계: 프로젝트 디렉토리 구조 생성

```
06-remediation-pack-runner/
├── README.md
├── docs/
│   ├── README.md
│   ├── concepts/
│   │   └── dry-run-remediation.md
│   └── references/
│       └── README.md
├── problem/
│   ├── README.md
│   └── data/
│       └── sample_finding.json
└── python/
    ├── README.md
    ├── src/
    │   └── remediation_pack_runner/
    │       ├── __init__.py
    │       ├── cli.py
    │       └── runner.py
    └── tests/
        └── test_runner.py
```

```bash
mkdir -p 01-cloud-security-core/06-remediation-pack-runner/{docs/{concepts,references},problem/data,python/{src/remediation_pack_runner,tests}}
```

---

## 3단계: fixture 데이터 작성

### sample_finding.json

과제 05의 CSPM-001 finding 형태를 그대로 fixture로 만들었다.
`control_id`가 `"CSPM-001"`이고 `resource_id`가 S3 버킷 이름인 형태.

이 fixture가 `build_dry_run`의 입력이 되어 `auto_patch_available` 모드의 remediation plan을 생성한다.

---

## 4단계: 핵심 엔진 구현

### runner.py 작성

구현 순서:

1. **RemediationPlan 데이터 클래스 정의**
   - `finding_id`, `mode`, `summary`, `commands_or_patch`, `status`

2. **build_dry_run() 함수**
   - `control_id`에 따른 분기:
     - `CSPM-001` → Terraform patch (S3 퍼블릭 차단 플래그)
     - `CSPM-002` → AWS CLI 명령 제안 + 수동 승인 필요
     - 기타 → 수동 리뷰 가이드

3. **approve() 함수**
   - 기존 plan을 수정하지 않고 새 plan 반환 (불변성)
   - `status`를 `"approved"`로 변경
   - `summary`에 승인자 정보 추가

4. **as_dict() 유틸**

### cli.py 작성

finding JSON을 받아서 dry-run plan을 JSON으로 출력.

```bash
touch python/src/remediation_pack_runner/__init__.py
```

---

## 5단계: 테스트 작성

### test_runner.py

두 가지 테스트:

1. **build_dry_run이 CSPM-001에 대해 auto_patch plan을 반환하는지**
   - `mode == "auto_patch_available"` 확인
   - `commands_or_patch`에 `"block_public_acls"` 포함 확인
   - `status == "pending_approval"` 확인

2. **approve가 status를 변경하고 승인자를 기록하는지**
   - `status == "approved"` 확인
   - `"security.lead" in plan.summary` 확인

---

## 6단계: 실행과 검증

### CLI 실행

```bash
cd python
PYTHONPATH=src python -m remediation_pack_runner.cli ../problem/data/sample_finding.json
```

### 테스트 실행

```bash
cd study2
PYTHONPATH=01-cloud-security-core/06-remediation-pack-runner/python/src .venv/bin/python -m pytest 01-cloud-security-core/06-remediation-pack-runner/python/tests
```

또는:
```bash
make test-unit
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
| 테스트 카테고리 | Unit |

---

## 주의사항

- `build_dry_run`의 분기는 `control_id` 기반이다.
  알 수 없는 `control_id`가 들어오면 `manual_review` 모드로 fallback한다.
- `approve`는 새 객체를 반환한다. 원래 plan은 변경되지 않는다.
- `commands_or_patch`는 문자열 리스트이며, 실행 가능한 명령어와 설명 텍스트가 섞여 있다.
  실제 실행을 위해서는 파싱이 필요하다.
