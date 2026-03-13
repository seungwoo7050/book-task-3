# Synchronization Contention Lab Structure Outline

이 문서는 최종 blog를 어떤 곡선으로 읽히게 만들지 미리 고정하는 편집 설계 메모다. 근거는 모두 `01-evidence-ledger.md`와 실제 소스에서 왔고, 여기서는 그 근거를 어떤 순서로 보여 줄 때 가장 자연스럽게 이해되는지에 집중한다.

## 이 시리즈의 편집 원칙

Synchronization Contention Lab에서는 결론을 먼저 선언하기보다, 구현이 어디서부터 단단해졌는지를 보여 주는 편이 더 중요하다. 그래서 최종 글은 문제를 좁히는 첫 장면, 설계가 갈라지는 중간 장면, 검증이 닫히는 마지막 장면의 세 구간으로 나눈다. 각 구간은 코드와 CLI가 함께 등장해야 하고, 다음 phase로 넘어가는 질문이 문단 끝에 남아 있어야 한다.

## 최종 글의 흐름

1. 도입에서 `make test && make run-demo`와 현재 재작성 범위를 먼저 밝히고, 독자가 이 글이 어떤 evidence layer 위에 서 있는지 알게 한다.
2. 본문은 Phase 1 shared-state 시나리오를 먼저 만든다 -> Phase 2 primitive 선택을 timing이 아니라 invariant 기준으로 설명한다 -> Phase 3 self-owned shell test와 demo binary로 검증을 닫는다 순서로 간다. 순서를 바꾸지 않는 이유는 이 흐름이 README와 테스트가 실제로 요구하는 구현 순서에 가장 가깝기 때문이다.
3. 마지막에는 CLI excerpt와 남은 질문을 붙여, 이 프로젝트가 어디까지 닫혔고 어디가 다음 학습 포인트인지 분명하게 남긴다.

## 1. Phase 1 - shared-state 시나리오를 먼저 만든다

이 구간의 중심 장면은 동기화 실험은 primitive보다 먼저 어떤 shared state를 보호하려는지 보여 줘야 한다.

본문에서는 먼저 mutex/semaphore/condvar를 바로 비교하는 것보다 counter/gate/buffer 시나리오를 먼저 세우는 편이 각 primitive의 역할을 설명하기 쉽다고 판단했다. 그 다음 문단에서는 `run_counter_scenario`, `run_gate_scenario`, `run_buffer_scenario`로 shared-state 실험면을 먼저 만들었다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `run_counter_scenario`, `run_gate_scenario`
- 붙일 CLI: `make test && make run-demo`
- 강조할 검증 신호: 시나리오 분리가 있어야 primitive 차이를 기능적으로 비교할 수 있다.
- 장면이 끝날 때 남길 문장: primitive 선택과 correctness reasoning으로 넘어간다.

## 2. Phase 2 - primitive 선택을 timing이 아니라 invariant 기준으로 설명한다

이 구간의 중심 장면은 이 lab의 핵심은 누가 더 빠른가보다 어떤 primitive가 어떤 조건을 안전하게 표현하는가에 있다.

본문에서는 먼저 동기화 비교가 벤치마크 놀이로 흐르지 않게 correctness-before-timing 원칙을 코드와 docs 모두에 남겨야 한다고 봤다. 그 다음 문단에서는 mutex, semaphore, condvar를 시나리오별로 배치하고, 출력 메트릭은 correctness를 통과한 뒤에만 의미가 있도록 정리했다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `print_metrics`, `# Correctness Before Timing`
- 붙일 CLI: `make test && make run-demo`
- 강조할 검증 신호: docs concept와 시나리오 함수가 같은 전환점을 공유한다.
- 장면이 끝날 때 남길 문장: shell test와 demo scenario로 전 과정을 닫는다.

## 3. Phase 3 - self-owned shell test와 demo binary로 검증을 닫는다

이 구간의 중심 장면은 동기화 실험은 재현 가능한 시나리오 출력이 있어야 reasoning이 추상으로 남지 않는다.

본문에서는 먼저 shell harness와 demo binary를 같이 남기면 primitive별 차이를 다시 확인하기 쉬울 것이라고 판단했다. 그 다음 문단에서는 `test_cases.sh`와 `problem/make run-demo`를 통해 counter/gate/buffer 결과를 반복 실행 가능하게 만들었다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `main`, `extract`
- 붙일 CLI: `make test && make run-demo`
- 강조할 검증 신호: shell test와 demo 출력이 마지막 검증 신호를 남긴다.
- 장면이 끝날 때 남길 문장: scenario design -> invariant choice -> demo verification 순서로 닫는다.

## Fixed CLI Anchor

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Operating-Systems-Internals/synchronization-contention-lab/problem && make test && make run-demo)
```

이 명령은 최종 글 마지막에서 README 계약이 여전히 살아 있다는 사실을 다시 확인하는 closing shot로 사용한다.
