# auth-threat-modeling

## 이 프로젝트의 문제

인증 설계는 “JWT를 쓴다”나 “OAuth를 붙인다”로 설명이 끝나지 않습니다. 이 프로젝트는 어떤 control이 빠지면 어떤 공격면이 열리는지를 고정 시나리오로 평가해 `AUTH-*` finding으로 바꾸는 문제를 다룹니다.

## 내가 만든 답

- cookie, bearer JWT, redirect-based OAuth/OIDC 흐름을 JSON scenario로 고정한 evaluator
- `AUTH-001`~`AUTH-008` control 기반 finding을 반환하는 판정 로직
- `check-scenarios`와 `demo` CLI로 secure baseline과 취약 시나리오를 재현하는 도구

## 검증 명령

```bash
make test-unit
make demo-auth
PYTHONPATH=study/02-auth-threat-modeling/python/src \
  .venv/bin/python -m auth_threat_modeling.cli check-scenarios \
  study/02-auth-threat-modeling/problem/data/scenario_bundle.json
```

## 입출력 계약

- 입력: `problem/data/scenario_bundle.json`, `problem/data/demo_profile.json`
- 출력: 시나리오별 `actual_control_ids`, `expected_control_ids`, `findings`
- 핵심 판정 축: OAuth `state`, PKCE, JWT validation, token storage, refresh rotation, CSRF, recovery code, rate limit

## 읽는 순서

1. [problem/README.md](problem/README.md)
2. [docs/README.md](docs/README.md)
3. [python/README.md](python/README.md)
4. [notion/README.md](notion/README.md)
5. [guides/security/auth-threat-modeling.md](../../../guides/security/auth-threat-modeling.md)

## 배운 점과 한계

- 실제 OAuth provider 연동보다 control gap을 설명 가능한 finding으로 고정하는 편이 먼저입니다.
- token cryptography 자체는 [crypto-primitives-in-practice](../01-crypto-primitives-in-practice/README.md)로 분리합니다.
- WebAuthn, device trust, risk-based auth는 현재 범위 밖입니다.
