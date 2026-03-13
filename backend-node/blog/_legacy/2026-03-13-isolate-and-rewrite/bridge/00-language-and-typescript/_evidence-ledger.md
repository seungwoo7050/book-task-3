# 00-language-and-typescript evidence ledger

정확한 저장 시각이 공개돼 있지 않아서 chronology는 `Phase` 단위로 복원했다. 근거는 [`README.md`](../../../study/Node-Backend-Architecture/bridge/00-language-and-typescript/README.md), [`ts/src/catalog.ts`](../../../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/src/catalog.ts), [`ts/src/cli.ts`](../../../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/src/cli.ts), [`ts/tests/catalog.test.ts`](../../../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/tests/catalog.test.ts), 실제 `pnpm`/`node` 검증 출력뿐이다.

## Phase 1

- 순서: 1
- 시간 표지: Phase 1
- 당시 목표: 이후 백엔드 프로젝트에서 계속 쓸 도서 메타데이터 타입을 먼저 고정한다.
- 변경 단위: `ts/src/catalog.ts`
- 처음 가설: CLI보다 먼저 slug, tag, summary 같은 순수 변환 규칙이 안정돼야 나중에 HTTP나 DB 계층이 흔들리지 않는다.
- 실제 조치: `BookDraft`, `NormalizedBook`, `InventorySnapshot` 타입을 나누고 `toSlugPart()`, `normalizeTags()`, `toNormalizedBook()`으로 정규화 단계를 분리했다.
- CLI: `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build`
- 검증 신호: `tsc`가 통과하면서 변환 함수와 타입 경계가 빌드 단계에서 닫혔다.
- 핵심 코드 앵커: `normalizeTags()`, `toNormalizedBook()`
- 새로 배운 것: TypeScript 입문 단계에서도 핵심은 문법 암기가 아니라 "입력 draft와 외부에 보여 줄 normalized model을 분리하는 습관"이었다.
- 다음: 정규화된 slug 목록에 비동기 재고 조회를 붙여도 한 항목 실패가 전체 흐름을 깨지 않게 만든다.

## Phase 2

- 순서: 2
- 시간 표지: Phase 2
- 당시 목표: 비동기 inventory 조회를 붙이되 일부 실패가 전체 출력을 망치지 않게 만든다.
- 변경 단위: `ts/src/catalog.ts`
- 처음 가설: `Promise.all()`을 쓰더라도 각 slug마다 `try/catch`를 안쪽에 두면 batch 전체는 계속 진행될 수 있다.
- 실제 조치: `fetchInventorySnapshot()`이 slug별 `client.fetchStock()`을 호출하고, 실패 시 `inStock: null`과 `error`를 담아 반환하게 했다.
- CLI: `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`
- 검증 신호: `✓ tests/catalog.test.ts (6 tests)`, `Tests 6 passed (6)`
- 핵심 코드 앵커: `fetchInventorySnapshot()`
- 새로 배운 것: 비동기 코드는 "성공 path"보다 "실패를 어떤 단위에서 흡수할 것인가"를 먼저 정해야 이후 API나 queue 단계로 자연스럽게 확장된다.
- 다음: 이 타입과 비동기 규칙을 CLI 인자 파싱, 오류 메시지, 카드 출력으로 묶는다.

## Phase 3

- 순서: 3
- 시간 표지: Phase 3
- 당시 목표: 사람 눈에 바로 읽히는 CLI와 테스트로 언어 브리지를 닫는다.
- 변경 단위: `ts/src/cli.ts`, `ts/tests/catalog.test.ts`
- 처음 가설: 언어 브리지 프로젝트라도 실행 진입점이 없으면 다음 런타임 프로젝트로 이어지지 않는다.
- 실제 조치: `parseArgs()`가 필수 플래그를 검사하고 `runCli()`가 `formatBookCard()` 결과를 출력하거나 에러를 stderr로 보낸다.
- CLI: `node dist/cli.js --title "Node Patterns" --author "Alice" --year 2024 --tags "Node, Architecture"`
- 검증 신호: `Node Patterns (2024)`, `Tags: architecture, node`, `Inventory: not requested`
- 핵심 코드 앵커: `parseArgs()`, `runCli()`
- 새로 배운 것: CLI는 단순 데모가 아니라 "타입-정규화-출력"을 한 번에 검증하는 가장 작은 runtime surface다.
- 다음: [`../01-node-runtime-and-tooling/00-series-map.md`](../01-node-runtime-and-tooling/00-series-map.md)에서 같은 감각을 실제 파일 스트림과 env 처리로 확장한다.
