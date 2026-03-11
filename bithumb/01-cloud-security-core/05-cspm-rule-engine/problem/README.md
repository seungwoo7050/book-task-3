# 문제 정리

## 원래 문제

Terraform plan JSON과 운영 snapshot을 읽어, 보안 운영자가 바로 triage할 수 있는 misconfiguration finding을 생성해야 합니다.
핵심은 규칙 개수보다 입력 스키마와 설명 가능한 출력 구조를 분명하게 만드는 것입니다.

## 제공된 자료

- `problem/data/insecure_plan.json`
- `problem/data/secure_plan.json`
- `problem/data/access_keys_snapshot.json`

## 제약

- 실제 배포 환경 전체를 스캔하지 않습니다.
- local fixture 기준으로 재현 가능한 규칙만 다룹니다.

## 통과 기준

- insecure fixture에서 S3, security group, encryption, access key age 관련 finding이 나와야 합니다.
- secure fixture에서 불필요한 finding이 나오지 않아야 합니다.
- finding 출력에 severity와 evidence가 포함되어야 합니다.

## 이번 프로젝트에서 일부러 제외한 것

- 전체 클라우드 자산 인벤토리 수집
- drift detection
- 조직 단위 multi-account 스캔
