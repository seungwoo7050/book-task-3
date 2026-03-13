# Performance Lab Evidence Ledger

이 문서는 최종 글보다 한 단계 앞에 있는 근거 문서다. 기존 `blog/` 초안은 입력에서 제외했고, 지금 남아 있는 README, problem 설명, 구현 파일, 테스트, git history, 재실행한 CLI만으로 chronology를 다시 세웠다.

## 근거 묶음

`perflab`은 cache simulator와 transpose 최적화를 통해 "왜 더 빠른가"를 코드와 지표로 설명하는 프로젝트다. 구현의 중심은 `c`, `cpp`에 퍼져 있고, 글에서 반복해서 참조할 핵심 파일은 `c/src/main.c`, `c/src/perflab.c`, `cpp/src/main.cpp`, `cpp/src/perflab.cpp`다. 검증 표면은 `c/tests/test_perflab.c`, `cpp/tests/test_perflab.cpp`와 `make clean && make test`에 걸쳐 있으며, 이번에 다시 붙잡은 개념 축은 `cache sim lru`, `transpose strategies`이다.

## Git History Anchor

- `2026-03-09	b1cbad9	docs(notion): cs-core, network-atda`
- `2026-03-10	ced9d08	docs: enhance cs-core`
- `2026-03-11	bbb6673	Track 1에 대한 전반적인 개선 완료`
- `2026-03-13	abeead6	docs: TRACK 1 에대한 blog/ 작업 1차 완료`

## 1. Phase 1 - cache simulator로 cost model을 먼저 만든다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다. 이 시점의 목표는 transpose 최적화를 설명하려면 먼저 miss/hit가 어떤 식으로 계산되는지 추적할 도구가 필요하다.

그때 세운 가설은 시뮬레이터 없이 transpose만 고치면 '왜 빨라졌는지'를 숫자로 설명하지 못할 거라고 봤다. 실제 조치는 `cache_sim_init`, `cache_access`, `perflab_run_trace_file`을 먼저 세워 trace 기반 cost model을 고정했다.

- 정리해 둔 근거:
- 변경 단위: `c/src/perflab.c`
- CLI: `make clean && make test`
- 검증 신호: trace runner와 simulator helper가 성능 설명의 바닥을 깔아 준다.
- 새로 배운 것: 성능 프로젝트도 결국 먼저 필요한 것은 최적화 기술이 아니라 관측 가능한 지표 표면이었다.

### 코드 앵커 — `cache_sim_init` (`c/src/perflab.c:27`)

```c
static void cache_sim_init(CacheSim *cache, int s, int E, int b)
{
    int set_index;

    cache->s = s;
    cache->E = E;
    cache->b = b;
    cache->S = 1 << s;
    cache->clock = 1;
    cache->stats.hits = 0;
    cache->stats.misses = 0;
    cache->stats.evictions = 0;
```

이 조각은 trace runner와 simulator helper가 성능 설명의 바닥을 깔아 준다는 설명이 실제로 어디서 나오는지 보여 준다. `cache_sim_init`를 읽고 나면 다음 장면이 왜 transpose 전략을 cache line 단위 사고로 옮긴다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `cache_access` (`c/src/perflab.c:55`)

```c
static void cache_access(CacheSim *cache, uint64_t address)
{
    uint64_t set_mask = (1ULL << cache->s) - 1ULL;
    uint64_t set_index = (address >> cache->b) & set_mask;
    uint64_t tag = address >> (cache->s + cache->b);
    CacheSet *set = &cache->sets[set_index];
    int line_index;
    int empty_index = -1;
    int victim_index = 0;
    uint64_t oldest_lru = UINT64_MAX;
```

이 조각은 trace runner와 simulator helper가 성능 설명의 바닥을 깔아 준다는 설명이 실제로 어디서 나오는지 보여 준다. `cache_access`를 읽고 나면 다음 장면이 왜 transpose 전략을 cache line 단위 사고로 옮긴다로 이어지는지도 한 번에 보인다.

다음 단계에서는 transpose 전략을 cache line 단위 사고로 옮긴다.

## 2. Phase 2 - transpose를 matrix 연산이 아니라 cache line 재배치로 본다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다. 이 시점의 목표는 `transpose_32`, `transpose_64`, `transpose_generic`을 나눠 둔 이유가 바로 workload별 locality 차이를 드러내기 위해서다.

그때 세운 가설은 한 가지 루프만 미세 조정하는 것보다 행렬 크기별 패턴 차이를 먼저 드러내는 편이 설명력이 높다고 판단했다. 실제 조치는 naive 경로와 optimized 경로를 같이 두고, load/store helper를 통해 접근 패턴을 눈에 보이는 단위로 만들었다.

- 정리해 둔 근거:
- 변경 단위: `c/src/perflab.c`, `cpp/src/perflab.cpp`
- CLI: `make clean && make test`
- 검증 신호: 접근 helper와 전략 함수가 최적화 이유를 코드 수준에서 추적하게 해 준다.
- 새로 배운 것: 최적화는 코드 양을 늘리는 일이 아니라 locality를 어기는 이동을 줄이는 재배치라는 점이 분명해졌다.

