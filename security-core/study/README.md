# study

`study/`는 이 저장소의 실제 학습 프로젝트 트리입니다. 상위 트랙 설명보다 프로젝트 번호 순서를 먼저 드러내서, 처음 방문한 사람이 바로 문제와 해답 위치를 찾을 수 있게 구성합니다.

## 읽기 시작점

1. [../docs/project-catalog.md](../docs/project-catalog.md)
2. 아래 번호형 프로젝트 README
3. 각 프로젝트의 `problem/README.md`, `docs/README.md`, `python/README.md`, `notion/README.md`

## 디렉터리 구조

```text
study/
  01-crypto-primitives-in-practice/
  02-auth-threat-modeling/
  03-owasp-backend-mitigations/
  04-dependency-vulnerability-workflow/
  90-capstone-collab-saas-security-review/
```

## 번호형 읽기 순서

| 번호 | 프로젝트 | 역할 |
| --- | --- | --- |
| `01` | [crypto-primitives-in-practice](01-crypto-primitives-in-practice/README.md) | secret input과 public input을 primitive 수준에서 분리합니다. |
| `02` | [auth-threat-modeling](02-auth-threat-modeling/README.md) | auth control vocabulary를 고정 시나리오로 검증합니다. |
| `03` | [owasp-backend-mitigations](03-owasp-backend-mitigations/README.md) | backend route defense를 endpoint fixture로 평가합니다. |
| `04` | [dependency-vulnerability-workflow](04-dependency-vulnerability-workflow/README.md) | patch triage와 action 결정을 offline bundle로 재현합니다. |
| `90` | [capstone-collab-saas-security-review](90-capstone-collab-saas-security-review/README.md) | 앞선 판단 기준을 하나의 remediation board로 다시 조합합니다. |

## 읽는 방법

- 각 프로젝트는 `README.md -> problem/README.md -> docs/README.md -> python/README.md -> notion/README.md` 순서로 읽습니다.
- `01`부터 `04`까지는 foundations 역할, `90`은 통합 capstone 역할을 맡지만 디렉터리 자체는 단일 시퀀스로 유지합니다.
- 개별 프로젝트를 건너뛰더라도 루트 기준 검증 명령은 유지하므로, 먼저 실행해 보고 필요한 프로젝트로 내려가도 됩니다.
