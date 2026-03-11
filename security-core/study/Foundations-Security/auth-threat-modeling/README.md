# auth-threat-modeling

## 프로젝트 한줄 소개

session, JWT, OAuth/OIDC 설계 선택을 고정 시나리오로 평가해 위협 finding으로 바꾸는 auth threat modeling 랩입니다.

## 왜 배우는가

인증 보안은 실제 서버를 크게 만드는 것보다 먼저, 어떤 제어가 빠지면 어떤 공격면이 열리는지 설명할 수 있어야 합니다.
이 프로젝트는 cookie, bearer JWT, redirect-based OAuth 흐름을 JSON fixture로 고정해, state/PKCE/CSRF/rotation 같은 통제를
시나리오 평가기로 검증합니다.

## 현재 구현 범위

- auth 설계 시나리오 manifest 평가
- `AUTH-001`~`AUTH-008` control 기반 finding 반환
- `check-scenarios`와 `demo` CLI
- secure baseline 0 finding 검증

## 빠른 시작

아래 명령은 `security-core` 레포 루트 기준입니다.

```bash
make venv
make demo-auth
PYTHONPATH=study/Foundations-Security/auth-threat-modeling/python/src \
  .venv/bin/python -m auth_threat_modeling.cli check-scenarios \
  study/Foundations-Security/auth-threat-modeling/problem/data/scenario_bundle.json
```

## 검증 명령

```bash
make test-unit
```

## 먼저 읽을 파일

- [problem/README.md](problem/README.md)
- [docs/README.md](docs/README.md)
- [python/README.md](python/README.md)
- [notion/README.md](notion/README.md)
- [guides/security/auth-threat-modeling.md](../../../../guides/security/auth-threat-modeling.md)

## 포트폴리오 확장 힌트

실제 OAuth provider 연동 여부보다, 어떤 auth control을 왜 요구하는지와 secure baseline에서 0 finding이 나오는 이유를
설명하는 편이 더 설득력 있습니다.

## 알려진 한계

- 실제 login server, provider callback, JWKS fetch는 구현하지 않습니다.
- threat model은 control presence 평가에 집중하고, token cryptography 자체는 [crypto-primitives-in-practice](../crypto-primitives-in-practice/README.md)로 분리합니다.
- WebAuthn, device trust, risk-based auth는 현재 범위 밖입니다.

