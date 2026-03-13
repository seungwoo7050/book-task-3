# Malloc Lab 재구성 개발 로그

`malloclab`은 힙 블록 레이아웃, 정렬 규칙, explicit free list, coalescing, `realloc`을 한 번에 다루는 allocator 프로젝트다.

2026-03-13에 기존 초안을 `_legacy`로 격리한 뒤, `README`, `problem/`, 실제 구현 파일, `docs/`, 테스트, 현재 다시 실행한 CLI만으로 이 글을 다시 썼다. 그래서 아래 서사는 나중에 답을 알고 난 뒤 매끈하게 정리한 회고가 아니라, 남아 있는 증거를 따라 다시 세운 개발 흐름에 가깝다.

## 이 프로젝트를 다시 읽는 순서

힙 메타데이터, free list, `realloc`/coalescing이 한 번에 얽히는 allocator를 invariants 중심으로 복원한다. 이 질문이 너무 빨리 추상적으로 흘러가지 않도록, 글은 세 개의 phase로 나눠 진행한다.

- Phase 1: 블록 레이아웃과 word helper를 먼저 고정한다 — `c/src/mm.c`
- Phase 2: explicit free list 조작을 핵심 설계 단위로 삼는다 — `c/src/mm.c`
- Phase 3: `realloc`과 trace 검증으로 allocator를 닫는다 — `c/src/mm.c`

## Phase 1. 블록 레이아웃과 word helper를 먼저 고정한다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다.

이 시점의 목표는 allocator는 정책보다 먼저 block header/footer와 alignment contract가 흔들리지 않아야 한다.

처음에는 free list를 만지기 전에 `pack`, `block_size`, `is_allocated`, alignment helper를 고정해야 뒤 단계가 덜 흔들릴 거라고 봤다. 그런데 실제로 글의 중심이 된 조치는 word load/store helper와 size/allocation 해석 함수를 먼저 정리해 힙을 읽는 어휘를 만들었다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/src/mm.c`
- CLI: `make clean && make test`
- 검증 신호: invariant helper가 있어야 이후 조작이 '왜 안전한가'를 설명할 수 있다.

### 이 장면을 고정하는 코드 — `align_size` (`c/src/mm.c:17`)

이 단계에서 가장 먼저 붙잡아야 하는 코드는 아래 조각이다.

```c
static size_t align_size(size_t size)
{
    return (size + (ALIGNMENT - 1)) & ~(size_t)(ALIGNMENT - 1);
}
```

`align_size`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 메모리 할당기는 자료구조보다 먼저 raw word를 어떻게 해석할지에 대한 문법을 세워야 했다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 explicit free list와 placement 정책으로 이동한다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 메모리 할당기는 자료구조보다 먼저 raw word를 어떻게 해석할지에 대한 문법을 세워야 했다.

그래서 다음 장면에서는 explicit free list와 placement 정책으로 이동한다.

## Phase 2. explicit free list 조작을 핵심 설계 단위로 삼는다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다.

이 시점의 목표는 `add_to_free_list`, `remove_from_free_list`, `place_block`이 allocator의 실제 설계 전환점이다.

처음에는 coalescing과 split을 따로 생각하면 버그가 많아질 것 같아 free list 조작을 중심축으로 두었다. 그런데 실제로 글의 중심이 된 조치는 free list head 갱신, block split, 재삽입 규칙을 helper 함수로 분리하고 `mm_malloc`/`mm_free`와 연결했다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/src/mm.c`
- CLI: `make clean && make test`
- 검증 신호: list 조작 helper가 설계 논의를 함수 수준으로 끌어내린다.

### 이 장면을 고정하는 코드 — `add_to_free_list` (`c/src/mm.c:77`)

판단이 뒤집히는 지점은 결국 이 구현 세부에서 드러난다.

```c
static void add_to_free_list(void *block)
{
    *next_free_slot(block) = free_list_head;
    *prev_free_slot(block) = NULL;
```

`add_to_free_list`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 allocator의 핵심은 '어디에서 할당할까'보다 'free list invariant를 언제 깨고 언제 복원할까'였다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 `realloc`과 trace-driven 검증으로 마지막 경계를 닫는다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 allocator의 핵심은 '어디에서 할당할까'보다 'free list invariant를 언제 깨고 언제 복원할까'였다.

그래서 다음 장면에서는 `realloc`과 trace-driven 검증으로 마지막 경계를 닫는다.

## Phase 3. `realloc`과 trace 검증으로 allocator를 닫는다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다.

이 시점의 목표는 마지막에 남는 문제는 단순 할당/해제가 아니라 기존 payload 보존과 coalescing 순서다.

처음에는 `realloc`은 결국 copy + free가 아니라 surrounding free block과의 관계까지 같이 봐야 할 것이라고 판단했다. 그런데 실제로 글의 중심이 된 조치는 `docs/concepts/realloc-and-coalescing.md`와 `mdriver` trace entrypoint를 연결해 마지막 검증 국면을 닫았다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/src/mm.c`
- CLI: `make clean && make test`
- 검증 신호: trace runner가 마지막에 성능/정확성 신호를 함께 보여 준다.

### 이 장면을 고정하는 코드 — `mm_init` (`c/src/mm.c:194`)

끝을 닫는 순간은 늘 테스트나 CLI 쪽 코드가 더 솔직하게 보여 준다.

```c
int mm_init(void)
{
    heap_start = (char *)mem_sbrk(4 * WORD_SIZE);
    if (heap_start == (void *)-1) {
        return -1;
    }
```

`mm_init`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 `realloc`을 다루고 나서야 free list 설계가 실제 workload에서 버티는지 설명할 수 있게 됐다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 invariants -> list ops -> trace verification 순서를 유지한다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 `realloc`을 다루고 나서야 free list 설계가 실제 workload에서 버티는지 설명할 수 있게 됐다.

그래서 다음 장면에서는 invariants -> list ops -> trace verification 순서를 유지한다.

## CLI로 다시 닫기

문장과 코드만으로는 마지막 닫힘이 약해질 수 있어서, 저장소에서 다시 실행 가능한 대표 명령을 마지막에 그대로 남긴다. 이 출력은 기능이 돌아간다는 사실뿐 아니라 README가 약속한 검증 entrypoint가 아직 살아 있다는 사실까지 함께 보여 준다.

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/malloclab/c && make clean && make test)
```

```text
./build/mdriver -t ../problem/data/traces -v
Trace basic.rep: errors=0 peak_live=104 peak_heap=4128 util=0.025 throughput=3871665 ops/s
Trace coalesce.rep: errors=0 peak_live=392 peak_heap=4128 util=0.095 throughput=4441028 ops/s
Trace mixed.rep: errors=0 peak_live=512 peak_heap=4128 util=0.124 throughput=3690988 ops/s
Trace realloc.rep: errors=0 peak_live=256 peak_heap=4128 util=0.062 throughput=3454133 ops/s
Summary: traces=4 errors=0 avg_util=0.077 throughput=3844779 ops/s
```

## 이번에 남은 질문

- 개념 축: `allocator invariants`, `realloc and coalescing`
- 대표 테스트/fixture: `(none)`
- 다음 질문: 최종 글에서는 invariants -> list ops -> trace verification 순서를 유지한다.
