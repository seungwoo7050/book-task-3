# AWS-First Cloud Security Track

이 레포는 AWS 보안 학습을 10개의 작은 문제로 쪼개고, 마지막에 하나의 local control plane으로 다시 묶는
학습용 결과물 저장소입니다. 핵심은 코드를 많이 쌓는 것이 아니라, 각 프로젝트가 `무슨 문제를 풀었는지`,
`어떤 답을 냈는지`, `어떻게 검증되는지`를 방문자가 바로 이해할 수 있게 만드는 것입니다.

## 프로젝트 맵

| ID | 프로젝트 | 풀 문제 | 내 답 | 검증 | 상태 |
| --- | --- | --- | --- | --- | --- |
| 01 | [AWS Security Primitives](00-aws-security-foundations/01-aws-security-primitives/README.md)<br>[문제](00-aws-security-foundations/01-aws-security-primitives/problem/README.md) | IAM policy가 왜 allow 또는 deny 되는지 설명하기 | statement match와 `explicit deny` 우선순위를 보여 주는 최소 평가 엔진 구현 | `pytest 00-aws-security-foundations/01-aws-security-primitives/python/tests` | `verified` |
| 02 | [Terraform AWS Lab](00-aws-security-foundations/02-terraform-aws-lab/README.md)<br>[문제](00-aws-security-foundations/02-terraform-aws-lab/problem/README.md) | Terraform을 배포 결과가 아니라 보안 분석 입력으로 읽기 | insecure/secure 실습 쌍을 만들고 plan JSON을 재현 가능한 입력으로 고정 | `pytest 00-aws-security-foundations/02-terraform-aws-lab/python/tests` | `verified` |
| 03 | [CloudTrail Log Basics](00-aws-security-foundations/03-cloudtrail-log-basics/README.md)<br>[문제](00-aws-security-foundations/03-cloudtrail-log-basics/problem/README.md) | 원본 보안 로그를 어떻게 queryable한 이벤트 구조로 바꿀 것인가 | CloudTrail과 VPC Flow Logs를 공통 `EventRecord`와 DuckDB/Parquet로 정규화 | `pytest 00-aws-security-foundations/03-cloudtrail-log-basics/python/tests` | `verified` |
| 04 | [IAM Policy Analyzer](01-cloud-security-core/04-iam-policy-analyzer/README.md)<br>[문제](01-cloud-security-core/04-iam-policy-analyzer/problem/README.md) | 정책 평가 결과를 least privilege finding으로 확장하기 | broad permission과 `iam:PassRole` 패턴을 severity가 있는 finding으로 변환 | `pytest 01-cloud-security-core/04-iam-policy-analyzer/python/tests` | `verified` |
| 05 | [CSPM Rule Engine](01-cloud-security-core/05-cspm-rule-engine/README.md)<br>[문제](01-cloud-security-core/05-cspm-rule-engine/problem/README.md) | plan JSON과 snapshot에서 triage 가능한 misconfiguration 찾기 | Terraform plan과 access key snapshot을 함께 읽는 규칙 엔진 구현 | `pytest 01-cloud-security-core/05-cspm-rule-engine/python/tests` | `verified` |
| 06 | [Remediation Pack Runner](01-cloud-security-core/06-remediation-pack-runner/README.md)<br>[문제](01-cloud-security-core/06-remediation-pack-runner/problem/README.md) | finding 이후 조치안을 어떻게 안전하게 제안할 것인가 | dry-run remediation과 승인 필요 여부를 분리하는 runner 구현 | `pytest 01-cloud-security-core/06-remediation-pack-runner/python/tests` | `verified` |
| 07 | [Security Lake Mini](01-cloud-security-core/07-security-lake-mini/README.md)<br>[문제](01-cloud-security-core/07-security-lake-mini/problem/README.md) | 적재된 로그에서 어떤 detection query를 반복 실행할 것인가 | CloudTrail fixture를 local lake에 적재하고 preset query로 alert 생성 | `pytest 01-cloud-security-core/07-security-lake-mini/python/tests` | `verified` |
| 08 | [Container Guardrails](01-cloud-security-core/08-container-guardrails/README.md)<br>[문제](01-cloud-security-core/08-container-guardrails/problem/README.md) | 클러스터 없이 manifest와 image metadata에서 위험 설정 찾기 | Kubernetes manifest와 image metadata를 함께 읽는 guardrail scanner 구현 | `pytest 01-cloud-security-core/08-container-guardrails/python/tests` | `verified` |
| 09 | [Exception and Evidence Manager](01-cloud-security-core/09-exception-and-evidence-manager/README.md)<br>[문제](01-cloud-security-core/09-exception-and-evidence-manager/problem/README.md) | finding, exception, evidence, audit를 어떻게 연결할 것인가 | 승인, 만료, 증적 연결, append-only audit 흐름을 갖는 작은 거버넌스 모델 구현 | `pytest 01-cloud-security-core/09-exception-and-evidence-manager/python/tests` | `verified` |
| 10 | [Cloud Security Control Plane](02-capstone/10-cloud-security-control-plane/README.md)<br>[문제](02-capstone/10-cloud-security-control-plane/problem/README.md) | 앞선 판단 로직을 하나의 운영 흐름으로 통합하기 | API, worker, DB, report, exception 흐름을 묶은 local control plane 구현 | `make test-capstone`, `make demo-capstone` | `verified` / `demo` |

