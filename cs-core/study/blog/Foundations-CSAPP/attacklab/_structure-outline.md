# Attack Lab Structure Outline

이 문서는 최종 blog를 어떤 곡선으로 읽히게 만들지 미리 고정하는 편집 설계 메모다. 근거는 모두 `01-evidence-ledger.md`와 실제 소스에서 왔고, 여기서는 그 근거를 어떤 순서로 보여 줄 때 가장 자연스럽게 이해되는지에 집중한다.

## 이 시리즈의 편집 원칙

Attack Lab에서는 결론을 먼저 선언하기보다, 구현이 어디서부터 단단해졌는지를 보여 주는 편이 더 중요하다. 그래서 최종 글은 문제를 좁히는 첫 장면, 설계가 갈라지는 중간 장면, 검증이 닫히는 마지막 장면의 세 구간으로 나눈다. 각 구간은 코드와 CLI가 함께 등장해야 하고, 다음 phase로 넘어가는 질문이 문단 끝에 남아 있어야 한다.

## 최종 글의 흐름

1. 도입에서 `make clean && make test`와 현재 재작성 범위를 먼저 밝히고, 독자가 이 글이 어떤 evidence layer 위에 서 있는지 알게 한다.
2. 본문은 Phase 1 payload를 읽는 표면을 먼저 고정한다 -> Phase 2 phase validator를 공격 기법별 contract로 바꾼다 -> Phase 3 publication boundary를 지키는 self-owned 검증 루프를 만든다 순서로 간다. 순서를 바꾸지 않는 이유는 이 흐름이 README와 테스트가 실제로 요구하는 구현 순서에 가장 가깝기 때문이다.
3. 마지막에는 CLI excerpt와 남은 질문을 붙여, 이 프로젝트가 어디까지 닫혔고 어디가 다음 학습 포인트인지 분명하게 남긴다.

## 1. Phase 1 - payload를 읽는 표면을 먼저 고정한다

이 구간의 중심 장면은 attacklab은 phase 정답보다 payload 바이트열을 어떤 형식으로 해석하는지가 먼저다.

본문에서는 먼저 hex parsing이 흔들리면 뒤 phase의 injection/ROP reasoning도 전부 불안정해질 거라고 봤다. 그 다음 문단에서는 `hex_value`, `parse_hex_string`, `load_hex_file`을 먼저 세워 입력 표면을 deterministic하게 만들었다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `hex_value`, `parse_hex_string`
- 붙일 CLI: `make clean && make test`
- 강조할 검증 신호: payload 로더가 따로 남아 있어 phase별 logic과 입력 해석을 혼동하지 않게 됐다.
- 장면이 끝날 때 남길 문장: phase 1~5 validator로 넘어가면서 공격 기법 차이를 코드로 분리한다.

## 2. Phase 2 - phase validator를 공격 기법별 contract로 바꾼다

이 구간의 중심 장면은 `attacklab_phase_1`~`attacklab_phase_5`는 한 덩어리 exploit dump가 아니라 서로 다른 검증 contract다.

본문에서는 먼저 코드 주입과 ROP를 같은 방식으로 설명하면 차이가 흐려질 것이라서 phase별로 기대하는 바이트/주소 패턴을 분리했다. 그 다음 문단에서는 validator 함수와 `matches_u64_le`, `read_u64_le` 같은 helper를 엮어 phase별 reasoning을 코드에서 바로 읽히게 했다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `read_u64_le`, `matches_u64_le`
- 붙일 CLI: `make clean && make test`
- 강조할 검증 신호: phase validator 분리가 되어 있어 injection과 ROP의 차이를 글에서도 단계적으로 전개할 수 있다.
- 장면이 끝날 때 남길 문장: sample payload와 unit test로 boundary를 닫는다.

## 3. Phase 3 - publication boundary를 지키는 self-owned 검증 루프를 만든다

이 구간의 중심 장면은 raw exploit answer를 늘리는 대신 sample payload와 unit test로 '왜 통과하는지'를 설명해야 한다.

본문에서는 먼저 phase data file과 unit test만 있으면 공개 가능한 범위에서 reasoning을 재현할 수 있다고 판단했다. 그 다음 문단에서는 `make test` 경로에 sample run을 넣고, README에서는 official boundary와 public test를 분리해 놓았다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `attacklab_validate_phase`, `C mini-attacklab tests passed`
- 붙일 CLI: `make clean && make test`
- 강조할 검증 신호: 샘플 phase 데이터와 테스트 바이너리가 마지막 단계를 구체적으로 닫아 준다.
- 장면이 끝날 때 남길 문장: payload dump 대신 입력 표면, validator, boundary 설계의 순서로 마무리한다.

## Fixed CLI Anchor

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/attacklab/c && make clean && make test)
```

이 명령은 최종 글 마지막에서 README 계약이 여전히 살아 있다는 사실을 다시 확인하는 closing shot로 사용한다.
