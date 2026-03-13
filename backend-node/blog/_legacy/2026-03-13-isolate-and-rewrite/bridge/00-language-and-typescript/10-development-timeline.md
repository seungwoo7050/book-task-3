# 00-language-and-typescript development timeline

이 프로젝트는 기능 수가 적어서 오히려 시작점이 선명하다. Express나 NestJS로 넘어가기 전에 먼저 고정해야 했던 건 HTTP가 아니라 "문자열 입력을 어떤 타입 모델로 정리할 것인가"였다. 실제 소스를 따라가 보면 이 순서는 `catalog.ts`에서 타입과 정규화 규칙을 세우고, 그 다음 비동기 inventory 조회 실패를 묶고, 마지막에 CLI로 묶는 흐름으로 아주 뚜렷하게 남아 있다.

## 구현 순서 요약

- `BookDraft -> NormalizedBook` 변환 규칙을 먼저 만든다.
- slug 목록을 비동기 inventory 조회와 연결하되 부분 실패를 batch 안에서 흡수한다.
- CLI가 필수 플래그, 오류 메시지, 카드 출력을 책임지게 해 언어 브리지를 runtime surface로 닫는다.

## Phase 1

- 당시 목표: 입력 draft와 외부에 보여 줄 normalized model을 분리한다.
- 변경 단위: `ts/src/catalog.ts`
- 처음 가설: title, tag, summary 규칙을 여기서 고정해 두면 이후 어떤 프레임워크를 붙여도 도메인 설명이 흔들리지 않는다.
- 실제 진행: `BookDraft`, `NormalizedBook`, `InventorySnapshot`을 분리하고 `toSlugPart()`, `normalizeTags()`, `toNormalizedBook()`으로 정규화 단계를 쪼갰다.

CLI:

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
✓ tests/catalog.test.ts (6 tests)
Tests 6 passed (6)
```

검증 신호:

- `normalizeTags([" Node ", "architecture", "node", "Type Script"])`가 `["architecture", "node", "type-script"]`로 닫힌다.
- `toNormalizedBook()` 테스트가 slug, trimmed title, 기본 summary를 한 번에 고정한다.

핵심 코드:

```ts
export function normalizeTags(tags: string[]): string[] {
  return [...new Set(tags.map(toSlugPart).filter((tag) => tag.length > 0))].sort();
}
```

왜 이 코드가 중요했는가:

중복 제거와 slug화가 여기서 끝나야 나중에 inventory 조회나 HTTP path parameter가 "입력 정리" 책임을 다시 떠안지 않는다. 이 한 줄이 단순한 편의 함수가 아니라 이후 프로젝트 전체의 naming contract였다.

새로 배운 것:

- TypeScript 학습에서 중요한 건 `type`을 많이 쓰는 것이 아니라 "어느 시점부터는 raw input을 더 이상 믿지 않는다"는 경계를 모델로 표현하는 일이다.

## Phase 2

- 당시 목표: inventory 조회를 붙이면서도 한 항목 실패가 전체 결과를 날리지 않게 만든다.
- 변경 단위: `ts/src/catalog.ts`
- 처음 가설: `Promise.all()`을 쓰되 실패를 바깥으로 던지지 않고 각 slug 내부에서 흡수하면, batch는 유지되고 결과는 더 설명적이 된다.
- 실제 진행: `fetchInventorySnapshot()`이 slug별 `client.fetchStock()`을 호출하고 예외를 `error` 필드로 바꿔 넣는다.

CLI:

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
✓ tests/catalog.test.ts (6 tests)
Tests 6 passed (6)
```

검증 신호:

- 테스트는 `clean-book`은 `inStock: 10`, `broken-book`은 `inStock: null`과 `service unavailable`을 받는 장면을 고정한다.
- 즉 "부분 실패"가 에러 전파가 아니라 결과 모델의 일부가 된다.

핵심 코드:

```ts
return Promise.all(
  slugs.map(async (slug) => {
    try {
      const inStock = await client.fetchStock(slug);
      return { slug, inStock };
    } catch (error) {
      return {
        slug,
        inStock: null,
        error: error instanceof Error ? error.message : "Unknown inventory error",
      };
    }
  }),
);
```

왜 이 코드가 중요했는가:

나중에 auth, cache, DB 같은 외부 의존을 붙일 때도 핵심은 "실패를 어디서 흡수하고 어디서 계약으로 노출할 것인가"다. 이 프로젝트는 그 결정을 아주 작은 inventory 예제로 먼저 연습한다.

새로 배운 것:

- 비동기 코드는 속도보다 격리 단위가 먼저다. batch 전체를 실패시킬지, 항목 단위로 실패를 수집할지는 여기서 이미 결정된다.

## Phase 3

- 당시 목표: 타입과 비동기 규칙을 CLI 진입점으로 묶어 실제로 실행 가능한 프로젝트로 만든다.
- 변경 단위: `ts/src/cli.ts`, `ts/tests/catalog.test.ts`
- 처음 가설: 언어 브리지라도 실행 진입점이 없으면 문법 연습 메모에 머문다.
- 실제 진행: `parseArgs()`가 필수 플래그와 연도 형식을 검사하고, `runCli()`가 `formatBookCard()`를 stdout에 쓰거나 에러를 stderr에 남긴다.

CLI:

```bash
$ node dist/cli.js --title "Node Patterns" --author "Alice" --year 2024 --tags "Node, Architecture"
Node Patterns (2024)
Author: Alice
Slug: node-patterns-2024
Tags: architecture, node
Summary: Alice wrote Node Patterns in 2024.
Inventory: not requested
```

검증 신호:

- 성공 케이스는 사람이 읽는 카드 형식으로 닫힌다.
- 실패 케이스는 `Required flags: --title --author --year --tags`를 stderr에 남기고 exit code 1을 반환한다.

핵심 코드:

```ts
if (!title || !author || !yearValue || !tagsValue) {
  throw new Error("Required flags: --title --author --year --tags");
}
```

왜 이 코드가 중요했는가:

이 시점부터 프로젝트는 "타입이 맞다"에서 끝나지 않고 "실행 entrypoint가 잘못된 입력을 어떻게 거절하는가"까지 설명할 수 있게 된다. 다음 런타임 프로젝트가 파일 경로와 env를 받는 것도 같은 이유다.

새로 배운 것:

- CLI는 보너스가 아니라 가장 작은 adapter다. 이 adapter가 있어야 타입 모델이 실제 입력과 출력에 닿는다.

다음:

- [`../01-node-runtime-and-tooling/00-series-map.md`](../01-node-runtime-and-tooling/00-series-map.md)에서 이 adapter 감각을 파일 스트림, env, JSON report로 확장한다.
