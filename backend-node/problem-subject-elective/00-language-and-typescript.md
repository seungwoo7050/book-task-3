# 00-language-and-typescript 문제지

## 왜 중요한가

TypeScript 구현

## 목표

시작 위치의 구현을 완성해 입력 데이터를 타입으로 모델링하고 기본 검증을 수행할 것, 비동기 유틸리티와 에러 처리를 테스트로 검증할 것, CLI 실행 예시를 README만 보고 바로 재현할 수 있을 것을 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/problem/code/starter.ts`
- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/src/catalog.ts`
- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/src/cli.ts`
- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/tests/catalog.test.ts`
- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/problem/script/run-example.sh`
- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/pnpm-lock.yaml`
- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/tsconfig.json`
- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/package.json`

## starter code / 입력 계약

- ../study/Node-Backend-Architecture/bridge/00-language-and-typescript/problem/code/starter.ts에서 starter 코드와 입력 경계를 잡는다.

## 핵심 요구사항

- 입력 데이터를 타입으로 모델링하고 기본 검증을 수행할 것
- 비동기 유틸리티와 에러 처리를 테스트로 검증할 것
- CLI 실행 예시를 README만 보고 바로 재현할 수 있을 것

## 제외 범위

- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/problem/code/starter.ts` starter skeleton을 정답 구현으로 착각하지 않는다.
- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/problem/script/run-example.sh` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.

## 성공 체크리스트

- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/problem/code/starter.ts`의 빈 확장 지점을 실제 구현으로 채웠다.
- 핵심 흐름은 `toSlugPart`와 `normalizeTags`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `catalog helpers`와 `normalizes and deduplicates tags`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/Node-Backend-Architecture/bridge/00-language-and-typescript/problem/script/run-example.sh` 등 fixture/trace 기준으로 결과를 대조했다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts && npm run test -- --run
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`00-language-and-typescript_answer.md`](00-language-and-typescript_answer.md)에서 확인한다.
