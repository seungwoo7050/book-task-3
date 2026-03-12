# 문제 정의

## 문제

auth 설계를 기능 이름이 아니라 control presence와 attack surface로 평가해야 합니다. 이 프로젝트는 JSON scenario를 읽어 auth control 누락을 `AUTH-*` finding으로 반환합니다.

## 성공 기준

- secure baseline scenario는 0 finding이어야 합니다.
- insecure scenario는 기대한 `AUTH-*` control ID만 반환해야 합니다.
- `check-scenarios <manifest>`가 시나리오별 matched 여부와 finding 목록을 JSON으로 출력해야 합니다.
- `demo <profile>`가 하나의 auth 설계를 deterministic하게 설명해야 합니다.

## canonical validation

```bash
make test-unit
make demo-auth
```

## scenario schema

- `name`
- `flow`: `oauth_enabled`, `uses_jwt`, `uses_refresh_token`, `cookie_session_mutation`, `supports_recovery_codes`
- `controls`: `token_storage`, `access_ttl_minutes`, `refresh_rotation`, `reuse_detection`, `issuer_validation`, `audience_validation`, `algorithm_pinning`, `state_required`, `pkce_required`, `csrf_protection`, `recovery_codes_hashed`, `rate_limit_mode`
- `expected_control_ids`

## 제공 fixture

- `problem/data/scenario_bundle.json`
- `problem/data/demo_profile.json`
