# problem

이 capstone의 핵심 문제는 "각 보안 판단을 따로 설명하는 것"이 아니라, 서로 다른 finding을 한 서비스 remediation queue로 다시
정렬하는 것입니다. 따라서 입력은 서버 요청 로그나 live scan feed가 아니라, review에 필요한 최소 정보만 담은 단일 `JSON bundle`
로 고정합니다.

## 이 프로젝트가 답하려는 질문

- message authentication, auth control, backend defense, dependency triage를 한 문서에서 어떻게 함께 읽을 것인가
- severity가 다른 finding을 `P1`~`P4` remediation queue로 어떻게 다시 정규화할 것인가
- secure baseline을 어떻게 정의해야 "이상 없음" 상태를 반복 가능하게 증명할 수 있는가

## 입력 schema

top-level key:

- `title`
- `service`
- `crypto_review`
- `auth_scenarios`
- `backend_cases`
- `dependency_bundle`

`service`:

- `name`
- `internet_exposed`
- `data_sensitivity`
- `tenant_model`

`crypto_review`:

- `name`
- `surface`
- `controls`
- `expected_control_ids`

`crypto_review.controls`:

- `message_auth`
- `constant_time_compare`
- `password_kdf`
- `password_kdf_hardened`
- `key_separation`
- `rotation_defined`

`auth_scenarios`, `backend_cases`, `dependency_bundle`의 item schema는 foundations 프로젝트와 동일한 vocabulary를 유지합니다.

## 출력 계약

`review`는 다음 top-level key를 가진 consolidated JSON을 출력해야 합니다.

- `service`
- `summary`
- `crypto_findings`
- `auth_findings`
- `backend_findings`
- `dependency_items`
- `remediation_board`

`summary`는 finding count와 remediation item count만 남기고, 세부 판정 근거는 각 카테고리 배열로 보냅니다.

## fixture 세트

- `secure_baseline_bundle.json`: 모든 finding과 triage item이 비어 있어야 하는 기준선
- `review_bundle.json`: 모든 카테고리에서 finding 또는 dependency item이 최소 1개 이상 나오는 통합 검증용 입력
- `demo_bundle.json`: `.artifacts/capstone/demo/`에 artifact를 생성하는 데모 입력

## 성공 기준

- `secure_baseline_bundle.json`은 빈 remediation board를 만들어야 합니다.
- `review_bundle.json`은 crypto/auth/backend/dependency 모두에서 결과를 만들어야 합니다.
- `demo_bundle.json`은 artifact 7개와 markdown report를 생성해야 합니다.

## canonical validation

```bash
make test-capstone
make demo-capstone
```

`make demo-capstone`이 성공하면 `.artifacts/capstone/demo/` 아래에 아래 파일이 생성되어야 합니다.

- `01-service-profile.json`
- `02-crypto-findings.json`
- `03-auth-findings.json`
- `04-backend-findings.json`
- `05-dependency-items.json`
- `06-remediation-board.json`
- `07-report.md`
