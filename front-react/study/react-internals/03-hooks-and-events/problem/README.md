# 문제 정의

프로비넌스: `adapted`

## 문제

함수 컴포넌트 state, effect cleanup, delegated event를 각각 따로 구현하는 대신, 세 가지가 하나의 runtime loop 안에서 어떻게 이어지는지 보여 주는 학습용 runtime을 만든다.

## 제공 자산

- [original/README.md](original/README.md): 레거시 source map
- `code/`: 공통 디렉터리 shape를 유지하기 위한 placeholder
- `script/`: 공통 디렉터리 shape를 유지하기 위한 placeholder
- `data/`: 별도 입력 데이터가 없어 placeholder만 유지

## 제약

- `@front-react/render-pipeline`의 diff/patch helper를 그대로 소비한다.
- hook order invariant를 지켜야 한다.
- delegated event는 runtime tree 메타데이터를 통해 처리해야 한다.

## 포함 범위

- function component execution
- `useState`
- `useEffect`와 cleanup lifecycle
- delegated event bubbling
- `stopPropagation`
- runtime integration

## 제외 범위

- `useMemo`, `useReducer`, `context`
- React의 synthetic event 전체 호환성
- concurrent semantics 전체

## 요구 산출물

- `ts/`에 실행 가능한 hooks/events runtime 구현
- hook slot, effect timing, delegated event를 설명하는 공개 문서
- state, effect, event integration을 검증하는 테스트

## Canonical Verification

```bash
cd study
npm run verify --workspace @front-react/hooks-and-events
```

- `state.test.ts`: rerender와 hook order invariant 확인
- `effect.test.ts`: setup/cleanup ordering과 unmount cleanup 확인
- `events.test.ts`, `integration.test.ts`: delegated event와 runtime integration 확인
