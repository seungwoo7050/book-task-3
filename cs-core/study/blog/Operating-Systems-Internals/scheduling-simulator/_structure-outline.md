# Scheduling Simulator Structure Outline

이 문서는 최종 blog를 어떤 곡선으로 읽히게 만들지 미리 고정하는 편집 설계 메모다. 근거는 모두 `01-evidence-ledger.md`와 실제 소스에서 왔고, 여기서는 그 근거를 어떤 순서로 보여 줄 때 가장 자연스럽게 이해되는지에 집중한다.

## 이 시리즈의 편집 원칙

Scheduling Simulator에서는 결론을 먼저 선언하기보다, 구현이 어디서부터 단단해졌는지를 보여 주는 편이 더 중요하다. 그래서 최종 글은 문제를 좁히는 첫 장면, 설계가 갈라지는 중간 장면, 검증이 닫히는 마지막 장면의 세 구간으로 나눈다. 각 구간은 코드와 CLI가 함께 등장해야 하고, 다음 phase로 넘어가는 질문이 문단 끝에 남아 있어야 한다.

## 최종 글의 흐름

1. 도입에서 `make test && make run-demo`와 현재 재작성 범위를 먼저 밝히고, 독자가 이 글이 어떤 evidence layer 위에 서 있는지 알게 한다.
2. 본문은 Phase 1 fixture loader와 공통 simulation loop를 먼저 고정한다 -> Phase 2 policy-specific helper로 fairness와 latency trade-off를 드러낸다 -> Phase 3 replay 출력과 summary metric으로 실험을 닫는다 순서로 간다. 순서를 바꾸지 않는 이유는 이 흐름이 README와 테스트가 실제로 요구하는 구현 순서에 가장 가깝기 때문이다.
3. 마지막에는 CLI excerpt와 남은 질문을 붙여, 이 프로젝트가 어디까지 닫혔고 어디가 다음 학습 포인트인지 분명하게 남긴다.

## 1. Phase 1 - fixture loader와 공통 simulation loop를 먼저 고정한다

이 구간의 중심 장면은 policy 비교는 scheduler 함수보다 먼저 workload를 어떻게 읽고 timeline으로 돌릴지를 정해야 한다.

본문에서는 먼저 FCFS/SJF/RR/MLFQ를 바로 구현하기보다 arrival/ready queue/metric 수집을 공통 루프로 빼는 편이 나중에 비교가 쉬울 것이라고 봤다. 그 다음 문단에서는 `load_fixture`, `simulate_policy`, arrival enqueue helper를 중심으로 공통 골격을 먼저 세웠다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `load_fixture`, `simulate_policy`
- 붙일 CLI: `make test && make run-demo`
- 강조할 검증 신호: 공통 루프가 먼저 있기 때문에 각 policy 차이를 좁은 범위에서 설명할 수 있다.
- 장면이 끝날 때 남길 문장: policy별 분기와 metric 차이를 해석한다.

## 2. Phase 2 - policy-specific helper로 fairness와 latency trade-off를 드러낸다

이 구간의 중심 장면은 `_simulate_fcfs`, `_simulate_sjf`, `_simulate_rr`, `_simulate_mlfq`와 queue helper가 실제 비교 지점을 만든다.

본문에서는 먼저 policy 차이는 결과 표 하나보다 queue 조작 방식과 preemption 규칙이 어떻게 다른지에서 더 선명하게 드러날 것이라고 판단했다. 그 다음 문단에서는 policy별 시뮬레이터를 분리하고, boost/quantum/level pick helper를 두어 MLFQ의 고유 규칙을 명확히 했다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `_simulate_fcfs`, `_simulate_sjf`
- 붙일 CLI: `make test && make run-demo`
- 강조할 검증 신호: policy helper가 분리돼 있어 metric 차이를 코드 수준에서 역추적할 수 있다.
- 장면이 끝날 때 남길 문장: replay CLI와 metrics 표로 결과를 닫는다.

## 3. Phase 3 - replay 출력과 summary metric으로 실험을 닫는다

이 구간의 중심 장면은 scheduler lab은 내부 자료구조보다 replay와 평균 지표가 외부에서 읽히는지가 중요하다.

본문에서는 먼저 CLI가 없다면 policy 차이를 설명하는 글이 결국 표 하나로 축약될 것 같아 replay surface를 끝까지 남겼다. 그 다음 문단에서는 `--replay` CLI와 `make run-demo`를 통해 timeline과 waiting/response/turnaround 표를 동시에 출력하게 했다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `main`, `test_sjf_reduces_waiting_time_on_convoy_fixture`
- 붙일 CLI: `make test && make run-demo`
- 강조할 검증 신호: 현재 demo 출력이 네 policy 차이를 한 번에 보여 준다.
- 장면이 끝날 때 남길 문장: common loop -> policy helper -> replay metric 순서로 닫는다.

## Fixed CLI Anchor

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Operating-Systems-Internals/scheduling-simulator/problem && make test && make run-demo)
```

이 명령은 최종 글 마지막에서 README 계약이 여전히 살아 있다는 사실을 다시 확인하는 closing shot로 사용한다.
