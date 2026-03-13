# security-core study blog

`study/blog/`는 `security-core`의 번호형 프로젝트를 소스코드와 실행 흔적 중심으로 다시 읽기 위한 공개 chronology 레이어다. 루트 README가 “무슨 프로젝트가 있는가”를 보여 준다면, 여기서는 “실제로 어떤 순서로 만들었고 무엇으로 검증했는가”를 따라가게 된다.

이번 배치는 `/Users/woopinbell/work/book-task-3/blog/blog-writing-guide.md` 기준으로 다시 썼다. 기존 초안은 새 글의 입력 근거에서 제외하기 위해 `_legacy/2026-03-13-isolate-and-rewrite/`로 옮겨 두었고, 현재 디렉터리에는 새로 리라이트한 라이브 문서만 남겨 두었다.

## 먼저 읽는 법

1. 루트 [../../README.md](../../README.md)와 [../../docs/project-catalog.md](../../docs/project-catalog.md)로 전체 문제 지형을 잡는다.
2. 원하는 프로젝트의 `00-series-map.md`에서 이 시리즈가 어떤 질문을 따라가는지와 canonical CLI를 먼저 확인한다.
3. `01-evidence-ledger.md`와 `02-structure.md`를 읽고, 마지막 `10-chronology-*.md`에서 실제 구현 순서를 따라간다.
4. 더 깊이 확인하고 싶으면 원 프로젝트의 `problem/`, `docs/`, `python/` 디렉터리로 내려가 source set을 다시 읽는다.

## 프로젝트 색인

| 프로젝트 | evidence ledger | structure | 최종 blog |
| --- | --- | --- | --- |
| `01-crypto-primitives-in-practice` | [01-evidence-ledger.md](01-crypto-primitives-in-practice/01-evidence-ledger.md) | [02-structure.md](01-crypto-primitives-in-practice/02-structure.md) | [10-chronology-separating-primitives-vectors-and-demo-surface.md](01-crypto-primitives-in-practice/10-chronology-separating-primitives-vectors-and-demo-surface.md) |
| `02-auth-threat-modeling` | [01-evidence-ledger.md](02-auth-threat-modeling/01-evidence-ledger.md) | [02-structure.md](02-auth-threat-modeling/02-structure.md) | [10-chronology-turning-auth-controls-into-deterministic-findings.md](02-auth-threat-modeling/10-chronology-turning-auth-controls-into-deterministic-findings.md) |
| `03-owasp-backend-mitigations` | [01-evidence-ledger.md](03-owasp-backend-mitigations/01-evidence-ledger.md) | [02-structure.md](03-owasp-backend-mitigations/02-structure.md) | [10-chronology-fixing-route-defense-gaps-with-case-fixtures.md](03-owasp-backend-mitigations/10-chronology-fixing-route-defense-gaps-with-case-fixtures.md) |
| `04-dependency-vulnerability-workflow` | [01-evidence-ledger.md](04-dependency-vulnerability-workflow/01-evidence-ledger.md) | [02-structure.md](04-dependency-vulnerability-workflow/02-structure.md) | [10-chronology-scoring-priority-actions-and-reason-codes.md](04-dependency-vulnerability-workflow/10-chronology-scoring-priority-actions-and-reason-codes.md) |
| `90-capstone-collab-saas-security-review` | [01-evidence-ledger.md](90-capstone-collab-saas-security-review/01-evidence-ledger.md) | [02-structure.md](90-capstone-collab-saas-security-review/02-structure.md) | [10-chronology-reassembling-findings-into-one-remediation-board.md](90-capstone-collab-saas-security-review/10-chronology-reassembling-findings-into-one-remediation-board.md) |

## provenance

- 근거 우선순위는 루트 `README.md`, `docs/project-catalog.md`, 각 프로젝트의 `README.md`, `problem/README.md`, `docs/README.md`, `docs/concepts/*`, `python/README.md`, `python/src/*`, `python/tests/*`, 2026-03-13에 다시 실행한 CLI와 pytest 결과 순서를 따른다.
- 이번 리라이트에서는 기존 `study/blog/*` 초안을 새 글의 입력 자료로 쓰지 않았다. 비교용 보관본으로만 남겨 두었다.
- `git log`는 각 프로젝트 모두 `e3be503` 한 줄만 남아 있어서, 세부 chronology는 날짜를 지어내지 않고 `Session 1`, `Session 2`처럼 보수적으로 복원했다.
- `notion/` 계층은 이번 시리즈에서 사용하지 않았다. README, docs, source, tests, CLI만으로 닫히는 범위만 다뤘다.
