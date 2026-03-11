# 보안 기초 로드맵

이 레포는 `작은 primitive 이해 -> 인증/방어 모델링 -> 취약점 대응 workflow -> consolidated remediation workflow`
순서로 확장했고, 현재 foundations와 capstone 범위를 모두 `verified`로 닫았습니다.

## Foundations Security

### 01 crypto-primitives-in-practice

상태: `verified`

질문: hash, MAC, KDF는 어디서 갈라서 설명해야 하는가?

핵심 범위:

- SHA-256 digest
- HMAC-SHA256
- HKDF-SHA256
- PBKDF2-HMAC-SHA1 reference vectors

### 02 auth-threat-modeling

상태: `verified`

질문: session, JWT, OAuth attack surface를 어떻게 fixture와 문서로 설명할 것인가?

핵심 범위:

- secure baseline auth scenario
- OAuth `state` / PKCE control gap
- JWT validation, token storage, refresh rotation gap
- CSRF, recovery code, rate limit gap

### 03 owasp-backend-mitigations

상태: `verified`

질문: OWASP Top 10의 대표 backend mitigation을 어떤 작은 랩으로 분리할 것인가?

핵심 범위:

- injection
- broken access control
- SSRF
- debug exposure
- path traversal

### 04 dependency-vulnerability-workflow

상태: `verified`

질문: advisory, SBOM, patch triage 흐름을 어떤 입력과 출력으로 재현할 것인가?

핵심 범위:

- offline package/advisory bundle
- priority `P1`~`P4`
- action mapping
- reason code 기반 triage 설명

## Capstone

### 05 collab-saas-security-review

상태: `verified`

질문: primitive, auth, backend defense, dependency triage를 한 서비스 review와 remediation board로 어떻게 다시 묶을 것인가?

핵심 범위:

- `JSON bundle -> consolidated review -> remediation board`
- `CRYPTO-*`, `AUTH-*`, `OWASP-*`, dependency `P1`~`P4` vocabulary 재구성
- `.artifacts/capstone/demo/` artifact 세트 생성
