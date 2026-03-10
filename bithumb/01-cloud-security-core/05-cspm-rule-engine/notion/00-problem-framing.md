# 문제 프레이밍

## 이 프로젝트가 답하려는 질문

CSPM의 핵심은 결국 “이 설정이 안전한가?”에 자동으로 답하는 것입니다. 이 프로젝트는 Terraform plan JSON과
access key snapshot을 읽어, 배포 전 설정과 운영 중 상태를 함께 보는 작은 규칙 엔진을 만듭니다.

## 실제 입력과 출력

입력:
- `insecure_plan.json`
- `secure_plan.json`
- `access_keys_snapshot.json`

출력:
- `CSPM-001` ~ `CSPM-004` finding
- severity와 title을 가진 triage 가능한 결과

## 강한 제약

- rule set은 S3 public access, SG ingress, encryption, access key age 네 종류로 제한합니다.
- DSL이나 외부 rule registry는 만들지 않습니다.
- 실제 클라우드 계정 스캔이 아니라 fixture 입력만 사용합니다.

## 완료로 보는 기준

- insecure plan에서 세 가지 misconfiguration finding이 나와야 합니다.
- secure plan에서는 finding 0개여야 합니다.
- 오래된 access key 하나만 별도 finding으로 잡혀야 합니다.

## 확인에 쓰는 근거

- 문제 설명: [../problem/README.md](../problem/README.md)
- 핵심 테스트: [../python/tests/test_scanner.py](../python/tests/test_scanner.py)
- 이전 배경 설명: [../notion-archive/essay.md](../notion-archive/essay.md)
