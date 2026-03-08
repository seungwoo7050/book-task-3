# TypeScript Implementation

프로비넌스: `authored`

이 디렉터리는 `01-vdom-foundations`의 현재 실행 가능한 구현과 테스트를 담는다.

## problem scope covered

- `createElement`
- `createTextElement`
- `createDom`
- `updateDom`
- `render`

## build command

이 프로젝트는 별도 빌드 없이 타입체크 중심으로 검증한다.

```bash
cd study
npm run typecheck:vdom
```

## test command

```bash
cd study
npm run test:vdom
```

## current status

- `verified`

## known gaps

- 동기 재귀 렌더만 지원한다.
- 함수 컴포넌트 실행, diff/patch, scheduler, hooks, delegation은 아직 없다.
- `null` 같은 특수 child 값은 최소 구현 범위 밖이다.

## implementation notes

- `ts/src/`는 레거시 `solve/solution/`을 새 구조에 맞게 옮긴 코드다.
- `ts/tests/`는 레거시 `solve/test/`를 새 경로에 맞춰 옮긴 테스트다.
- `ts/src/index.ts`를 통해 이후 단계가 패키지 형태로 이 코드를 소비할 수 있게 했다.
