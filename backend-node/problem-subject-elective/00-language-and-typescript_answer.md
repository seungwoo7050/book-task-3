# 00-language-and-typescript 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 입력 데이터를 타입으로 모델링하고 기본 검증을 수행할 것, 비동기 유틸리티와 에러 처리를 테스트로 검증할 것, CLI 실행 예시를 README만 보고 바로 재현할 수 있을 것을 한 흐름으로 설명하고 검증한다. 핵심은 `toSlugPart`와 `normalizeTags`, `toNormalizedBook` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 입력 데이터를 타입으로 모델링하고 기본 검증을 수행할 것
- 비동기 유틸리티와 에러 처리를 테스트로 검증할 것
- CLI 실행 예시를 README만 보고 바로 재현할 수 있을 것
- 첫 진입점은 `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/src/catalog.ts`이고, 여기서 `toSlugPart`와 `normalizeTags` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/src/catalog.ts`: `toSlugPart`, `normalizeTags`, `toNormalizedBook`, `fetchInventorySnapshot`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/src/cli.ts`: `readFlag`, `parseArgs`, `runCli`, `,`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/problem/code/starter.ts`: `normalizeTags`, `toNormalizedBook`, `fetchInventorySnapshot`, `formatBookCard`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/tests/catalog.test.ts`: `catalog helpers`, `normalizes and deduplicates tags`, `builds a normalized book`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/problem/script/run-example.sh`: 검증 절차나 보조 자동화를 담아 결과를 재현하는 스크립트다.
- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/pnpm-lock.yaml`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.
- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/tsconfig.json`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.
- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/package.json`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.

## 정답을 재구성하는 절차

1. `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/problem/code/starter.ts`와 `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/src/catalog.ts`를 나란히 열어 먼저 바뀌는 경계를 잡는다.
2. `catalog helpers` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts && npm run test -- --run`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts && npm run test -- --run
```

- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/problem/code/starter.ts` starter skeleton의 빈칸을 그대로 정답으로 착각하지 않는다.
- `catalog helpers`와 `normalizes and deduplicates tags`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts && npm run test -- --run`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/src/catalog.ts`
- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/src/cli.ts`
- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/problem/code/starter.ts`
- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/tests/catalog.test.ts`
- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/problem/script/run-example.sh`
- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/pnpm-lock.yaml`
- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/tsconfig.json`
- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/package.json`
- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/vitest.config.ts`
