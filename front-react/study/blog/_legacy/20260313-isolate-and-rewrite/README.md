# front-react study blog

`study/blog/`는 `front-react`의 9개 독립 프로젝트를 소스와 실행 흔적으로 다시 읽는 공개 chronology 레이어다. 이번 배치는 `/Users/woopinbell/work/book-task-3/blog/blog-writing-guide.md` 기준으로 만들었고, `README`, `problem/`, 구현 README, `docs/`, 실제 소스코드, 테스트, `git log`, 2026-03-13 재검증 CLI만을 근거로 썼다.

## 공통 provenance

- 근거 우선순위는 루트 `README.md`, `docs/README.md`, 트랙 README, 프로젝트 `README.md`, `problem/README.md`, 구현 README, `docs/README.md`, 실제 `src/`/`tests/`/`app/`, `git log --reverse --stat`, `npm run verify --workspace ...` 순서를 따른다.
- 기존 `study/blog/*` 초안은 없었으므로 `isolate-and-rewrite`는 "기존 blog 입력 없이 새 blog를 생성"하는 방식으로 처리했다.
- `notion/`은 각 프로젝트에 존재하지만 이번 배치의 근거로 쓰지 않았다. 2026-03-09 커밋 `7813150`가 notion note drop이라는 사실만 `git log`로 확인하고, 실제 chronology는 README, 코드, 테스트, CLI로만 복원했다.
- 2026-03-13 재검증을 시작할 때 Playwright 브라우저가 없어 첫 E2E 실행이 막혔고, `npx playwright install chromium` 후 모든 canonical verify를 다시 통과시켰다. 이 조정은 배치 검증 provenance이지, 원래 프로젝트 개발 chronology 자체로 서술하지는 않는다.

## 프로젝트 색인

| 프로젝트 | evidence ledger | structure | 최종 blog |
| --- | --- | --- | --- |
| `frontend-foundations/01-semantic-layouts-and-a11y` | [01-evidence-ledger.md](frontend-foundations/01-semantic-layouts-and-a11y/01-evidence-ledger.md) | [02-structure.md](frontend-foundations/01-semantic-layouts-and-a11y/02-structure.md) | [10-development-timeline.md](frontend-foundations/01-semantic-layouts-and-a11y/10-development-timeline.md) |
| `frontend-foundations/02-dom-state-and-events` | [01-evidence-ledger.md](frontend-foundations/02-dom-state-and-events/01-evidence-ledger.md) | [02-structure.md](frontend-foundations/02-dom-state-and-events/02-structure.md) | [10-development-timeline.md](frontend-foundations/02-dom-state-and-events/10-development-timeline.md) |
| `frontend-foundations/03-networked-ui-patterns` | [01-evidence-ledger.md](frontend-foundations/03-networked-ui-patterns/01-evidence-ledger.md) | [02-structure.md](frontend-foundations/03-networked-ui-patterns/02-structure.md) | [10-development-timeline.md](frontend-foundations/03-networked-ui-patterns/10-development-timeline.md) |
| `react-internals/01-vdom-foundations` | [01-evidence-ledger.md](react-internals/01-vdom-foundations/01-evidence-ledger.md) | [02-structure.md](react-internals/01-vdom-foundations/02-structure.md) | [10-development-timeline.md](react-internals/01-vdom-foundations/10-development-timeline.md) |
| `react-internals/02-render-pipeline` | [01-evidence-ledger.md](react-internals/02-render-pipeline/01-evidence-ledger.md) | [02-structure.md](react-internals/02-render-pipeline/02-structure.md) | [10-development-timeline.md](react-internals/02-render-pipeline/10-development-timeline.md) |
| `react-internals/03-hooks-and-events` | [01-evidence-ledger.md](react-internals/03-hooks-and-events/01-evidence-ledger.md) | [02-structure.md](react-internals/03-hooks-and-events/02-structure.md) | [10-development-timeline.md](react-internals/03-hooks-and-events/10-development-timeline.md) |
| `react-internals/04-runtime-demo-app` | [01-evidence-ledger.md](react-internals/04-runtime-demo-app/01-evidence-ledger.md) | [02-structure.md](react-internals/04-runtime-demo-app/02-structure.md) | [10-development-timeline.md](react-internals/04-runtime-demo-app/10-development-timeline.md) |
| `frontend-portfolio/01-ops-triage-console` | [01-evidence-ledger.md](frontend-portfolio/01-ops-triage-console/01-evidence-ledger.md) | [02-structure.md](frontend-portfolio/01-ops-triage-console/02-structure.md) | [10-development-timeline.md](frontend-portfolio/01-ops-triage-console/10-development-timeline.md) |
| `frontend-portfolio/02-client-onboarding-portal` | [01-evidence-ledger.md](frontend-portfolio/02-client-onboarding-portal/01-evidence-ledger.md) | [02-structure.md](frontend-portfolio/02-client-onboarding-portal/02-structure.md) | [10-development-timeline.md](frontend-portfolio/02-client-onboarding-portal/10-development-timeline.md) |

## 읽는 순서

1. 루트 [../README.md](../README.md)와 [../docs/README.md](../docs/README.md)로 저장소 전체 질문과 검증 규칙을 먼저 확인한다.
2. 트랙별 README에서 같은 학습 축 안에서 프로젝트가 어떻게 이어지는지 본다.
3. 프로젝트별 `00-series-map.md`에서 source set과 canonical CLI를 확인한다.
4. `01-evidence-ledger.md`와 `02-structure.md`를 먼저 읽고, 마지막에 `10-development-timeline.md`로 실제 chronology를 따라간다.
