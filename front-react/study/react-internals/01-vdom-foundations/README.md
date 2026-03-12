# 01 VDOM Foundations

상태: `verified`

## 무슨 문제인가

이 단계는 JSX와 실제 DOM 사이에 최소한의 Virtual DOM 계층을 직접 만들면서, `createElement`에서 `render`까지의 경로가 어떤 데이터 구조와 DOM 조작으로 이어지는지 확인하는 문제를 푼다.

## 왜 필요한가

프레임워크를 사용하는 입장만으로는 React의 갱신 모델과 제약을 설명하기 어렵다. 이 단계는 JSX가 어떤 객체로 바뀌고, 그 객체가 실제 DOM으로 물질화되는지 가장 작은 단위에서 보여 준다.

## 내가 만든 답

`createElement`, `createTextElement`, `createDom`, `updateDom`, `render`를 구현한 TypeScript 패키지를 만들고, 이후 단계가 이 패키지를 직접 소비하도록 구성했다.

- 문제 정의: [problem/README.md](problem/README.md)
- 구현 상세: [ts/README.md](ts/README.md)
- 공개 문서: [docs/README.md](docs/README.md)

## 핵심 구현 포인트

- `ts/src/element.ts`에서 primitive child를 `TEXT_ELEMENT`로 정규화한다.
- `ts/src/dom-utils.ts`에서 DOM 생성과 prop/event 반영, 동기 재귀 render를 처리한다.
- `ts/src/index.ts`에서 다음 단계가 소비할 패키지 경계를 고정한다.

## 검증

```bash
cd study
npm run test:vdom
npm run typecheck:vdom
npm run verify:vdom
```

- 검증 일시: 2026-03-07
- `vitest`: `element.test.ts`, `dom-utils.test.ts` 포함 `27`개 테스트 통과
- `typecheck`: `@front-react/vdom-foundations` 패키지 타입 검사 통과

## 읽기 순서

1. [problem/README.md](problem/README.md)
2. [ts/README.md](ts/README.md)
3. [docs/README.md](docs/README.md)

## 한계

- 전체 트리를 매번 동기적으로 렌더한다.
- 변경 집합을 계산하지 않으므로 최소 DOM 갱신이 없다.
- 상태, effect, 스케줄러, 이벤트 위임은 아직 없다.
- 다음 단계인 `02-render-pipeline`에서 diff와 commit 타이밍 분리를 다룬다.
