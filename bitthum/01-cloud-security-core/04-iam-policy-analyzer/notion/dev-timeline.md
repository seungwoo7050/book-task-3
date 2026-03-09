# 04 IAM Policy Analyzer — 개발 타임라인

이 문서는 프로젝트를 처음부터 다시 재현할 때 필요한 모든 단계를 순서대로 기록한다.
소스코드만으로는 알 수 없는 fixture 설계 의도, 탐지 규칙 결정 과정을 담고 있다.

---

## 1단계: 환경 준비

이전 과제에서 이미 만든 가상환경을 그대로 사용한다.
이 과제에서 추가로 필요한 외부 패키지는 `typer`뿐이며, 이미 설치되어 있다.

```bash
cd study2
make venv
```

---

## 2단계: 프로젝트 디렉토리 구조 생성

```
04-iam-policy-analyzer/
├── README.md
├── docs/
│   ├── README.md
│   ├── concepts/
│   │   └── least-privilege-findings.md
│   └── references/
│       └── README.md
├── problem/
│   ├── README.md
│   └── data/
│       ├── broad_admin_policy.json
│       ├── passrole_policy.json
│       └── scoped_policy.json
└── python/
    ├── README.md
    ├── src/
    │   └── iam_policy_analyzer/
    │       ├── __init__.py
    │       ├── analyzer.py
    │       └── cli.py
    └── tests/
        └── test_analyzer.py
```

```bash
mkdir -p 01-cloud-security-core/04-iam-policy-analyzer/{docs/{concepts,references},problem/data,python/{src/iam_policy_analyzer,tests}}
```

---

## 3단계: fixture 데이터 작성

세 가지 정책 fixture를 만들었다. 각각 다른 탐지 시나리오를 대표한다.

### broad_admin_policy.json

```json
{
  "Statement": [{
    "Effect": "Allow",
    "Action": "*",
    "Resource": "*"
  }]
}
```

가장 위험한 정책. IAM-001(모든 액션)과 IAM-002(모든 리소스) 두 finding이 동시에 발생해야 한다.

### passrole_policy.json

`iam:PassRole`을 포함하는 정책. IAM-003(privilege escalation) finding이 발생해야 한다.

### scoped_policy.json

`s3:GetObject`만 특정 버킷에 허용. finding이 0개여야 한다.
이 "negative test"가 false positive 검증에 필수적이다.

---

## 4단계: 핵심 분석 엔진 구현

### analyzer.py 작성

구현 순서:

1. **상수 정의**
   - `HIGH_RISK_ACTIONS`: privilege escalation 가능 액션 5개
   - `READ_ONLY_PREFIXES`: false positive 필터링용 읽기 전용 액션 접두사

2. **Finding 데이터 클래스 정의**
   - 7개 필드: `source`, `control_id`, `severity`, `resource_type`, `resource_id`, `title`, `evidence_ref`
   - 이 Finding 구조는 과제 05, 06, 10에서도 동일하게 사용

3. **analyze_policy() 함수**
   - Allow statement만 분석 (Deny는 스킵)
   - 세 가지 규칙을 순서대로 적용:
     - IAM-001: `"*" in actions`
     - IAM-002: `"*" in resources` AND 읽기 전용이 아닌 액션 존재
     - IAM-003: `HIGH_RISK_ACTIONS`와 교집합

4. **findings_as_dicts() 유틸**
   - `dataclasses.asdict`로 직렬화 (CLI 출력용)

### cli.py 작성

Typer 기반 CLI. policy JSON 경로를 받아서 finding 리스트를 JSON으로 출력한다.

```bash
touch python/src/iam_policy_analyzer/__init__.py
```

---

## 5단계: 테스트 작성

### test_analyzer.py

세 가지 테스트:

1. **broad_admin_policy → IAM-001, IAM-002 동시 발동**
   - control_id 집합이 `{"IAM-001", "IAM-002"}`와 일치하는지 확인

2. **passrole_policy → IAM-003 발동**
   - `any(finding.control_id == "IAM-003")`로 확인

3. **scoped_policy → finding 없음**
   - `findings == []`로 확인
   - 이 테스트가 false positive 검증의 핵심

---

## 6단계: 실행과 검증

### CLI 실행

```bash
cd python
PYTHONPATH=src python -m iam_policy_analyzer.cli ../problem/data/broad_admin_policy.json
```

출력 예시:
```json
[
  {
    "source": "iam-policy",
    "control_id": "IAM-001",
    "severity": "HIGH",
    "resource_type": "iam-policy",
    "resource_id": "Statement1",
    "title": "Policy allows every action",
    "evidence_ref": "Statement1"
  },
  {
    "source": "iam-policy",
    "control_id": "IAM-002",
    "severity": "HIGH",
    "resource_type": "iam-policy",
    "resource_id": "Statement1",
    "title": "Policy applies to every resource",
    "evidence_ref": "Statement1"
  }
]
```

### 다른 fixture도 확인

```bash
PYTHONPATH=src python -m iam_policy_analyzer.cli ../problem/data/passrole_policy.json
PYTHONPATH=src python -m iam_policy_analyzer.cli ../problem/data/scoped_policy.json
```

scoped_policy는 빈 배열 `[]`이 출력되어야 한다.

### 테스트 실행

```bash
cd study2
PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src .venv/bin/python -m pytest 01-cloud-security-core/04-iam-policy-analyzer/python/tests
```

또는:
```bash
make test-unit
```

### 타입 체크

```bash
.venv/bin/python -m mypy 01-cloud-security-core/04-iam-policy-analyzer/python/src
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

- Finding의 `resource_id`는 statement의 `Sid` 필드를 그대로 사용한다.
  Sid가 없는 statement는 `"Statement{index}"` 형태로 자동 생성된다.
- 같은 statement에서 여러 finding이 동시에 발생할 수 있다 (IAM-001 + IAM-002).
- `analyze_policy`는 `Deny` effect의 statement를 완전히 무시한다.
  Deny statement는 "위험한 설정"이 아니라 "제한하는 설정"이기 때문이다.
