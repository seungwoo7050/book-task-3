# 문제 정의

## 문제

인증 흐름을 설계할 때는 “JWT를 쓴다”, “OAuth를 붙인다” 같은 기능 이름보다, 어떤 통제가 있어야 공격면이 줄어드는지를
먼저 설명해야 합니다. 이 프로젝트는 JSON scenario를 읽어 auth control 누락을 finding으로 반환하는 평가기를 구현합니다.

## 성공 기준

- secure baseline scenario는 0 finding이어야 합니다.
- insecure scenario는 `AUTH-001`~`AUTH-008` 중 기대한 control ID만 반환해야 합니다.
- `check-scenarios <manifest>`가 시나리오별 matched 여부와 finding 목록을 pretty JSON으로 출력해야 합니다.
- `demo <profile>`가 하나의 auth 설계를 deterministic JSON으로 설명해야 합니다.

## canonical validation

```bash
make test-unit
make demo-auth
```

## scenario schema

- `name`: 시나리오 이름
- `flow`: `oauth_enabled`, `uses_jwt`, `uses_refresh_token`, `cookie_session_mutation`, `supports_recovery_codes`
- `controls`: `token_storage`, `access_ttl_minutes`, `refresh_rotation`, `reuse_detection`, `issuer_validation`, `audience_validation`, `algorithm_pinning`, `state_required`, `pkce_required`, `csrf_protection`, `recovery_codes_hashed`, `rate_limit_mode`
- `expected_control_ids`: 기대 finding control ID 목록

## 제공 fixture

- `problem/data/scenario_bundle.json`
- `problem/data/demo_profile.json`

