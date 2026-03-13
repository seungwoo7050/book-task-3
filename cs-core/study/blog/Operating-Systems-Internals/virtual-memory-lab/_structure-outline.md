# Virtual Memory Lab Structure Outline

이 문서는 최종 blog를 어떤 곡선으로 읽히게 만들지 미리 고정하는 편집 설계 메모다. 근거는 모두 `01-evidence-ledger.md`와 실제 소스에서 왔고, 여기서는 그 근거를 어떤 순서로 보여 줄 때 가장 자연스럽게 이해되는지에 집중한다.

## 이 시리즈의 편집 원칙

Virtual Memory Lab에서는 결론을 먼저 선언하기보다, 구현이 어디서부터 단단해졌는지를 보여 주는 편이 더 중요하다. 그래서 최종 글은 문제를 좁히는 첫 장면, 설계가 갈라지는 중간 장면, 검증이 닫히는 마지막 장면의 세 구간으로 나눈다. 각 구간은 코드와 CLI가 함께 등장해야 하고, 다음 phase로 넘어가는 질문이 문단 끝에 남아 있어야 한다.

## 최종 글의 흐름

1. 도입에서 `make test && make run-demo`와 현재 재작성 범위를 먼저 밝히고, 독자가 이 글이 어떤 evidence layer 위에 서 있는지 알게 한다.
2. 본문은 Phase 1 trace와 frame state를 읽는 공통 루프를 먼저 만든다 -> Phase 2 replacement policy와 writeback 차이를 별도 규칙으로 드러낸다 -> Phase 3 trace replay와 summary metric으로 실험을 닫는다 순서로 간다. 순서를 바꾸지 않는 이유는 이 흐름이 README와 테스트가 실제로 요구하는 구현 순서에 가장 가깝기 때문이다.
3. 마지막에는 CLI excerpt와 남은 질문을 붙여, 이 프로젝트가 어디까지 닫혔고 어디가 다음 학습 포인트인지 분명하게 남긴다.

## 1. Phase 1 - trace와 frame state를 읽는 공통 루프를 먼저 만든다

이 구간의 중심 장면은 page replacement 비교도 먼저 필요한 것은 trace와 frame state를 어떤 형식으로 표현할지다.

본문에서는 먼저 LRU/FIFO/Clock/OPT를 바로 구현하기보다 trace parsing과 공통 simulate loop를 먼저 고정하는 편이 훨씬 덜 흔들릴 거라고 봤다. 그 다음 문단에서는 `load_trace`, `simulate_policy`, frame rendering helper를 먼저 세워 공통 실험면을 만들었다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `load_trace`, `simulate_policy`
- 붙일 CLI: `make test && make run-demo`
- 강조할 검증 신호: 공통 루프가 있으니 정책 차이를 좁은 함수 범위에서 설명할 수 있다.
- 장면이 끝날 때 남길 문장: policy-specific 선택 로직과 dirty page 처리로 넘어간다.

## 2. Phase 2 - replacement policy와 writeback 차이를 별도 규칙으로 드러낸다

이 구간의 중심 장면은 Clock/OPT 선택 함수와 dirty page summary가 이 lab의 실제 개념 전환점이다.

본문에서는 먼저 policy 차이를 단순 fault count로만 설명하면 locality와 writeback 규칙의 차이가 묻힐 것이라고 판단했다. 그 다음 문단에서는 `_clock_select`, `_opt_select`, `render_summary`를 중심으로 eviction과 dirty-page signal을 동시에 보여 주도록 정리했다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `_clock_select`, `_opt_select`
- 붙일 CLI: `make test && make run-demo`
- 강조할 검증 신호: 정책 helper와 summary renderer가 같은 판단 전환점을 보존한다.
- 장면이 끝날 때 남길 문장: demo trace와 summary 출력을 통해 결과를 닫는다.

## 3. Phase 3 - trace replay와 summary metric으로 실험을 닫는다

이 구간의 중심 장면은 VM lab도 결국 외부에서 읽히는 것은 trace별 fault/writeback 차이와 frame replay다.

본문에서는 먼저 CLI가 남아 있어야 locality와 replacement policy 설명이 표 한 장으로 축약되지 않을 것이라고 봤다. 그 다음 문단에서는 `make run-demo`와 `render_replay` surface를 통해 locality/dirty trace를 다시 재생하고 요약하게 만들었다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `main`, `test_dirty_evictions_counted`
- 붙일 CLI: `make test && make run-demo`
- 강조할 검증 신호: 현재 demo 출력이 정책별 차이를 수치로 남긴다.
- 장면이 끝날 때 남길 문장: common trace loop -> policy selection -> replay summary 순서로 닫는다.

## Fixed CLI Anchor

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Operating-Systems-Internals/virtual-memory-lab/problem && make test && make run-demo)
```

이 명령은 최종 글 마지막에서 README 계약이 여전히 살아 있다는 사실을 다시 확인하는 closing shot로 사용한다.
