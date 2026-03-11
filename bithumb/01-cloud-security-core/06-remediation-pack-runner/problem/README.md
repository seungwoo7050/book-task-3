# 문제 정리

## 원래 문제

탐지에서 끝나지 않고, 어떤 finding은 자동 패치 후보가 되고 어떤 finding은 수동 승인과 운영 절차가 필요하다는 점을 코드로 구분해야 합니다.
핵심은 “실행”보다 “검토 가능한 제안”을 우선하는 것입니다.

## 제공된 자료

- `problem/data/sample_finding.json`
- finding을 remediation plan으로 바꾸는 CLI 흐름

## 제약

- 실제 patch 적용은 하지 않습니다.
- 외부 승인 시스템이나 rollback orchestration은 연결하지 않습니다.

## 통과 기준

- sample finding에서 remediation mode와 요약, patch 초안이 생성되어야 합니다.
- 승인 필요 상태가 테스트로 고정되어야 합니다.
- 후속 control plane이 재사용할 수 있는 형태여야 합니다.

## 이번 프로젝트에서 일부러 제외한 것

- 실제 인프라 변경
- 자동 rollback
- 외부 승인 시스템 연동
