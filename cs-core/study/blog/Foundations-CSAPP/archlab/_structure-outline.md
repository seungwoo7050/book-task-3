# Architecture Lab Structure Outline

이 문서는 최종 blog를 어떤 곡선으로 읽히게 만들지 미리 고정하는 편집 설계 메모다. 근거는 모두 `01-evidence-ledger.md`와 실제 소스에서 왔고, 여기서는 그 근거를 어떤 순서로 보여 줄 때 가장 자연스럽게 이해되는지에 집중한다.

## 이 시리즈의 편집 원칙

Architecture Lab에서는 결론을 먼저 선언하기보다, 구현이 어디서부터 단단해졌는지를 보여 주는 편이 더 중요하다. 그래서 최종 글은 문제를 좁히는 첫 장면, 설계가 갈라지는 중간 장면, 검증이 닫히는 마지막 장면의 세 구간으로 나눈다. 각 구간은 코드와 CLI가 함께 등장해야 하고, 다음 phase로 넘어가는 질문이 문단 끝에 남아 있어야 한다.

## 최종 글의 흐름

1. 도입에서 `make clean && make test`와 현재 재작성 범위를 먼저 밝히고, 독자가 이 글이 어떤 evidence layer 위에 서 있는지 알게 한다.
2. 본문은 Phase 1 Y86 문제를 companion 코드와 part split으로 분해한다 -> Phase 2 `iaddq`를 단일 명령 추가가 아니라 control-signal 변화로 본다 -> Phase 3 `ncopy`를 '더 빠르게'가 아니라 cycle budget으로 해석한다 순서로 간다. 순서를 바꾸지 않는 이유는 이 흐름이 README와 테스트가 실제로 요구하는 구현 순서에 가장 가깝기 때문이다.
3. 마지막에는 CLI excerpt와 남은 질문을 붙여, 이 프로젝트가 어디까지 닫혔고 어디가 다음 학습 포인트인지 분명하게 남긴다.

## 1. Phase 1 - Y86 문제를 companion 코드와 part split으로 분해한다

이 구간의 중심 장면은 `sum`, `rsum`, `copy`, `ncopy` 같은 Y86 작업과 companion C 테스트가 같은 문제를 다른 표면으로 설명하게 만든다.

본문에서는 먼저 원문 lab의 파트 구성이 그대로 남아 있어야 나중에 성능/제어 로직 작업으로 넘어가도 길을 잃지 않을 거라고 봤다. 그 다음 문단에서는 Y86 소스는 `y86/src/`에, 재현 가능한 샘플과 테스트는 `c/src/mini_archlab.c`로 분리해 공개 경계를 만들었다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `ncopy`, `arch_copy_block`
- 붙일 CLI: `make clean && make test`
- 강조할 검증 신호: 문제 분해가 먼저 되어 있어 이후 제어/성능 논의를 붙일 자리가 생긴다.
- 장면이 끝날 때 남길 문장: `iaddq`가 실제로 제어 신호를 얼마나 흔드는지로 초점을 옮긴다.

## 2. Phase 2 - `iaddq`를 단일 명령 추가가 아니라 control-signal 변화로 본다

이 구간의 중심 장면은 `seq_iaddq`와 overflow helper를 보면 결국 핵심은 새 opcode를 넣는 일이 아니라 decode/execute 경계에서 어떤 신호를 더 건드려야 하는지다.

본문에서는 먼저 Y86 instruction을 하나 추가해도 데이터 경로와 condition code 규칙을 건드리는 지점이 더 클 것이라고 예상했다. 그 다음 문단에서는 `seq_iaddq`, `add_overflow`, docs의 control-signal 메모를 중심으로 구현/설명을 묶었다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `add_overflow`, `arch_seq_iaddq`
- 붙일 CLI: `make clean && make test`
- 강조할 검증 신호: 제어 로직을 companion 함수로 둔 덕분에 결과를 C 테스트로 다시 확인할 수 있다.
- 장면이 끝날 때 남길 문장: 마지막 국면에서는 `ncopy`를 성능 지표와 연결한다.

## 3. Phase 3 - `ncopy`를 '더 빠르게'가 아니라 cycle budget으로 해석한다

이 구간의 중심 장면은 `baseline_cycles`, `optimized_cycles`, `arch_ncopy_optimized`를 같이 보면 최적화는 감이 아니라 cost model을 맞추는 작업이다.

본문에서는 먼저 copy correctness만 통과하면 끝이 아니라, pipeline cost를 숫자로 보지 않으면 왜 unroll/branch 정리가 필요한지 설명할 수 없다고 봤다. 그 다음 문단에서는 baseline/optimized 두 경로를 같이 두고 테스트 바이너리에서 기능과 비용을 동시에 비교하게 만들었다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `baseline_cycles`, `optimized_cycles`
- 붙일 CLI: `make clean && make test`
- 강조할 검증 신호: 샘플 실행과 테스트 바이너리가 남아 있어 마지막 국면을 CLI로 닫을 수 있다.
- 장면이 끝날 때 남길 문장: Y86 파트 분리, control signal, cost model을 한 줄로 연결한다.

## Fixed CLI Anchor

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/archlab/c && make clean && make test)
```

이 명령은 최종 글 마지막에서 README 계약이 여전히 살아 있다는 사실을 다시 확인하는 closing shot로 사용한다.
