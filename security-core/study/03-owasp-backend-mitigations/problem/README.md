# 문제 정의

## 문제

backend route 설계를 작은 fixture로 고정하고, 어떤 방어가 빠졌는지를 `OWASP-*` finding으로 설명해야 합니다.

## 성공 기준

- secure baseline case는 0 finding이어야 합니다.
- insecure case는 기대한 `OWASP-*` control ID만 반환해야 합니다.
- `check-cases <manifest>`가 case별 matched 여부와 finding 목록을 JSON으로 출력해야 합니다.
- `demo <profile>`가 하나의 insecure endpoint 설계를 deterministic하게 설명해야 합니다.

## canonical validation

```bash
make test-unit
make demo-owasp
```

## case schema

- `name`
- `surface`: `route`, `method`, `database_touched`, `object_lookup`, `outbound_fetch`, `can_raise_debug`, `file_path_input`
- `controls`: `parameterized_queries`, `ownership_scope_enforced`, `outbound_allowlist`, `private_ip_blocking`, `debug_stacktrace_hidden`, `safe_path_normalization`
- `expected_control_ids`

## 제공 fixture

- `problem/data/case_bundle.json`
- `problem/data/demo_profile.json`
