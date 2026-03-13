# Malloc Lab Evidence Ledger

이 문서는 최종 글보다 한 단계 앞에 있는 근거 문서다. 기존 `blog/` 초안은 입력에서 제외했고, 지금 남아 있는 README, problem 설명, 구현 파일, 테스트, git history, 재실행한 CLI만으로 chronology를 다시 세웠다.

## 근거 묶음

`malloclab`은 힙 블록 레이아웃, 정렬 규칙, explicit free list, coalescing, `realloc`을 한 번에 다루는 allocator 프로젝트다. 구현의 중심은 `c`, `cpp`에 퍼져 있고, 글에서 반복해서 참조할 핵심 파일은 `c/src/mm.c`, `cpp/src/mm.cpp`다. 검증 표면은 `(none)`와 `make clean && make test`에 걸쳐 있으며, 이번에 다시 붙잡은 개념 축은 `allocator invariants`, `realloc and coalescing`이다.

## Git History Anchor

- `2026-03-09	b1cbad9	docs(notion): cs-core, network-atda`
- `2026-03-10	ced9d08	docs: enhance cs-core`
- `2026-03-11	bbb6673	Track 1에 대한 전반적인 개선 완료`
- `2026-03-13	abeead6	docs: TRACK 1 에대한 blog/ 작업 1차 완료`

## 1. Phase 1 - 블록 레이아웃과 word helper를 먼저 고정한다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다. 이 시점의 목표는 allocator는 정책보다 먼저 block header/footer와 alignment contract가 흔들리지 않아야 한다.

그때 세운 가설은 free list를 만지기 전에 `pack`, `block_size`, `is_allocated`, alignment helper를 고정해야 뒤 단계가 덜 흔들릴 거라고 봤다. 실제 조치는 word load/store helper와 size/allocation 해석 함수를 먼저 정리해 힙을 읽는 어휘를 만들었다.

- 정리해 둔 근거:
- 변경 단위: `c/src/mm.c`
- CLI: `make clean && make test`
- 검증 신호: invariant helper가 있어야 이후 조작이 '왜 안전한가'를 설명할 수 있다.
- 새로 배운 것: 메모리 할당기는 자료구조보다 먼저 raw word를 어떻게 해석할지에 대한 문법을 세워야 했다.

### 코드 앵커 — `align_size` (`c/src/mm.c:17`)

```c
static size_t align_size(size_t size)
{
    return (size + (ALIGNMENT - 1)) & ~(size_t)(ALIGNMENT - 1);
}
```

이 조각은 invariant helper가 있어야 이후 조작이 '왜 안전한가'를 설명할 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `align_size`를 읽고 나면 다음 장면이 왜 explicit free list와 placement 정책으로 이동한다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `pack` (`c/src/mm.c:22`)

```c
static size_t pack(size_t size, int allocated)
{
    return size | (size_t)allocated;
}
```

이 조각은 invariant helper가 있어야 이후 조작이 '왜 안전한가'를 설명할 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `pack`를 읽고 나면 다음 장면이 왜 explicit free list와 placement 정책으로 이동한다로 이어지는지도 한 번에 보인다.

다음 단계에서는 explicit free list와 placement 정책으로 이동한다.

## 2. Phase 2 - explicit free list 조작을 핵심 설계 단위로 삼는다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다. 이 시점의 목표는 `add_to_free_list`, `remove_from_free_list`, `place_block`이 allocator의 실제 설계 전환점이다.

그때 세운 가설은 coalescing과 split을 따로 생각하면 버그가 많아질 것 같아 free list 조작을 중심축으로 두었다. 실제 조치는 free list head 갱신, block split, 재삽입 규칙을 helper 함수로 분리하고 `mm_malloc`/`mm_free`와 연결했다.

- 정리해 둔 근거:
- 변경 단위: `c/src/mm.c`
- CLI: `make clean && make test`
- 검증 신호: list 조작 helper가 설계 논의를 함수 수준으로 끌어내린다.
- 새로 배운 것: allocator의 핵심은 '어디에서 할당할까'보다 'free list invariant를 언제 깨고 언제 복원할까'였다.

### 코드 앵커 — `add_to_free_list` (`c/src/mm.c:77`)

```c
static void add_to_free_list(void *block)
{
    *next_free_slot(block) = free_list_head;
    *prev_free_slot(block) = NULL;
```

이 조각은 list 조작 helper가 설계 논의를 함수 수준으로 끌어내린다는 설명이 실제로 어디서 나오는지 보여 준다. `add_to_free_list`를 읽고 나면 다음 장면이 왜 `realloc`과 trace-driven 검증으로 마지막 경계를 닫는다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `remove_from_free_list` (`c/src/mm.c:88`)

```c
static void remove_from_free_list(void *block)
{
    void *prev = *prev_free_slot(block);
    void *next = *next_free_slot(block);
```

이 조각은 list 조작 helper가 설계 논의를 함수 수준으로 끌어내린다는 설명이 실제로 어디서 나오는지 보여 준다. `remove_from_free_list`를 읽고 나면 다음 장면이 왜 `realloc`과 trace-driven 검증으로 마지막 경계를 닫는다로 이어지는지도 한 번에 보인다.

다음 단계에서는 `realloc`과 trace-driven 검증으로 마지막 경계를 닫는다.

## 3. Phase 3 - `realloc`과 trace 검증으로 allocator를 닫는다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다. 이 시점의 목표는 마지막에 남는 문제는 단순 할당/해제가 아니라 기존 payload 보존과 coalescing 순서다.

그때 세운 가설은 `realloc`은 결국 copy + free가 아니라 surrounding free block과의 관계까지 같이 봐야 할 것이라고 판단했다. 실제 조치는 `docs/concepts/realloc-and-coalescing.md`와 `mdriver` trace entrypoint를 연결해 마지막 검증 국면을 닫았다.

- 정리해 둔 근거:
- 변경 단위: `c/src/mm.c`
- CLI: `make clean && make test`
- 검증 신호: trace runner가 마지막에 성능/정확성 신호를 함께 보여 준다.
- 새로 배운 것: `realloc`을 다루고 나서야 free list 설계가 실제 workload에서 버티는지 설명할 수 있게 됐다.

### 코드 앵커 — `mm_init` (`c/src/mm.c:194`)

```c
int mm_init(void)
{
    heap_start = (char *)mem_sbrk(4 * WORD_SIZE);
    if (heap_start == (void *)-1) {
        return -1;
    }
```

이 조각은 trace runner가 마지막에 성능/정확성 신호를 함께 보여 준다는 설명이 실제로 어디서 나오는지 보여 준다. `mm_init`를 읽고 나면 다음 장면이 왜 invariants -> list ops -> trace verification 순서를 유지한다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `mm_free` (`c/src/mm.c:239`)

```c
void mm_free(void *ptr)
{
    size_t size;

    if (ptr == NULL) {
        return;
    }
```

이 조각은 trace runner가 마지막에 성능/정확성 신호를 함께 보여 준다는 설명이 실제로 어디서 나오는지 보여 준다. `mm_free`를 읽고 나면 다음 장면이 왜 invariants -> list ops -> trace verification 순서를 유지한다로 이어지는지도 한 번에 보인다.

다음 단계에서는 invariants -> list ops -> trace verification 순서를 유지한다.

## Latest CLI Excerpt

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
