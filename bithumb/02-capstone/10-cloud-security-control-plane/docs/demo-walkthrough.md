# 데모 워크스루

이 문서는 `10-cloud-security-control-plane`를 처음 보는 사람이 실행 없이도 데모 흐름과 결과를 빠르게 이해하도록 만든 공개용 요약입니다.

## 한 번에 재현하는 명령

```bash
make demo-capstone
```

- Docker daemon이 있으면 PostgreSQL 경로로 실행합니다.
- Docker daemon이 없으면 SQLite fallback으로 같은 흐름을 재현합니다.
- PostgreSQL 경로를 쓰는 경우 `docker-compose.yml`의 기본 DB 이름은 `study2_control_plane`입니다.

## 데모 시나리오

1. insecure Terraform plan과 broad IAM policy를 scan request로 넣습니다.
2. scan worker가 pending job을 처리하고 findings를 저장합니다.
3. CloudTrail fixture를 ingest해서 suspicious event finding을 추가합니다.
4. insecure Kubernetes manifest를 ingest해서 container guardrail finding을 추가합니다.
5. finding 하나를 예외 승인 상태로 바꿉니다.
6. 다른 finding에 대해 remediation dry-run을 만듭니다.
7. 최종 markdown report를 export합니다.

## 이 데모가 증명하는 것

- Terraform plan 기반 CSPM finding 생성
- IAM least privilege finding 생성
- CloudTrail 로그 적재와 detection
- Kubernetes manifest guardrail detection
- exception approval flow
- remediation dry-run generation
- report export

## 기록된 샘플 출력

아래 파일은 마지막 검증 실행에서 골라 둔 대표 샘플입니다.

- [demo-assets/findings-snapshot.json](demo-assets/findings-snapshot.json)
- [demo-assets/remediation-snapshot.json](demo-assets/remediation-snapshot.json)
- [demo-assets/report-excerpt.md](demo-assets/report-excerpt.md)

## 마지막 실행에서 본 핵심 숫자

- scan worker processed jobs: `2`
- CloudTrail findings added: `2`
- Kubernetes findings added: `3`
- report includes findings from four sources:
  - `terraform-plan`
  - `iam-policy`
  - `cloudtrail`
  - `k8s-manifest`
