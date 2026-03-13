# 00-language-and-typescript series map

`00-language-and-typescript`는 backend-node 전체에서 가장 작지만, 이후 모든 프로젝트가 기대하는 타입 감각을 먼저 정하는 시작점이다. 그래서 이 시리즈는 "도서 draft를 어떤 모델로 정규화하고, 그 결과를 어떤 CLI surface로 닫았는가"라는 질문으로 읽는 편이 가장 정확했다.

## 복원 원칙

- chronology는 git 커밋이 아니라 [`ts/src/catalog.ts`](../../../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/src/catalog.ts)와 [`ts/src/cli.ts`](../../../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/src/cli.ts)의 의존 순서로 복원한다.
- 검증은 [`ts/tests/catalog.test.ts`](../../../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/tests/catalog.test.ts)와 실제 `pnpm`/`node` 실행 출력으로 닫는다.
- README의 실행 문구는 참고만 하고, 실제 재검증은 빌드된 `dist/cli.js`를 직접 호출해 남겼다.

## 대표 검증

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ node dist/cli.js --title "Node Patterns" --author "Alice" --year 2024 --tags "Node, Architecture"
```

## 글 순서

1. [10-development-timeline.md](10-development-timeline.md)
   타입 정규화, 비동기 inventory 조회, CLI 출력이 어떤 순서로 붙었는지 한 번에 따라간다.
