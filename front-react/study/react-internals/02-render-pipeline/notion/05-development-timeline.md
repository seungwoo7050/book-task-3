# 개발 타임라인 — render pipeline 프로젝트 구축 과정

## Phase 0: 프로젝트 초기화

```bash
cd study
```

workspace 루트의 `package.json`에 `@front-react/render-pipeline` workspace가 이미 등록되어 있다. 02-render-pipeline 디렉토리 안에서 `package.json`의 name을 `@front-react/render-pipeline`으로 설정하고, vdom-foundations를 의존으로 추가했다.

```bash
npm install
```

workspace symlink가 생성되면서 `@front-react/vdom-foundations`를 import할 수 있게 된다. node_modules 안에 01 프로젝트로의 symlink가 만들어진다.

## Phase 1: 타입 정의

types.ts를 먼저 작성했다. 

```
ts/src/types.ts
```

vdom-foundations에서 VNode, VNodeProps를 re-export하고, 이 프로젝트 고유의 타입을 정의:
- PatchType, PropsPatch, Patch — diff/patch 축
- EffectTag, Fiber, IdleDeadlineLike — fiber 축

타입을 먼저 확정하면 나머지 모듈의 시그니처가 결정된다.

## Phase 2: diff 모듈 구현

```
ts/src/diff.ts
ts/tests/diff.test.ts
```

diffProps → diffChildren (keyed/unkeyed) → diff 순으로 bottom-up 구현. 각 함수를 만들 때마다 테스트를 작성하고 실행:

```bash
npm run test --workspace @front-react/render-pipeline
```

diff.test.ts에서 검증하는 시나리오:
- prop 변경과 제거 계산
- 인덱스 기반 child diff
- key 기반 child diff (create/remove 발생)
- 타입 변경 시 replace patch

## Phase 3: patch 모듈 구현

```
ts/src/patch.ts
ts/tests/patch.test.ts
```

applyPatches 구현 시 jsdom 환경에서 DOM 조작을 테스트한다. vitest.config.ts에 `environment: 'jsdom'`이 설정되어 있어 document, HTMLElement 등을 쓸 수 있다.

```bash
npm run test --workspace @front-react/render-pipeline -- --run patch
```

patch.test.ts에서 create → 삽입 확인 → remove → 빈 container 확인까지 검증.

## Phase 4: fiber 모듈 구현

```
ts/src/fiber.ts
```

reconcileChildren과 performUnitOfWork를 구현. 이 모듈은 scheduler와 함께 통합 테스트로 검증하므로 별도 단위 테스트 파일은 없다.

reconcileChildren에서 onDelete 콜백 패턴을 도입 — 삭제 대상 fiber를 외부(scheduler)에서 수집하도록 분리.

## Phase 5: scheduler 구현

```
ts/src/scheduler.ts
ts/tests/scheduler.test.ts
```

모듈 레벨 상태 변수(nextUnitOfWork, wipRoot, currentRoot, deletions) 설정. render → workLoop → commitRoot 흐름 구현.

scheduler.test.ts가 render pipeline의 핵심 동작 세 가지를 검증:

```bash
npm run test --workspace @front-react/render-pipeline -- --run scheduler
```

1. render 직후 DOM 미변경
2. flushSync 후 완전한 DOM
3. interrupted work 후 일관된 commit

## Phase 6: barrel export 구성

```
ts/src/index.ts
```

모든 구현과 타입을 단일 진입점에서 re-export. vdom-foundations에서 가져온 함수도 함께 내보내서 이 패키지만으로 완결된 API를 제공.

## Phase 7: 타입 체크

```bash
npm run typecheck --workspace @front-react/render-pipeline
```

tsconfig.json에서 strict 모드 활성화. vdom-foundations의 타입과 이 프로젝트의 타입이 올바르게 연결되는지 확인.

## Phase 8: 문서 작성

```
docs/concepts/diff-and-patch-scope.md
docs/concepts/render-vs-commit.md
docs/references/verification-notes.md
```

구현 후 설계 결정을 문서화. diff-and-patch-scope.md에 범위 제한 이유를, render-vs-commit.md에 phase 분리 mental model을 기록.

## Phase 9: 전체 검증

```bash
cd study
npm run verify --workspace @front-react/render-pipeline
```

verify 스크립트가 타입 체크 + 테스트를 순서대로 실행. 모든 검증 통과 후 `verified` 상태로 전환.

## 사용된 도구 정리

| 도구 | 용도 |
|------|------|
| TypeScript 5.3 | 타입 안전 보장, strict mode |
| Vitest 1.6.0 | 단위 테스트, jsdom 환경 |
| jsdom 24.0.0 | DOM API 에뮬레이션 |
| npm workspaces | 로컬 패키지 의존 관리 |

## 디렉토리 구조

```
02-render-pipeline/
├── package.json          # @front-react/render-pipeline
├── tsconfig.json
├── vitest.config.ts
├── README.md
├── docs/
│   ├── concepts/
│   │   ├── diff-and-patch-scope.md
│   │   └── render-vs-commit.md
│   └── references/
│       └── verification-notes.md
├── problem/              # 레거시 원문
├── ts/
│   ├── src/
│   │   ├── types.ts      # 타입 정의
│   │   ├── diff.ts       # 변경 계산
│   │   ├── patch.ts      # DOM 반영
│   │   ├── fiber.ts      # fiber reconciliation
│   │   ├── scheduler.ts  # render/commit 분리
│   │   └── index.ts      # barrel export
│   └── tests/
│       ├── diff.test.ts
│       ├── patch.test.ts
│       └── scheduler.test.ts
└── notion/               # (로컬 전용)
```
