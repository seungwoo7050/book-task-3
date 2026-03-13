# 00-language-and-typescript series map

이 프로젝트는 `Node-Backend-Architecture`의 맨 앞에서, 이후 모든 레인이 기대할 입력·출력 계약을 먼저 세우는 자리다. 겉으로는 작은 TypeScript 연습처럼 보여도, 실제로는 "free-form 입력을 언제 정규화된 내부 표현으로 바꿀 것인가"를 처음 결정하는 프로젝트에 가깝다.

처음 읽을 때는 `catalog.ts`만 보면 충분하다. 여기서 slug, tags, summary가 어떤 규칙으로 고정되는지 잡히면, 뒤에 붙는 inventory 조회와 CLI 계약도 자연스럽게 읽힌다.

## 이 글에서 볼 것

- 왜 `BookDraft`를 바로 출력하지 않고 `NormalizedBook`으로 한 번 더 바꾸는지
- 비동기 inventory 조회를 붙이면서도 실패를 항목별로 가둔 이유가 무엇인지
- CLI가 단순 실행 래퍼가 아니라 종료 코드와 오류 메시지 계약이 되는 순간이 어디인지

## source of truth

- `bridge/00-language-and-typescript/README.md`
- `bridge/00-language-and-typescript/problem/README.md`
- `bridge/00-language-and-typescript/ts/src/catalog.ts`
- `bridge/00-language-and-typescript/ts/src/cli.ts`
- `bridge/00-language-and-typescript/ts/tests/catalog.test.ts`

## 구현 흐름 한눈에 보기

1. `catalog.ts`에서 slug, tags, summary를 만드는 정규화 경계를 세운다.
2. 같은 파일에서 `fetchInventorySnapshot`으로 비동기 실패를 항목별 결과로 바꾼다.
3. 마지막에 `cli.ts`에서 필수 플래그, stderr, exit code를 고정한다.

## 대표 검증

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
build: ok

$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
Test Files  1 passed (1)
Tests       6 passed (6)
```

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm start -- --title "Node Patterns" --author "Alice" --year 2024 --tags "Node, Architecture"
Node Patterns (2024)
Author: Alice
Slug: node-patterns-2024
Tags: architecture, node
Summary: Alice wrote Node Patterns in 2024.
Inventory: not requested
```

## 다음 프로젝트와의 연결

다음 장 `01-node-runtime-and-tooling`은 여기서 만든 입력 정리 감각을 메모리 안이 아니라 실제 파일, env, stream 위에서 다시 시험한다. 즉 값의 shape를 고정하는 단계에서, 런타임 입력을 다루는 단계로 넘어간다.