### 코드 앵커 — `transpose_32` (`cpp/src/perflab.cpp:145`)

```cpp
void transpose_32(const std::vector<int> &A, std::vector<int> &B, TransposeCache &cache)
{
    for (int ii = 0; ii < 32; ii += 8) {
        for (int jj = 0; jj < 32; jj += 8) {
            for (int i = ii; i < ii + 8; ++i) {
                int diag_value = 0;
                int diag_index = -1;
                for (int j = jj; j < jj + 8; ++j) {
                    const int value = load_a(32, A, i, j, cache);
                    if (ii == jj && i == j) {
                        diag_value = value;
                        diag_index = i;
```

이 조각은 접근 helper와 전략 함수가 최적화 이유를 코드 수준에서 추적하게 해 준다는 설명이 실제로 어디서 나오는지 보여 준다. `transpose_32`를 읽고 나면 다음 장면이 왜 trace/test 결과로 cost model과 구현을 다시 연결한다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `perflab_transpose_naive` (`c/src/perflab.c:181`)

```c
void perflab_transpose_naive(int M, int N, const int *A, int *B, TransposeCache *cache)
{
    int i;
    int j;
```

이 조각은 접근 helper와 전략 함수가 최적화 이유를 코드 수준에서 추적하게 해 준다는 설명이 실제로 어디서 나오는지 보여 준다. `perflab_transpose_naive`를 읽고 나면 다음 장면이 왜 trace/test 결과로 cost model과 구현을 다시 연결한다로 이어지는지도 한 번에 보인다.

다음 단계에서는 trace/test 결과로 cost model과 구현을 다시 연결한다.

## 3. Phase 3 - 검증을 기능 테스트와 cost signal 두 축으로 닫는다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다. 이 시점의 목표는 performance lab은 정답 여부와 cost improvement를 같이 닫아야 한다.

그때 세운 가설은 unit test만 통과해도 충분하지 않고, trace/run 결과가 README의 설명과 맞아야 프로젝트가 끝난다고 봤다. 실제 조치는 `make test` 경로와 `problem/`의 status/compile entrypoint를 같이 두어 기능과 지표를 한 흐름으로 묶었다.

- 정리해 둔 근거:
- 변경 단위: `c/tests/test_perflab.c`
- CLI: `make clean && make test`
- 검증 신호: 테스트 바이너리와 trace runner가 마지막 확인 루프를 맡는다.
- 새로 배운 것: 성능 검증은 '빠르다'라는 문장보다 cost signal이 남아 있는지로 평가해야 한다.

### 코드 앵커 — `../problem/data/traces/study.trace` (`c/tests/test_perflab.c:33`)

```c
    perflab_run_trace_file("../problem/data/traces/study.trace", 1, 1, 1, 0, &stats);
    expect_equal_int("study trace config 1 hits", stats.hits, 5);
    expect_equal_int("study trace config 1 misses", stats.misses, 10);
    expect_equal_int("study trace config 1 evictions", stats.evictions, 8);
```

이 조각은 테스트 바이너리와 trace runner가 마지막 확인 루프를 맡는다는 설명이 실제로 어디서 나오는지 보여 준다. `../problem/data/traces/study.trace`를 읽고 나면 다음 장면이 왜 simulator, transpose 전략, 검증 지표를 한 축으로 정리한다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `../problem/data/traces/study.trace` (`c/tests/test_perflab.c:38`)

```c
    perflab_run_trace_file("../problem/data/traces/study.trace", 2, 1, 2, 0, &stats);
    expect_equal_int("study trace config 2 hits", stats.hits, 6);
    expect_equal_int("study trace config 2 misses", stats.misses, 9);
    expect_equal_int("study trace config 2 evictions", stats.evictions, 7);
```

이 조각은 테스트 바이너리와 trace runner가 마지막 확인 루프를 맡는다는 설명이 실제로 어디서 나오는지 보여 준다. `../problem/data/traces/study.trace`를 읽고 나면 다음 장면이 왜 simulator, transpose 전략, 검증 지표를 한 축으로 정리한다로 이어지는지도 한 번에 보인다.

다음 단계에서는 simulator, transpose 전략, 검증 지표를 한 축으로 정리한다.

## Latest CLI Excerpt

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/perflab/c && make clean && make test)
```

```text
C perflab tests passed
csim study.trace (s=1 E=1 b=1): hits=5 misses=10 evictions=8
csim study.trace (s=2 E=1 b=2): hits=6 misses=9 evictions=7
csim study.trace (s=5 E=1 b=5): hits=10 misses=5 evictions=0
transpose 32x32 naive misses=1180 tuned misses=284 correct=1
transpose 64x64 naive misses=4720 tuned misses=1176 correct=1
transpose 61x67 naive misses=4420 tuned misses=1989 correct=1
./build/test_perflab
```
