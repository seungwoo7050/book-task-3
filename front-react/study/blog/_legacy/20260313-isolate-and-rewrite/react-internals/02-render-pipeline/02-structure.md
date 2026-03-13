# 02 Render Pipeline structure

## opening frame

- 한 줄 훅: 이 단계의 변화는 "더 빨라졌다"가 아니라 render와 commit를 분리할 수 있게 되었다는 데 있다.
- chronology 주의: code landing은 한 commit이지만, 실제 이해 순서는 `diff -> patch -> scheduler`가 더 자연스럽다.
- 첫 질문: 무엇이 바뀌었는지 계산하고, 그 계산 결과를 언제 DOM에 반영할지를 어떻게 분리했는가.

## chapter flow

1. README와 problem 문서로 pipeline의 범위를 먼저 고정한다.
2. `diffChildrenByKey`와 `diff`로 patch calculation을 설명한다.
3. `commitRoot`와 `workLoop`로 render/commit split을 닫고 verify로 확인한다.

## evidence allocation

- 도입: `README.md`, `problem/README.md`, `git log`
- 본문 1: `ts/src/diff.ts`
- 본문 2: `ts/src/scheduler.ts`
- 본문 3: `npm run verify --workspace @front-react/render-pipeline`, `ts/tests/*`

## tone guardrails

- render pipeline을 성능 광고처럼 쓰지 않고, phase separation과 patch ordering의 이유를 코드 수준으로 설명한다.
- keyed/unkeyed diff와 scheduler를 하나의 흐름으로 연결한다.
- notion과 새 blog는 입력에서 제외한다.
