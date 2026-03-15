# security-core

`security-core`는 학습 결과물을 `무슨 문제를 풀었는가`, `내가 만든 답이 무엇인가`, `어떻게 다시 검증하는가`로 바로 읽히게 정리한 보안 기초 학습 아카이브입니다. 목적은 보안 제품 배포가 아니라, 보안 primitive와 판단 기준을 작은 실행 가능한 프로젝트로 설명 가능하게 만드는 것입니다.

## 이 레포가 푸는 문제

- hash, MAC, KDF처럼 자주 섞여 설명되는 암호 primitive를 어디서 갈라서 이해해야 하는가
- session, JWT, OAuth/OIDC 설계에서 어떤 control이 빠지면 어떤 공격면이 열리는가
- backend route 설계에서 반복되는 방어 경계를 어떤 작은 fixture로 검증할 수 있는가
- dependency 취약점 대응에서 무엇을 지금 고치고 무엇을 문서화하며 무엇을 유예할지 어떻게 판단할 것인가
- 앞선 판단 기준을 하나의 remediation board와 review artifact로 어떻게 다시 묶을 것인가

## 이 레포의 답

- `study/` 아래에 다섯 개의 번호형 프로젝트를 두고, 각 프로젝트마다 `problem/`, `docs/`, `python/`, `notion/` 경계를 유지합니다.
- 각 프로젝트는 입력 fixture, CLI, pytest를 함께 제공해 문제와 해답을 같은 저장소 표면에서 확인할 수 있게 합니다.
- 루트와 프로젝트 README는 모두 `문제 / 내가 만든 답 / 검증` 계약으로 맞추고, 더 자세한 인덱스는 [docs/project-catalog.md](docs/project-catalog.md)와 [docs/readme-contract.md](docs/readme-contract.md)에서 관리합니다.

## 추천 읽기 순서

1. [study/01-crypto-primitives-in-practice/README.md](study/01-crypto-primitives-in-practice/README.md)
2. [study/02-auth-threat-modeling/README.md](study/02-auth-threat-modeling/README.md)
3. [study/03-owasp-backend-mitigations/README.md](study/03-owasp-backend-mitigations/README.md)
4. [study/04-dependency-vulnerability-workflow/README.md](study/04-dependency-vulnerability-workflow/README.md)
5. [study/90-capstone-collab-saas-security-review/README.md](study/90-capstone-collab-saas-security-review/README.md)

가장 짧은 입문 경로는 `01 -> 02 -> 03`이고, dependency triage와 capstone은 그 다음 단계입니다.

## 서버 문제지 빠른 진입

- [problem-subject-essential/README.md](problem-subject-essential/README.md): 서버 공통 필수 기준으로 다시 고른 문제지
- [problem-subject-elective/README.md](problem-subject-elective/README.md): essential에 포함되지 않은 나머지 문제지
- [problem-subject-capstone/README.md](problem-subject-capstone/README.md): 판단 기준을 다시 묶는 종합 과제 문제지

## 빠른 검증

아래 명령은 모두 레포 루트 기준입니다.

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

- `make test-unit`: `01`부터 `04`까지 foundations 프로젝트 pytest를 순서대로 실행합니다.
- `make test-capstone`: `90` capstone pytest를 실행합니다.
- `make demo-*`: 각 프로젝트의 대표 출력을 재현합니다.
- `make demo-capstone`: `.artifacts/capstone/demo/` 아래에 review artifact 세트를 생성합니다.

## 프로젝트 카탈로그

| 번호 | 프로젝트 | 문제 | 내가 만든 답 | canonical 검증 | 상태 |
| --- | --- | --- | --- | --- | --- |
| `01` | [crypto-primitives-in-practice](study/01-crypto-primitives-in-practice/README.md) | hash, MAC, KDF를 같은 함수처럼 다루지 않고 역할을 분리해 설명하는 문제 | reference vector와 `check-vectors`/`demo` CLI로 primitive 경계를 재현하는 Python 랩 | `make test-unit` / `make demo-crypto` | `verified` |
| `02` | [auth-threat-modeling](study/02-auth-threat-modeling/README.md) | auth 설계 선택을 control vocabulary와 finding으로 바꾸는 문제 | scenario evaluator와 `check-scenarios`/`demo` CLI로 `AUTH-*` 판정을 고정하는 랩 | `make test-unit` / `make demo-auth` | `verified` |
| `03` | [owasp-backend-mitigations](study/03-owasp-backend-mitigations/README.md) | backend route에서 어떤 방어가 빠졌는지 fixture로 설명하는 문제 | endpoint evaluator와 `check-cases`/`demo` CLI로 `OWASP-*` finding을 반환하는 랩 | `make test-unit` / `make demo-owasp` | `verified` |
| `04` | [dependency-vulnerability-workflow](study/04-dependency-vulnerability-workflow/README.md) | advisory triage를 우선순위와 action으로 정규화하는 문제 | offline bundle evaluator와 `triage`/`demo` CLI로 `P1`~`P4`와 action을 계산하는 랩 | `make test-unit` / `make demo-dependency` | `verified` |
| `90` | [capstone-collab-saas-security-review](study/90-capstone-collab-saas-security-review/README.md) | 앞선 finding을 하나의 remediation queue로 다시 묶는 문제 | consolidated review builder와 artifact writer로 review JSON, board, report를 생성하는 capstone | `make test-capstone` / `make demo-capstone` | `verified` |

전체 표의 단일 source of truth는 [docs/project-catalog.md](docs/project-catalog.md)입니다.

## 함께 보면 좋은 공용 가이드

- [guides/security/crypto-primitives.md](../guides/security/crypto-primitives.md)
- [guides/security/auth-threat-modeling.md](../guides/security/auth-threat-modeling.md)
- [guides/security/owasp-backend-defense.md](../guides/security/owasp-backend-defense.md)
- [guides/security/dependency-vulnerability-workflow.md](../guides/security/dependency-vulnerability-workflow.md)
