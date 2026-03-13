# 04 Runtime Demo App structure

## opening frame

- 한 줄 훅: 이 앱의 핵심은 예쁜 demo가 아니라 직접 만든 runtime을 복사본 없이 소비해도 search, pagination, metrics가 끝까지 버티는지 보여 주는 데 있다.
- chronology 주의: code landing은 한 commit에 압축돼 있으므로, 글은 `consumer app scope -> debounced search + metrics -> verify` 순서로 재구성한다.
- 첫 질문: shared runtime을 실제 상호작용 앱에 얹었을 때 어디까지 설명 가능하고 어디서 멈추는가.

## chapter flow

1. README와 problem 문서로 consumer app의 public contract를 먼저 고정한다.
2. `useDebouncedValue`, `updateMetrics`, `DemoApp`으로 상호작용과 관찰값을 설명한다.
3. verify 결과로 debounce/pagination/metrics 시나리오를 닫고 한계를 적는다.

## evidence allocation

- 도입: `README.md`, `problem/README.md`, `git log`
- 본문 1: `ts/src/app.ts`의 debounced search
- 본문 2: `ts/src/app.ts`의 metrics update
- 본문 3: `npm run verify --workspace @front-react/runtime-demo-app`, `ts/tests/demo.test.ts`

## tone guardrails

- demo app을 showcase 설명으로만 쓰지 말고, shared runtime consumption이 왜 중요한지 계속 연결한다.
- metrics를 profiler처럼 과장하지 않고 learning signal이라고 명시한다.
- notion과 새 blog는 입력 근거에서 제외한다.
