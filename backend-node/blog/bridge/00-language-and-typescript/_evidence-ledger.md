# 00-language-and-typescript evidence ledger

이 프로젝트의 `git log`는 `2026-03-12` 한 번의 이관 커밋으로 뭉쳐 있다. 아래 표는 그 시각을 세밀한 개발 로그처럼 오해하지 않기 위해, `problem -> src -> tests -> CLI` 순서로 다시 복원한 chronology다.

| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1 | 도서 입력을 바로 출력하지 않고 정규화된 내부 표현으로 먼저 바꾼다 | `ts/src/catalog.ts`의 `normalizeTags`, `toNormalizedBook` | 카드 한 장이면 문자열 가공도 한 함수로 끝낼 수 있을 것 같았다 | slug, tags, summary를 별도 함수로 나눠 `BookDraft -> NormalizedBook` 경계를 만들었다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build` | `build: ok` | `normalizeTags(tags.map(toSlugPart))` | 타입은 필드 선언보다 "정규화가 끝난 값의 모양"을 고정하는 쪽에서 더 빛난다 | 비동기 inventory를 붙여도 이 경계가 유지돼야 한다 |
| 2 | Phase 2 | 비동기 inventory 조회가 한 항목 실패로 전체 결과를 깨지 않게 한다 | `ts/src/catalog.ts`의 `fetchInventorySnapshot` | `Promise.all`이면 실패도 적당히 같이 처리될 거라고 보기 쉽다 | 각 slug를 개별 `try/catch`로 감싸 `inStock: null`과 `error`를 항목별로 남겼다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test` | `Test Files 1 passed`, `Tests 6 passed` | `slugs.map(async (slug) => { try { ... } catch { ... } })` | 배치 비동기 처리에서는 전체 성공보다 실패를 어디에 가둘지가 먼저다 | 이 결과를 사람이 읽는 CLI 표면으로 닫아야 한다 |
| 3 | Phase 3 | CLI 입력 오류와 정상 출력을 명시적 계약으로 만든다 | `ts/src/cli.ts`, `ts/tests/catalog.test.ts` | 예외만 던져도 터미널에서는 충분히 실패가 보일 것 같았다 | `stdout`, `stderr`, exit code를 분리하고 필수 플래그 오류를 테스트에 고정했다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm start -- --title "Node Patterns" --author "Alice" --year 2024 --tags "Node, Architecture"` | 카드 출력에 `Slug: node-patterns-2024`, `Tags: architecture, node`가 그대로 보였다 | `runCli(args, stdout, stderr): number` | CLI는 함수 래퍼가 아니라 입력 검증과 오류 보고를 결정하는 런타임 경계다 | 다음 프로젝트에서 파일과 env, stream이 들어오는 실제 Node 런타임으로 넘어간다 |

## 근거 파일

- `bridge/00-language-and-typescript/README.md`
- `bridge/00-language-and-typescript/problem/README.md`
- `bridge/00-language-and-typescript/ts/src/catalog.ts`
- `bridge/00-language-and-typescript/ts/src/cli.ts`
- `bridge/00-language-and-typescript/ts/tests/catalog.test.ts`
