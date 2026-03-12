# Project Catalog

이 문서는 `security-core` 전체를 `문제 / 내 답 / 검증 / 상태`로 한 번에 보는 단일 인덱스입니다. 루트 README의 카탈로그를 더 자세히 본다고 생각하면 됩니다.

| 번호 | 프로젝트 | 문제 | 내 답 | canonical 검증 | 상태 |
| --- | --- | --- | --- | --- | --- |
| `01` | [crypto-primitives-in-practice](../study/01-crypto-primitives-in-practice/README.md) | hash, MAC, KDF를 같은 함수처럼 다루지 않고 역할과 입력 경계를 분리해 설명하는 문제 | reference vector 검증기와 deterministic demo CLI | `make test-unit` / `make demo-crypto` | `verified` |
| `02` | [auth-threat-modeling](../study/02-auth-threat-modeling/README.md) | auth 설계 선택을 attack surface와 control gap으로 바꾸는 문제 | scenario evaluator와 `AUTH-*` finding CLI | `make test-unit` / `make demo-auth` | `verified` |
| `03` | [owasp-backend-mitigations](../study/03-owasp-backend-mitigations/README.md) | backend route에서 반복되는 defense gap을 fixture로 설명하는 문제 | endpoint evaluator와 `OWASP-*` finding CLI | `make test-unit` / `make demo-owasp` | `verified` |
| `04` | [dependency-vulnerability-workflow](../study/04-dependency-vulnerability-workflow/README.md) | advisory triage를 priority와 action으로 정리하는 문제 | offline bundle triage engine과 reason code 출력 CLI | `make test-unit` / `make demo-dependency` | `verified` |
| `90` | [capstone-collab-saas-security-review](../study/90-capstone-collab-saas-security-review/README.md) | 앞선 판단을 하나의 remediation board로 합치는 문제 | consolidated review builder와 artifact writer | `make test-capstone` / `make demo-capstone` | `verified` |

## 읽는 순서

1. `01`에서 primitive vocabulary를 고정합니다.
2. `02`, `03`에서 auth와 backend defense를 scenario/case 평가기로 확장합니다.
3. `04`에서 triage와 우선순위 결정을 추가합니다.
4. `90`에서 앞선 출력을 하나의 review artifact 세트로 다시 조합합니다.
