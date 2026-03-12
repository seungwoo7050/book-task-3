# 문제 정의

프로비넌스: `adapted`

## 문제

동기 전체 render의 다음 단계는 무엇이 바뀌었는지 계산하고, 그 계산 결과를 언제 DOM에 반영할지 분리하는 것이다. 이 단계는 reconciliation과 fiber-like work loop를 "render pipeline"이라는 하나의 질문으로 묶어 구현한다.

## 제공 자산

- [original/README.md](original/README.md): 레거시 source map
- `code/`: 공통 디렉터리 shape를 유지하기 위한 placeholder
- `script/`: 공통 디렉터리 shape를 유지하기 위한 placeholder
- `data/`: 별도 입력 데이터가 없어 placeholder만 유지

## 제약

- `@front-react/vdom-foundations`의 VNode 구조를 그대로 사용한다.
- render phase 동안 DOM mutation을 하면 안 된다.
- keyed/unkeyed child diff를 모두 설명할 수 있어야 한다.

## 포함 범위

- `diffProps`
- `diffChildren`
- `diff`
- `applyPatches`
- `render`
- `workLoop`
- `flushSync`

## 제외 범위

- 함수 컴포넌트 state와 effect
- delegated events
- React의 priority/lanes 모델 전체

## 요구 산출물

- `ts/`에 실행 가능한 render pipeline 패키지 구현
- diff, patch, scheduler를 설명하는 공개 문서
- DOM patch ordering과 interrupted work를 검증하는 테스트

## Canonical Verification

```bash
cd study
npm run verify --workspace @front-react/render-pipeline
```

- `diff.test.ts`: prop delta, keyed/unkeyed child diff, replace patch 확인
- `patch.test.ts`: create/remove patch DOM 반영 확인
- `scheduler.test.ts`: render/commit 분리와 interrupted work 이후 commit 확인
