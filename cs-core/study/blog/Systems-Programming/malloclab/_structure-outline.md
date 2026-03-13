# Malloc Lab Structure Outline

이 문서는 최종 blog를 어떤 곡선으로 읽히게 만들지 미리 고정하는 편집 설계 메모다. 근거는 모두 `01-evidence-ledger.md`와 실제 소스에서 왔고, 여기서는 그 근거를 어떤 순서로 보여 줄 때 가장 자연스럽게 이해되는지에 집중한다.

## 이 시리즈의 편집 원칙

Malloc Lab에서는 결론을 먼저 선언하기보다, 구현이 어디서부터 단단해졌는지를 보여 주는 편이 더 중요하다. 그래서 최종 글은 문제를 좁히는 첫 장면, 설계가 갈라지는 중간 장면, 검증이 닫히는 마지막 장면의 세 구간으로 나눈다. 각 구간은 코드와 CLI가 함께 등장해야 하고, 다음 phase로 넘어가는 질문이 문단 끝에 남아 있어야 한다.

## 최종 글의 흐름

1. 도입에서 `make clean && make test`와 현재 재작성 범위를 먼저 밝히고, 독자가 이 글이 어떤 evidence layer 위에 서 있는지 알게 한다.
2. 본문은 Phase 1 블록 레이아웃과 word helper를 먼저 고정한다 -> Phase 2 explicit free list 조작을 핵심 설계 단위로 삼는다 -> Phase 3 `realloc`과 trace 검증으로 allocator를 닫는다 순서로 간다. 순서를 바꾸지 않는 이유는 이 흐름이 README와 테스트가 실제로 요구하는 구현 순서에 가장 가깝기 때문이다.
3. 마지막에는 CLI excerpt와 남은 질문을 붙여, 이 프로젝트가 어디까지 닫혔고 어디가 다음 학습 포인트인지 분명하게 남긴다.

## 1. Phase 1 - 블록 레이아웃과 word helper를 먼저 고정한다

이 구간의 중심 장면은 allocator는 정책보다 먼저 block header/footer와 alignment contract가 흔들리지 않아야 한다.

본문에서는 먼저 free list를 만지기 전에 `pack`, `block_size`, `is_allocated`, alignment helper를 고정해야 뒤 단계가 덜 흔들릴 거라고 봤다. 그 다음 문단에서는 word load/store helper와 size/allocation 해석 함수를 먼저 정리해 힙을 읽는 어휘를 만들었다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `align_size`, `pack`
- 붙일 CLI: `make clean && make test`
- 강조할 검증 신호: invariant helper가 있어야 이후 조작이 '왜 안전한가'를 설명할 수 있다.
- 장면이 끝날 때 남길 문장: explicit free list와 placement 정책으로 이동한다.

## 2. Phase 2 - explicit free list 조작을 핵심 설계 단위로 삼는다

이 구간의 중심 장면은 `add_to_free_list`, `remove_from_free_list`, `place_block`이 allocator의 실제 설계 전환점이다.

본문에서는 먼저 coalescing과 split을 따로 생각하면 버그가 많아질 것 같아 free list 조작을 중심축으로 두었다. 그 다음 문단에서는 free list head 갱신, block split, 재삽입 규칙을 helper 함수로 분리하고 `mm_malloc`/`mm_free`와 연결했다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `add_to_free_list`, `remove_from_free_list`
- 붙일 CLI: `make clean && make test`
- 강조할 검증 신호: list 조작 helper가 설계 논의를 함수 수준으로 끌어내린다.
- 장면이 끝날 때 남길 문장: `realloc`과 trace-driven 검증으로 마지막 경계를 닫는다.

## 3. Phase 3 - `realloc`과 trace 검증으로 allocator를 닫는다

이 구간의 중심 장면은 마지막에 남는 문제는 단순 할당/해제가 아니라 기존 payload 보존과 coalescing 순서다.

본문에서는 먼저 `realloc`은 결국 copy + free가 아니라 surrounding free block과의 관계까지 같이 봐야 할 것이라고 판단했다. 그 다음 문단에서는 `docs/concepts/realloc-and-coalescing.md`와 `mdriver` trace entrypoint를 연결해 마지막 검증 국면을 닫았다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `mm_init`, `mm_free`
- 붙일 CLI: `make clean && make test`
- 강조할 검증 신호: trace runner가 마지막에 성능/정확성 신호를 함께 보여 준다.
- 장면이 끝날 때 남길 문장: invariants -> list ops -> trace verification 순서를 유지한다.

## Fixed CLI Anchor

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/malloclab/c && make clean && make test)
```

이 명령은 최종 글 마지막에서 README 계약이 여전히 살아 있다는 사실을 다시 확인하는 closing shot로 사용한다.
