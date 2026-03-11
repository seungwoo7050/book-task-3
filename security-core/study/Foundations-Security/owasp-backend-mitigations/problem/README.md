# 문제 정의

## 문제

backend 보안은 “Top 10을 안다”보다, 특정 endpoint 설계에서 어떤 방어가 빠졌는지를 설명할 수 있어야 합니다.
이 프로젝트는 route case fixture를 읽어 대표 mitigation 누락을 finding으로 반환하는 평가기를 구현합니다.

## 성공 기준

- secure baseline case는 0 finding이어야 합니다.
- insecure case는 `OWASP-001`~`OWASP-005` 중 기대한 control ID만 반환해야 합니다.
- `check-cases <manifest>`가 case별 matched 여부, finding, severity를 pretty JSON으로 출력해야 합니다.
- `demo <profile>`가 하나의 insecure endpoint 설계를 deterministic JSON으로 설명해야 합니다.

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

