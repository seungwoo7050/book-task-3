# owasp-backend-mitigations

## 이 프로젝트의 문제

backend 보안은 “OWASP Top 10을 안다”가 아니라, 특정 route에서 어떤 방어가 빠졌는지를 설명할 수 있어야 합니다. 이 프로젝트는 endpoint fixture를 읽어 대표적인 defense gap을 `OWASP-*` finding으로 바꾸는 문제를 다룹니다.

## 내가 만든 답

- injection, broken access control, SSRF, debug exposure, path traversal을 다루는 endpoint case evaluator
- `OWASP-001`~`OWASP-005` finding을 반환하는 판정 로직
- `check-cases`와 `demo` CLI로 secure baseline과 취약 route를 재현하는 도구

## 검증 명령

```bash
make test-unit
make demo-owasp
PYTHONPATH=study/03-owasp-backend-mitigations/python/src \
  .venv/bin/python -m owasp_backend_mitigations.cli check-cases \
  study/03-owasp-backend-mitigations/problem/data/case_bundle.json
```

## 입출력 계약

- 입력: `problem/data/case_bundle.json`, `problem/data/demo_profile.json`
- 출력: case별 `actual_control_ids`, `expected_control_ids`, `findings`
- 핵심 판정 축: parameterized query, ownership scope, outbound allowlist, private IP blocking, debug stacktrace hiding, safe path normalization

## 읽는 순서

1. [problem/README.md](problem/README.md)
2. [docs/README.md](docs/README.md)
3. [python/README.md](python/README.md)
4. [notion/README.md](notion/README.md)
5. [guides/security/owasp-backend-defense.md](../../../guides/security/owasp-backend-defense.md)

## 배운 점과 한계

- 취약점 이름 나열보다 어떤 입력 경계에서 어떤 방어가 필요한지 설명하는 편이 더 중요합니다.
- 실제 FastAPI/Spring app, DB, outbound network는 구현하지 않습니다.
- XSS, deserialization, authz-as-code 같은 다른 OWASP 주제는 현재 범위 밖입니다.
