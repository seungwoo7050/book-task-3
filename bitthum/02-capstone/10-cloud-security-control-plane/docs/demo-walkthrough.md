# Demo Walkthrough

이 문서는 `10-cloud-security-control-plane`를 처음 보는 사람이 실행 없이도 데모 흐름과 결과를
빠르게 이해하도록 만든 공개용 요약이다.

## One Command

```bash
cd study2
make demo-capstone
```

- Docker daemon이 있으면 PostgreSQL 경로로 실행한다.
- Docker daemon이 없으면 SQLite fallback으로 같은 흐름을 재현한다.

## Scenario

1. insecure Terraform plan과 broad IAM policy를 scan request로 넣는다.
2. scan worker가 pending job을 처리하고 findings를 저장한다.
3. CloudTrail fixture를 ingest해서 suspicious event finding을 추가한다.
4. insecure Kubernetes manifest를 ingest해서 container guardrail finding을 추가한다.
5. finding 하나를 예외 승인 상태로 바꾼다.
6. 다른 finding에 대해 remediation dry-run을 만든다.
7. 최종 markdown report를 export한다.

## What The Demo Proves

- Terraform plan 기반 CSPM finding 생성
- IAM least privilege finding 생성
- CloudTrail 로그 적재와 detection
- Kubernetes manifest guardrail detection
- exception approval flow
- remediation dry-run generation
- report export

## Recorded Outputs

아래 샘플은 실제 `make demo-capstone` 산출물을 요약해 tracked 문서로 옮긴 것이다.

- [demo-assets/findings-snapshot.json](demo-assets/findings-snapshot.json)
- [demo-assets/remediation-snapshot.json](demo-assets/remediation-snapshot.json)
- [demo-assets/report-excerpt.md](demo-assets/report-excerpt.md)

## Key Numbers From The Last Run

- scan worker processed jobs: `2`
- CloudTrail findings added: `2`
- Kubernetes findings added: `3`
- report includes findings from four sources:
  - `terraform-plan`
  - `iam-policy`
  - `cloudtrail`
  - `k8s-manifest`

## Why This Matters For The Target Job

- 단순 스캐너가 아니라 `탐지 -> triage -> 예외 -> 조치안 -> 리포트` 흐름을 보여 준다.
- 실제 AWS 계정 없이도 CSPM, IAM, 로그 분석, 자동화의 핵심 동작을 설명할 수 있다.
- 공고에서 요구하는 “반복 업무 자동화”와 “보안 로그 활용”을 둘 다 한 프로젝트에서 증명한다.
