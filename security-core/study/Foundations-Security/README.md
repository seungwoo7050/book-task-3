# Foundations Security

이 트랙은 보안 주제를 제품 기능으로 바로 섞기 전에, 먼저 primitive와 경계 모델을 독립된 학습 단위로 이해하게
만드는 구간입니다. 현재 foundations 범위는 모두 `verified`이며, 각 프로젝트는 fixture와 CLI로 재현 가능한 형태를 갖춥니다.

## 프로젝트 지도

| 순서 | 프로젝트 | 상태 | 핵심 질문 |
| --- | --- | --- | --- |
| 01 | [crypto-primitives-in-practice](crypto-primitives-in-practice/README.md) | `verified` | hash, MAC, KDF는 어디서 구분해야 하는가 |
| 02 | [auth-threat-modeling](auth-threat-modeling/README.md) | `verified` | session, JWT, OAuth 경계를 어떻게 위협 모델로 설명할까 |
| 03 | [owasp-backend-mitigations](owasp-backend-mitigations/README.md) | `verified` | 대표 backend mitigation을 어떤 작은 랩으로 나눌까 |
| 04 | [dependency-vulnerability-workflow](dependency-vulnerability-workflow/README.md) | `verified` | advisory, SBOM, patch triage를 어떻게 재현할까 |

## 권장 학습 순서

1. [crypto-primitives-in-practice](crypto-primitives-in-practice/README.md)에서 secret input과 public input의 차이를 먼저 잡습니다.
2. [auth-threat-modeling](auth-threat-modeling/README.md)에서 auth control vocabulary를 정리합니다.
3. [owasp-backend-mitigations](owasp-backend-mitigations/README.md)에서 route defense 경계를 고정합니다.
4. [dependency-vulnerability-workflow](dependency-vulnerability-workflow/README.md)에서 patch queue와 triage 판단 흐름을 정리합니다.
5. [../Capstone/collab-saas-security-review/README.md](../Capstone/collab-saas-security-review/README.md)에서 이 판단 기준을 remediation board로 다시 조합합니다.
