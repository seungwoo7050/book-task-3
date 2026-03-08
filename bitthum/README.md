# study2: AWS First Cloud Security Track

`study2/`는 `backend-go/study/`와 분리된 독립 학습 레포다. 목표는 AWS를 거의 써보지 않은
상태에서 시작해, 로컬에서 재현 가능한 보안 자동화 과제들과 최종 control plane capstone을
통해 `클라우드 보안 담당자 (신입/주니어)` 공고에 맞는 결과물을 만드는 것이다.

## Tracks

1. `00-aws-security-foundations`
   - `01-aws-security-primitives`
   - `02-terraform-aws-lab`
   - `03-cloudtrail-log-basics`
2. `01-cloud-security-core`
   - `04-iam-policy-analyzer`
   - `05-cspm-rule-engine`
   - `06-remediation-pack-runner`
   - `07-security-lake-mini`
   - `08-container-guardrails`
   - `09-exception-and-evidence-manager`
3. `02-capstone`
   - `10-cloud-security-control-plane`

## Commands

```bash
make doctor
make test-unit
make test-integration
make test-capstone
make test-all
make demo-capstone
```

## Design Rules

- AWS 계정은 v1 필수 조건이 아니다.
- Terraform plan JSON, CloudTrail fixtures, Kubernetes manifests, DuckDB, PostgreSQL로
  로컬에서 끝까지 재현 가능해야 한다.
- tracked 문서는 문제, 구현 범위, 검증 명령, 학습 포인트를 설명한다.
- `notion/`은 로컬 전용 기술 노트다.

