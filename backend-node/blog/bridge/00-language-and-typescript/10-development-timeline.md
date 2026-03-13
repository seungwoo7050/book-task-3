# 00-language-and-typescript development timeline

이 프로젝트는 TypeScript 문법을 훑는 글처럼 시작하지만, 실제로 따라가 보면 문법보다 먼저 등장하는 건 경계다. 문자열을 어떻게 정리할지, 비동기 실패를 어디에 가둘지, CLI가 어떤 종료 코드를 돌려줄지 같은 결정이 먼저 나오고, 타입은 그 결정을 붙잡아 두는 역할을 한다.

## 흐름 먼저 보기

1. `catalog.ts`에서 정규화된 내부 표현을 먼저 만든다.
2. 그 위에 inventory 조회를 올리되, 실패를 전체가 아니라 항목별 결과로 바꾼다.
3. 마지막으로 CLI가 이 결과를 어떻게 보여 줄지, 실패를 어떻게 끝낼지 정한다.

## 정규화 경계를 먼저 세운 장면

처음 읽어야 할 곳은 `toNormalizedBook`보다 한 단계 앞에 있는 `normalizeTags`다. 이 프로젝트가 중요해지는 이유가 바로 여기에 있다.

```ts
export function normalizeTags(tags: string[]): string[] {
  return [...new Set(tags.map(toSlugPart).filter((tag) => tag.length > 0))].sort();
}
```

이 한 줄짜리 정리에 가까운 함수가 왜 중요한가 하면, 뒤에서 CLI를 만들든 테스트를 쓰든 더 이상 "사용자가 어떤 공백과 대소문자로 넣었는가"를 신경 쓰지 않아도 되기 때문이다. 입력의 흔들림을 초기에 흡수해 두면, 이후 단계는 정규화된 값만 상대하면 된다.

같은 이유로 `toNormalizedBook`도 프로젝트의 중심축이 된다.

```ts
const slug = `${toSlugPart(draft.title)}-${draft.publishedYear}`;
const summary = description && description.length > 0
  ? description
  : `${author} wrote ${title} in ${draft.publishedYear}.`;
```

여기서 정리되는 건 단순 문자열이 아니다. 이 프로젝트가 어떤 내부 상태를 "완성된 책 카드"로 인정할지에 대한 기준이다. 그래서 타입 모델링이 필드 목록을 예쁘게 적는 일보다, 정규화 이후의 값을 고정하는 일에 더 가깝게 느껴진다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
build: ok
```

`tsc`가 통과했다는 사실 자체보다, 타입 정의와 CLI 진입점이 같은 전제를 공유하기 시작했다는 게 더 중요했다.

## 비동기 실패를 항목별로 묶어 둔 장면

정규화된 책 카드 위에 inventory 조회를 붙이는 순간, 이 프로젝트는 더 흥미로워진다. 여기서 중요한 질문은 "모두 성공하느냐"가 아니라 "실패를 어디에 두느냐"였다.

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

`Promise.all`을 쓰고 있다는 사실보다 중요한 건, 각 slug가 자기 실패를 자기 결과 안에만 품고 끝난다는 점이다. 이 결정 덕분에 깨진 항목 하나가 전체 카드 목록을 망치지 않는다.

테스트도 그 전환점을 정확히 붙잡고 있다.

```ts
await expect(fetchInventorySnapshot(["clean-book", "broken-book"], { fetchStock })).resolves.toEqual([
  { slug: "clean-book", inStock: 10 },
  { slug: "broken-book", inStock: null, error: "service unavailable" },
]);
```

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
Test Files  1 passed (1)
Tests       6 passed (6)
Duration    280ms
```

여기서 처음 또렷해지는 건, 배치 비동기에서 중요한 건 메커니즘보다 복구 전략이라는 점이다. `Promise.all`은 도구일 뿐이고, 실제 설계는 실패를 어떤 모양으로 되돌려줄지에서 갈린다.

## CLI 계약으로 닫아 둔 장면

마지막 장면은 `runCli`다. 여기서 프로젝트는 라이브러리 같은 코드 덩어리에서, 실제로 사람이 실행하는 작은 도구로 바뀐다.

```ts
export function runCli(args: string[], stdout: WriteTarget, stderr: WriteTarget): number {
  try {
    const draft = parseArgs(args);
    const normalized = toNormalizedBook(draft);
    stdout.write(`${formatBookCard(normalized)}\n`);
    return 0;
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown CLI error";
    stderr.write(`${message}\n`);
    return 1;
  }
}
```

이 함수가 중요한 이유는 예외를 없애서가 아니다. 실패를 stack trace가 아니라, 사람이 해석 가능한 stderr 메시지와 exit code로 바꿨기 때문이다. 테스트도 정확히 그 계약을 본다.

```ts
const exitCode = runCli(["--title", "Only Title"], stdout, stderr);
expect(exitCode).toBe(1);
expect(stderr.write).toHaveBeenCalledWith("Required flags: --title --author --year --tags\n");
```

실제 출력도 이 계약을 그대로 따른다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm start -- --title "Node Patterns" --author "Alice" --year 2024 --tags "Node, Architecture"
Node Patterns (2024)
Author: Alice
Slug: node-patterns-2024
Tags: architecture, node
Summary: Alice wrote Node Patterns in 2024.
Inventory: not requested
```

이 지점에서야 이 프로젝트가 왜 bridge의 첫 장면인지 선명해진다. 타입과 함수 분해를 배운 것이 아니라, 이후 모든 프로젝트가 반복할 "입력 정리 -> 신뢰 가능한 내부 표현 -> 명시적인 CLI 계약"을 한 번 먼저 겪은 셈이기 때문이다.

다음 프로젝트에서는 이 감각이 메모리 안을 벗어나 디스크와 env, stream이 섞인 실제 Node 런타임으로 옮겨 간다.
