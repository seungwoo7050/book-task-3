# Series Map — 01 Semantic Layouts And A11y

## 프로젝트 경계

- 트랙: `frontend-foundations`
- 프로젝트 루트: `study/frontend-foundations/01-semantic-layouts-and-a11y`
- 독립 프로젝트 판정 근거: 자체 `README.md`, `problem/README.md`, `vanilla/README.md`, `npm run verify --workspace @front-react/semantic-layouts-a11y`가 모두 존재하고, 구현/테스트 경로가 다른 폴더와 분리되어 있다.
- 기존 blog 처리: `isolate-and-rewrite`, 다만 기존 `study/blog/frontend-foundations/01-semantic-layouts-and-a11y`는 없어서 새로 생성했다.

## source of truth

- 포함: 프로젝트 README, `problem/README.md`, `docs/README.md`, `vanilla/README.md`, `vanilla/src/app.ts`, `vanilla/src/validation.ts`, `vanilla/tests/*`, `package.json`, `git log`, 2026-03-13 재검증 CLI
- 제외: `notion/**`, 이번에 새로 만든 `study/blog/**`

## chronology 복원 메모

- `git log --reverse --stat` 기준 visible change는 `46051f3`(2026-03-08, 코드/테스트/문서 landing), `7813150`(2026-03-09, notion note drop, 입력에서 제외), `0e12fb8`(2026-03-12, README/problem/docs polish) 세 지점이다.
- 구현 내부의 세부 순서는 commit 하나에 압축돼 있으므로, `problem` surface -> validation/accessibility invariant -> verify contract 순서로 다시 세웠다.
- 한 줄 답: semantic landmark와 validation/focus flow를 DOM 구조 자체로 드러내는 vanilla 설정 화면이다.

## canonical CLI

```bash
cd study
npm run verify --workspace @front-react/semantic-layouts-a11y
```

## series

1. [01-evidence-ledger.md](01-evidence-ledger.md)
2. [02-structure.md](02-structure.md)
3. [10-development-timeline.md](10-development-timeline.md)
