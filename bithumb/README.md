# AWS First Cloud Security Track

이 저장소는 AWS 보안 실습을 작은 문제 단위로 쪼개어 학습하고, 마지막에 하나의 로컬 control plane으로
통합해 보는 학습용 레포입니다. 목표는 정답 모음집을 만드는 것이 아니라, 문제 정의부터 검증과 한계 설명까지
스스로 정리할 수 있는 사람을 돕는 것입니다.

이 레포를 따라가는 사람은 두 가지 결과물을 얻을 수 있습니다.
- 클라우드 보안 실습을 단계적으로 따라가며 코드와 검증 흐름을 이해할 수 있습니다.
- 각 프로젝트의 설명 방식을 참고해, 자신의 공개용 포트폴리오 레포를 더 설득력 있게 다시 구성할 수 있습니다.

## 이 저장소를 읽는 순서

1. [docs/roadmap.md](docs/roadmap.md)에서 전체 학습 순서를 먼저 확인합니다.
2. 관심 있는 프로젝트의 `README.md`에서 문제 범위와 검증 명령을 파악합니다.
3. `problem/`으로 원래 문제를 확인하고, `python/`으로 현재 구현을 읽습니다.
4. `docs/`에서 개념 요약과 참고 자료를 확인합니다.
5. `notion/`에서 문제 정의, 접근 기록, 디버깅, 회고, 지식 인덱스를 따라갑니다.

## 트랙 구성

### 00 AWS Security Foundations

- `01-aws-security-primitives`: IAM 정책 평가의 가장 작은 핵심 규칙을 코드로 익힙니다.
- `02-terraform-aws-lab`: Terraform plan JSON을 보안 분석 입력으로 읽는 감각을 만듭니다.
- `03-cloudtrail-log-basics`: CloudTrail과 VPC Flow Logs를 질의 가능한 형태로 정규화합니다.

### 01 Cloud Security Core

- `04-iam-policy-analyzer`: broad permission과 privilege escalation 패턴을 finding으로 바꿉니다.
- `05-cspm-rule-engine`: misconfiguration 규칙 엔진을 로컬 fixture 기반으로 구현합니다.
- `06-remediation-pack-runner`: finding을 조치 제안과 승인 흐름으로 연결합니다.
- `07-security-lake-mini`: 보안 로그 적재와 detection query를 작은 lake 형태로 재현합니다.
- `08-container-guardrails`: Kubernetes manifest와 이미지 메타데이터에서 위험 설정을 찾습니다.
- `09-exception-and-evidence-manager`: 예외, 증적, 감사 흐름을 작은 모델로 정리합니다.

### 02 Capstone

- `10-cloud-security-control-plane`: 앞선 과제의 핵심 로직을 하나의 API, worker, 상태 저장소, 보고 흐름으로 통합합니다.

## 빠른 시작

모든 명령은 레포 루트에서 실행합니다.

```bash
make venv
make test-unit
make test-integration
make test-capstone
make demo-capstone
```

- `make doctor`: Python, Docker, Terraform이 준비됐는지 확인합니다.
- `make test-unit`: 단위 프로젝트 8개의 테스트를 실행합니다.
- `make test-integration`: Terraform 기반 실습 테스트를 실행합니다.
- `make test-capstone`: 캡스톤 테스트를 실행합니다.
- `make demo-capstone`: Docker daemon이 있으면 PostgreSQL, 없으면 SQLite fallback으로 데모 산출물을 만듭니다.

## 환경 준비 전에 확인할 점

- Python은 `3.13+`가 필요합니다. `python3 --version`이 3.12 이하면 `make venv` 단계에서 실패합니다.
- Docker Compose와 Terraform `1.5.x`는 일부 검증과 데모에 필요합니다.
- 가상환경이 꼬였으면 `.venv`를 삭제한 뒤 `make venv`로 다시 만드는 편이 가장 빠릅니다.

## 문서 정책

- tracked 문서는 문제 범위, 실행 방법, 검증 기준, 학습 포인트를 설명합니다.
- `notion/`은 이 레포에 포함되는 공개용 백업 문서입니다. 학습 기록과 회고를 남기되, 코드만 복사한 덤프가 되지 않도록 유지합니다.
- `notion/`을 다시 작성할 때는 기존 폴더를 `notion-archive/`로 보존하고 새 폴더를 생성합니다.
- 오래된 레포 이름이나 로컬 경로에 의존하는 표현은 쓰지 않고, 항상 “레포 루트 기준”으로 명령을 적습니다.

공통 문서 규칙은 [docs/documentation-policy.md](docs/documentation-policy.md)에서 확인할 수 있습니다.
