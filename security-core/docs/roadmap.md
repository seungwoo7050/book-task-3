# 보안 기초 로드맵

이 레포는 `primitive 이해 -> auth/boundary 모델링 -> backend defense -> dependency triage -> consolidated review` 순서로 읽게 설계했습니다. 디렉터리는 단일 번호형 시퀀스로 평탄화했지만, 학습 역할상 `01`부터 `04`까지는 foundations, `90`은 통합 capstone입니다.

## 현재 시퀀스

### 01 crypto-primitives-in-practice

상태: `verified`

질문: hash, MAC, KDF는 어디서 갈라서 설명해야 하는가?

핵심 범위:

- SHA-256 digest reference vector
- HMAC-SHA256 reference vector
- HKDF-SHA256 reference vector
- PBKDF2-HMAC-SHA1 reference vector

### 02 auth-threat-modeling

상태: `verified`

질문: session, JWT, OAuth/OIDC 설계를 어떤 control vocabulary로 평가할 것인가?

핵심 범위:

- OAuth `state`, PKCE
- JWT validation, token storage, refresh rotation
- CSRF, recovery code, rate limit

### 03 owasp-backend-mitigations

상태: `verified`

질문: backend route에서 반복되는 방어 경계를 어떤 fixture로 검증할 것인가?

핵심 범위:

- injection
- broken access control
- SSRF
- debug exposure
- path traversal

### 04 dependency-vulnerability-workflow

상태: `verified`

질문: advisory triage를 우선순위와 action으로 어떻게 정규화할 것인가?

핵심 범위:

- package/advisory/service_context bundle
- `P1`~`P4` priority 계산
- action mapping
- reason code 설명

### 90 capstone-collab-saas-security-review

상태: `verified`

질문: 앞선 finding을 하나의 remediation queue와 artifact 세트로 어떻게 다시 묶을 것인가?

핵심 범위:

- `JSON bundle -> consolidated review -> remediation board`
- `CRYPTO-*`, `AUTH-*`, `OWASP-*`, dependency `P1`~`P4`
- `.artifacts/capstone/demo/` artifact 7종 생성