## 트랙 인덱스

- [00 AWS Security Foundations](00-aws-security-foundations/README.md): 가장 작은 판단 규칙과 입력 구조를 익히는 기초 트랙
- [01 Cloud Security Core](01-cloud-security-core/README.md): finding, remediation, detection, governance로 확장하는 핵심 트랙
- [02 Capstone](02-capstone/README.md): 앞선 결과물을 하나의 local security platform 흐름으로 통합하는 캡스톤
- [docs/roadmap.md](docs/roadmap.md): 왜 이 순서로 배치했는지와 프로젝트 간 연결 이유
- [blog/README.md](blog/README.md): `notion/` 없이 실제 소스와 테스트만으로 다시 읽은 source-first blog 시리즈

## 전체 검증

모든 명령은 레포 루트 기준입니다.

```bash
make venv
make test-unit
make test-integration
make test-capstone
make demo-capstone
```

- `make doctor`: Python, Docker, Terraform 준비 상태를 확인합니다.
- `make test-unit`: 8개 단위 프로젝트의 테스트를 실행합니다.
- `make test-integration`: Terraform 기반 실습 테스트를 실행합니다.
- `make test-capstone`: 캡스톤 테스트를 실행합니다.
- `make demo-capstone`: Docker daemon이 있으면 PostgreSQL, 없으면 SQLite fallback으로 데모 산출물을 생성합니다.

## 개별 프로젝트 탐색

1. 루트 표에서 프로젝트 README와 `problem/README.md`를 먼저 엽니다.
2. 프로젝트 README에서 `풀려는 문제`, `내가 낸 답`, `검증 방법`을 먼저 확인합니다.
3. 구현 세부는 `python/README.md`, 개념은 `docs/README.md`, 학습 기록은 `notion/README.md`로 내려갑니다.

## 문서 레이어

- `README.md`: 공개 인덱스입니다. 문제, 답, 검증, 상태를 가장 먼저 보여 줍니다.
- `problem/README.md`: 원래 문제, 제공된 자료, 제약, 통과 기준을 정리합니다.
- `python/README.md`: 실제 구현 엔트리포인트, 실행 명령, 테스트, 대표 출력을 보여 줍니다.
- `docs/README.md`: 개념 문서 묶음의 역할과 먼저 읽을 문서를 안내합니다.
- `notion/README.md`: 현재 공개 학습 기록입니다. 문제 정의와 재현, 디버깅 근거를 보완합니다.

공통 규칙은 [docs/documentation-policy.md](docs/documentation-policy.md)에서 확인할 수 있습니다.
