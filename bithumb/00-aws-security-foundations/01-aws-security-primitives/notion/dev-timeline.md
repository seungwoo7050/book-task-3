# 01 AWS Security Primitives — 개발 타임라인

이 문서는 프로젝트를 처음부터 다시 재현할 때 필요한 모든 단계를 순서대로 기록한다.
소스코드만으로는 알 수 없는 환경 설정, CLI 명령, 설치 과정, 판단 근거를 담고 있다.

---

## 1단계: 프로젝트 환경 준비

### Python 가상환경 생성

프로젝트 루트(`study2/`)에서 공용 가상환경을 만든다.
모든 과제가 같은 가상환경을 공유하는 구조여서, 과제별로 따로 만들지 않는다.

```bash
cd study2
python3 -m venv .venv
source .venv/bin/activate
```

### 의존성 설치

`pyproject.toml`에 정의된 패키지를 설치한다.
이 과제에서 직접 사용하는 패키지는 `typer`뿐이지만,
루트의 `pyproject.toml`로 전체 트랙 의존성을 한 번에 설치한다.

```bash
pip install --upgrade pip
pip install -e ".[dev]"
```

설치되는 핵심 패키지:
- `typer`: CLI 인터페이스
- `pytest`: 테스트 실행
- `ruff`: 린팅
- `mypy`: 타입 체크

### Makefile을 통한 간편 설치

위 과정을 `make venv`로 대체할 수 있다.

```bash
make venv
```

---

## 2단계: 프로젝트 디렉토리 구조 생성

```
01-aws-security-primitives/
├── README.md
├── docs/
│   ├── README.md
│   ├── concepts/
│   │   └── iam-basics.md
│   └── references/
│       └── README.md
├── problem/
│   ├── README.md
│   └── data/
│       ├── policy_allow_read.json
│       └── request_read.json
└── python/
    ├── README.md
    ├── src/
    │   └── aws_security_primitives/
    │       ├── __init__.py
    │       ├── cli.py
    │       └── engine.py
    └── tests/
        └── test_engine.py
```

디렉토리를 생성하는 순서:

```bash
mkdir -p 00-aws-security-foundations/01-aws-security-primitives/{docs/{concepts,references},problem/data,python/{src/aws_security_primitives,tests}}
```

---

## 3단계: fixture 데이터 작성

코드를 작성하기 전에 입출력 예제를 먼저 만들었다.

### policy_allow_read.json

S3 읽기 권한만 허용하는 단순한 정책이다.
`s3:GetObject`와 `s3:ListBucket` 두 가지 액션만 허용하고,
`study2-logs` 버킷으로 리소스를 한정했다.

```bash
cat > problem/data/policy_allow_read.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowRead",
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": ["arn:aws:s3:::study2-logs", "arn:aws:s3:::study2-logs/*"]
    }
  ]
}
EOF
```

### request_read.json

정책에 매칭되는 단순 읽기 요청이다.

```bash
cat > problem/data/request_read.json << 'EOF'
{
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::study2-logs/app.log"
}
EOF
```

---

## 4단계: 핵심 엔진 구현

### engine.py 작성

`python/src/aws_security_primitives/engine.py`에 핵심 로직을 작성했다.

구현 순서:
1. `_as_list` 유틸: IAM statement에서 Action/Resource가 문자열일 수도 리스트일 수도 있어서 통일하는 함수
2. `StatementResult`, `Decision` 데이터 클래스: 평가 결과를 구조화
3. `_matches` 함수: `fnmatch.fnmatchcase`를 사용한 wildcard 패턴 매칭
4. `evaluate_policy` 함수: 핵심 평가 루프 — 모든 statement를 순회하며 deny/allow를 수집하고, deny가 하나라도 있으면 거부

### cli.py 작성

`python/src/aws_security_primitives/cli.py`에 Typer 기반 CLI를 작성했다.

- `explain` 명령: policy JSON과 request JSON을 받아 결정 결과를 JSON으로 출력
- Typer의 `Path` 타입을 사용해 파일 경로를 자동 검증

### `__init__.py`

빈 파일로 생성. 패키지 인식용.

```bash
touch python/src/aws_security_primitives/__init__.py
```

---

## 5단계: 테스트 작성

### test_engine.py 작성

세 가지 시나리오를 테스트로 작성했다:

1. **Allow 매칭**: Action과 Resource가 모두 맞을 때 허용
2. **Explicit Deny Override**: Allow statement가 먼저 있어도 Deny가 매칭되면 거부
3. **Implicit Deny**: 어떤 Allow statement도 매칭되지 않을 때 기본 거부

이 세 테스트가 IAM 평가의 핵심 세 가지 경로를 전부 커버한다.

---

## 6단계: 실행과 검증

### CLI 실행

```bash
cd python
PYTHONPATH=src python -m aws_security_primitives.cli explain ../problem/data/policy_allow_read.json ../problem/data/request_read.json
```

출력 예시:
```json
{
  "allowed": true,
  "reason": "at least one allow matched",
  "matches": [
    {
      "sid": "AllowRead",
      "effect": "Allow",
      "matched": true,
      "reason": "action/resource matched"
    }
  ]
}
```

### 테스트 실행

프로젝트 디렉토리에서 직접 실행:

```bash
cd python
PYTHONPATH=src python -m pytest tests
```

루트에서 Makefile을 통해 실행:

```bash
cd study2
make test-unit
```

`make test-unit`은 모든 unit test 대상 프로젝트를 순회하며 테스트를 실행한다.
이 과제는 `UNIT_DIRS`에 포함되어 있다.

### 타입 체크와 린팅

```bash
cd study2
.venv/bin/python -m mypy 00-aws-security-foundations/01-aws-security-primitives/python/src
.venv/bin/python -m ruff check 00-aws-security-foundations/01-aws-security-primitives/python
```

---

## 7단계: 문서 작성

- `README.md`: 프로젝트 상태, 빌드/테스트 명령, 학습 포인트
- `docs/concepts/iam-basics.md`: IAM 평가 핵심 규칙 요약
- `docs/references/README.md`: AWS 공식 문서 참조 링크
- `problem/README.md`: 과제 정의 (입출력 명세)
- `python/README.md`: 구현 범위, 빌드 명령, 알려진 한계

---

## 환경 요약

| 항목 | 값 |
|------|-----|
| Python | 3.13+ |
| 핵심 의존성 | typer |
| 테스트 프레임워크 | pytest |
| 린팅 | ruff |
| 타입 체크 | mypy |
| AWS 계정 필요 여부 | 불필요 |
| 외부 서비스 의존 | 없음 |

---

## 주의사항

- `PYTHONPATH=src`를 반드시 설정해야 한다. 이 프로젝트는 설치 가능한 패키지가 아니라
  `src` 디렉토리를 직접 참조하는 구조다.
- `pyproject.toml`에서 `requires-python = ">=3.13"`이므로 3.13 미만에서는 실행되지 않는다.
- fixture JSON은 실제 AWS 정책과 같은 구조지만, 실제 AWS API를 호출하지 않는다.
