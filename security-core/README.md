# security-core

이 저장소는 `bithumb`의 AWS/cloud-security 흐름과 별개로, 일반 백엔드와 CS 학습에서 공통으로 필요한
보안 기초를 작은 프로젝트로 다시 설명하는 학습 아카이브입니다. 목표는 보안 제품을 바로 배포하는 것이 아니라,
개념 경계와 검증 근거를 스스로 설명할 수 있는 학습 표면을 만드는 것입니다.

## 이 레포가 맡는 역할

- hash, MAC, KDF, 인증 경계, 취약점 triage 같은 공용 선수 지식을 별도 축으로 분리합니다.
- `backend-fastapi`, `backend-spring`, `bithumb`에서 반복되는 보안 개념을 더 작은 학습 단위로 먼저 다룹니다.
- README, `problem/`, `docs/`, `notion/`, 구현 코드 사이의 provenance를 명확히 남깁니다.

## 먼저 읽을 곳

1. [docs/roadmap.md](docs/roadmap.md)
2. [study/README.md](study/README.md)
3. [study/Foundations-Security/README.md](study/Foundations-Security/README.md)
4. 각 프로젝트 README

## 현재 트랙

### Foundations Security

- [crypto-primitives-in-practice](study/Foundations-Security/crypto-primitives-in-practice/README.md) `verified`
- [auth-threat-modeling](study/Foundations-Security/auth-threat-modeling/README.md) `verified`
- [owasp-backend-mitigations](study/Foundations-Security/owasp-backend-mitigations/README.md) `verified`
- [dependency-vulnerability-workflow](study/Foundations-Security/dependency-vulnerability-workflow/README.md) `verified`

### Capstone

- [collab-saas-security-review](study/Capstone/collab-saas-security-review/README.md) `verified`

이 capstone은 앞선 네 프로젝트의 vocabulary를 하나의 remediation workflow로 다시 묶는 offline review 파이프라인입니다.

## 빠른 시작

아래 명령은 이 저장소 루트 기준입니다.

```bash
make venv
make test-unit
make test-capstone
make demo-crypto
make demo-auth
make demo-owasp
make demo-dependency
make demo-capstone
```

- `make doctor`: Python 3.13 기반 실행 환경인지 확인합니다.
- `make test-unit`: 네 프로젝트의 pytest를 순서대로 실행합니다.
- `make test-capstone`: capstone pytest를 실행합니다.
- `make demo-crypto`: hash, MAC, KDF 결과를 출력합니다.
- `make demo-auth`: auth control gap 평가 결과를 출력합니다.
- `make demo-owasp`: backend defense gap finding을 출력합니다.
- `make demo-dependency`: offline dependency triage 결과를 출력합니다.
- `make demo-capstone`: consolidated review artifact를 `.artifacts/capstone/demo/` 아래에 생성합니다.

## 문서 원칙

- 설명 문장은 한국어를 기본으로 쓰고, 명령어·파일 경로·도구명·식별자는 영어 원문을 유지합니다.
- 각 프로젝트 README는 학습 안내문 역할만 맡고, 긴 개념 설명은 `docs/`, 긴 실행 복기와 실패 사례는 `notion/`으로 보냅니다.
- 아직 시작하지 않은 트랙은 빈 디렉터리나 선제 링크로 만들지 않습니다.

공용 문서 규칙은 [docs/documentation-policy.md](docs/documentation-policy.md)에서 관리합니다.

## 함께 보면 좋은 공용 가이드

- [guides/security/crypto-primitives.md](../guides/security/crypto-primitives.md)
- [guides/security/auth-threat-modeling.md](../guides/security/auth-threat-modeling.md)
- [guides/security/owasp-backend-defense.md](../guides/security/owasp-backend-defense.md)
- [guides/security/dependency-vulnerability-workflow.md](../guides/security/dependency-vulnerability-workflow.md)
