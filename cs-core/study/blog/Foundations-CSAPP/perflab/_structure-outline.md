# Performance Lab Structure Outline

이 문서는 최종 blog를 어떤 곡선으로 읽히게 만들지 미리 고정하는 편집 설계 메모다. 근거는 모두 `01-evidence-ledger.md`와 실제 소스에서 왔고, 여기서는 그 근거를 어떤 순서로 보여 줄 때 가장 자연스럽게 이해되는지에 집중한다.

## 이 시리즈의 편집 원칙

Performance Lab에서는 결론을 먼저 선언하기보다, 구현이 어디서부터 단단해졌는지를 보여 주는 편이 더 중요하다. 그래서 최종 글은 문제를 좁히는 첫 장면, 설계가 갈라지는 중간 장면, 검증이 닫히는 마지막 장면의 세 구간으로 나눈다. 각 구간은 코드와 CLI가 함께 등장해야 하고, 다음 phase로 넘어가는 질문이 문단 끝에 남아 있어야 한다.

## 최종 글의 흐름

1. 도입에서 `make clean && make test`와 현재 재작성 범위를 먼저 밝히고, 독자가 이 글이 어떤 evidence layer 위에 서 있는지 알게 한다.
2. 본문은 Phase 1 cache simulator로 cost model을 먼저 만든다 -> Phase 2 transpose를 matrix 연산이 아니라 cache line 재배치로 본다 -> Phase 3 검증을 기능 테스트와 cost signal 두 축으로 닫는다 순서로 간다. 순서를 바꾸지 않는 이유는 이 흐름이 README와 테스트가 실제로 요구하는 구현 순서에 가장 가깝기 때문이다.
3. 마지막에는 CLI excerpt와 남은 질문을 붙여, 이 프로젝트가 어디까지 닫혔고 어디가 다음 학습 포인트인지 분명하게 남긴다.

## 1. Phase 1 - cache simulator로 cost model을 먼저 만든다

이 구간의 중심 장면은 transpose 최적화를 설명하려면 먼저 miss/hit가 어떤 식으로 계산되는지 추적할 도구가 필요하다.

본문에서는 먼저 시뮬레이터 없이 transpose만 고치면 '왜 빨라졌는지'를 숫자로 설명하지 못할 거라고 봤다. 그 다음 문단에서는 `cache_sim_init`, `cache_access`, `perflab_run_trace_file`을 먼저 세워 trace 기반 cost model을 고정했다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `cache_sim_init`, `cache_access`
- 붙일 CLI: `make clean && make test`
- 강조할 검증 신호: trace runner와 simulator helper가 성능 설명의 바닥을 깔아 준다.
- 장면이 끝날 때 남길 문장: transpose 전략을 cache line 단위 사고로 옮긴다.

## 2. Phase 2 - transpose를 matrix 연산이 아니라 cache line 재배치로 본다

이 구간의 중심 장면은 `transpose_32`, `transpose_64`, `transpose_generic`을 나눠 둔 이유가 바로 workload별 locality 차이를 드러내기 위해서다.

본문에서는 먼저 한 가지 루프만 미세 조정하는 것보다 행렬 크기별 패턴 차이를 먼저 드러내는 편이 설명력이 높다고 판단했다. 그 다음 문단에서는 naive 경로와 optimized 경로를 같이 두고, load/store helper를 통해 접근 패턴을 눈에 보이는 단위로 만들었다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `transpose_32`, `perflab_transpose_naive`
- 붙일 CLI: `make clean && make test`
- 강조할 검증 신호: 접근 helper와 전략 함수가 최적화 이유를 코드 수준에서 추적하게 해 준다.
- 장면이 끝날 때 남길 문장: trace/test 결과로 cost model과 구현을 다시 연결한다.

## 3. Phase 3 - 검증을 기능 테스트와 cost signal 두 축으로 닫는다

이 구간의 중심 장면은 performance lab은 정답 여부와 cost improvement를 같이 닫아야 한다.

본문에서는 먼저 unit test만 통과해도 충분하지 않고, trace/run 결과가 README의 설명과 맞아야 프로젝트가 끝난다고 봤다. 그 다음 문단에서는 `make test` 경로와 `problem/`의 status/compile entrypoint를 같이 두어 기능과 지표를 한 흐름으로 묶었다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `../problem/data/traces/study.trace`, `../problem/data/traces/study.trace`
- 붙일 CLI: `make clean && make test`
- 강조할 검증 신호: 테스트 바이너리와 trace runner가 마지막 확인 루프를 맡는다.
- 장면이 끝날 때 남길 문장: simulator, transpose 전략, 검증 지표를 한 축으로 정리한다.

## Fixed CLI Anchor

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/perflab/c && make clean && make test)
```

이 명령은 최종 글 마지막에서 README 계약이 여전히 살아 있다는 사실을 다시 확인하는 closing shot로 사용한다.
