# 문제 정리

## 원래 문제

최종 목표는 AWS-first local security control plane을 만드는 것입니다.
여러 입력을 받아 finding, exception, remediation plan, markdown report, audit event까지 한 흐름으로 연결해야 합니다.

## 제공된 자료

- `problem/data/insecure_plan.json`
- `problem/data/broad_admin_policy.json`
- `problem/data/cloudtrail_suspicious.json`
- `problem/data/insecure_k8s.yaml`
- FastAPI app, worker, demo capture 스크립트

## 제약

- 실제 AWS 계정과 연동하지 않습니다.
- 외부 큐 시스템, 운영용 인증, 멀티테넌시는 다루지 않습니다.

## 통과 기준

- scan과 ingestion 결과가 공통 finding 저장소에 쌓여야 합니다.
- exception 생성, remediation dry-run, report 생성이 end-to-end로 동작해야 합니다.
- `make test-capstone`과 `make demo-capstone`이 각각 테스트와 데모 산출물을 제공해야 합니다.

## 이번 프로젝트에서 일부러 제외한 것

- 실제 클라우드 API 연동
- 외부 메시지 큐와 분산 worker
- 운영용 인증, 권한 관리, 멀티테넌시
