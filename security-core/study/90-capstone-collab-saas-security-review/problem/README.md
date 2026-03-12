# 문제 정의

## 문제

이 capstone의 문제는 각 보안 판단을 따로 설명하는 것이 아니라, 서로 다른 finding을 한 서비스 remediation queue로 다시 정렬하는 것입니다. 입력은 서버 로그나 live scan feed가 아니라 review에 필요한 최소 정보만 담은 단일 `JSON bundle`로 고정합니다.

## 성공 기준

- `secure_baseline_bundle.json`은 빈 remediation board를 만들어야 합니다.
- `review_bundle.json`은 crypto, auth, backend, dependency 결과를 모두 만들어야 합니다.
- `demo_bundle.json`은 artifact 7개와 markdown report를 생성해야 합니다.

## 입력 schema

- top-level: `title`, `service`, `crypto_review`, `auth_scenarios`, `backend_cases`, `dependency_bundle`
- `service`: `name`, `internet_exposed`, `data_sensitivity`, `tenant_model`
- `crypto_review`: `name`, `surface`, `controls`, `expected_control_ids`
- `crypto_review.controls`: `message_auth`, `constant_time_compare`, `password_kdf`, `password_kdf_hardened`, `key_separation`, `rotation_defined`
- `auth_scenarios`, `backend_cases`, `dependency_bundle` item schema는 foundations 프로젝트와 동일한 vocabulary를 유지합니다.

## 출력 계약

- `review`: `service`, `summary`, `crypto_findings`, `auth_findings`, `backend_findings`, `dependency_items`, `remediation_board`
- `summary`: finding count와 remediation item count만 남깁니다.
- demo artifact: `01-service-profile.json`부터 `07-report.md`까지 7개 파일

## fixture 세트

- `problem/data/secure_baseline_bundle.json`
- `problem/data/review_bundle.json`
- `problem/data/demo_bundle.json`

## canonical validation

```bash
make test-capstone
make demo-capstone
```
