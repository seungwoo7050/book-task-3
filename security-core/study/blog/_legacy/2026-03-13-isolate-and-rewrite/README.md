# security-core study blog

`study/blog/`는 `security-core`의 공개 학습 로그 레이어다. 이 디렉터리는 기존 `README.md`, `problem/`, `docs/`, `python/`을 대체하지 않고, 각 독립 프로젝트를 `source-first chronology`로 다시 읽는 시리즈만 모은다.

## 공통 provenance

- 근거 우선순위는 `../../README.md` -> `../README.md` -> 각 프로젝트 `README.md` -> `problem/README.md` -> `docs/README.md`와 개념 문서 -> `python/README.md` -> `python/src` -> `python/tests` -> 실제 CLI 실행 결과 -> `git log -- security-core`다.
- 기존 blog 초안은 입력 근거로 쓰지 않았다. `security-core` 아래에는 기존 프로젝트 blog가 없어서 `isolate-and-rewrite`는 새 작성 모드로 동작했다.
- 현재 git anchor는 `2026-03-12 e3be503` 한 줄로 얇게 남아 있으므로, 세부 chronology는 날짜를 지어내지 않고 `Day / Session` 단위로 보수적으로 복원했다.
- `notion/` 계층은 chronology를 보강하는 용도로도 사용하지 않았다. 이번 시리즈는 README, docs, source, tests, CLI만으로 닫히는 범위만 다룬다.

## 프로젝트 카탈로그

| 프로젝트 | 핵심 질문 | 시작점 |
| --- | --- | --- |
| [crypto-primitives-in-practice](01-crypto-primitives-in-practice/README.md) | hash, MAC, KDF를 어디서 갈라서 설명해야 하는가 | [00-series-map.md](01-crypto-primitives-in-practice/00-series-map.md) |
| [auth-threat-modeling](02-auth-threat-modeling/README.md) | auth 설계를 control gap과 finding으로 어떻게 고정할까 | [00-series-map.md](02-auth-threat-modeling/00-series-map.md) |
| [owasp-backend-mitigations](03-owasp-backend-mitigations/README.md) | backend route 방어 경계를 fixture로 어떻게 재현할까 | [00-series-map.md](03-owasp-backend-mitigations/00-series-map.md) |
| [dependency-vulnerability-workflow](04-dependency-vulnerability-workflow/README.md) | dependency triage를 priority와 action으로 어떻게 설명할까 | [00-series-map.md](04-dependency-vulnerability-workflow/00-series-map.md) |
| [collab-saas-security-review](90-capstone-collab-saas-security-review/README.md) | 앞선 판단을 remediation board 하나로 어떻게 합칠까 | [00-series-map.md](90-capstone-collab-saas-security-review/00-series-map.md) |

## 읽는 법

1. 먼저 [../README.md](../README.md)와 [../../README.md](../../README.md)로 전체 문제 지형과 검증 entrypoint를 잡는다.
2. 원하는 프로젝트의 `README.md`와 `00-series-map.md`로 source set, canonical CLI, git anchor를 확인한다.
3. numbered chronology 글을 순서대로 읽으며 `문제 정의 -> evaluator surface -> fixture/test matrix -> demo/output` 흐름이 어떻게 닫히는지 따라간다.
4. 필요할 때만 원 프로젝트의 `problem/`, `docs/`, `python/`으로 다시 내려가 세부 구현을 확인한다.

## Git Anchor

- `2026-03-12 e3be503 Track Appendix 에 대한 전반적인 개선 완료 (mobile / security)`
