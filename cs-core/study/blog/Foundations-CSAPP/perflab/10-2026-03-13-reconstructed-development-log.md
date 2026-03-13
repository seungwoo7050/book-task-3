# Performance Lab 재구성 개발 로그

`perflab`은 cache simulator와 transpose 최적화를 통해 "왜 더 빠른가"를 코드와 지표로 설명하는 프로젝트다.

2026-03-13에 기존 초안을 `_legacy`로 격리한 뒤, `README`, `problem/`, 실제 구현 파일, `docs/`, 테스트, 현재 다시 실행한 CLI만으로 이 글을 다시 썼다. 그래서 아래 서사는 나중에 답을 알고 난 뒤 매끈하게 정리한 회고가 아니라, 남아 있는 증거를 따라 다시 세운 개발 흐름에 가깝다.

## 이 프로젝트를 다시 읽는 순서

cache simulator와 transpose 최적화를 따로 떼지 않고, 같은 cost model을 두 개의 다른 구현 표면에 배치한 흐름으로 복원한다. 이 질문이 너무 빨리 추상적으로 흘러가지 않도록, 글은 세 개의 phase로 나눠 진행한다.

- Phase 1: cache simulator로 cost model을 먼저 만든다 — `c/src/perflab.c`
- Phase 2: transpose를 matrix 연산이 아니라 cache line 재배치로 본다 — `c/src/perflab.c`, `cpp/src/perflab.cpp`
- Phase 3: 검증을 기능 테스트와 cost signal 두 축으로 닫는다 — `c/tests/test_perflab.c`

## Phase 1. cache simulator로 cost model을 먼저 만든다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다.

이 시점의 목표는 transpose 최적화를 설명하려면 먼저 miss/hit가 어떤 식으로 계산되는지 추적할 도구가 필요하다.

처음에는 시뮬레이터 없이 transpose만 고치면 '왜 빨라졌는지'를 숫자로 설명하지 못할 거라고 봤다. 그런데 실제로 글의 중심이 된 조치는 `cache_sim_init`, `cache_access`, `perflab_run_trace_file`을 먼저 세워 trace 기반 cost model을 고정했다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/src/perflab.c`
- CLI: `make clean && make test`
- 검증 신호: trace runner와 simulator helper가 성능 설명의 바닥을 깔아 준다.

### 이 장면을 고정하는 코드 — `cache_sim_init` (`c/src/perflab.c:27`)

이 단계에서 가장 먼저 붙잡아야 하는 코드는 아래 조각이다.

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

`cache_sim_init`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 성능 프로젝트도 결국 먼저 필요한 것은 최적화 기술이 아니라 관측 가능한 지표 표면이었다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 transpose 전략을 cache line 단위 사고로 옮긴다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 성능 프로젝트도 결국 먼저 필요한 것은 최적화 기술이 아니라 관측 가능한 지표 표면이었다.

그래서 다음 장면에서는 transpose 전략을 cache line 단위 사고로 옮긴다.

## Phase 2. transpose를 matrix 연산이 아니라 cache line 재배치로 본다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다.

이 시점의 목표는 `transpose_32`, `transpose_64`, `transpose_generic`을 나눠 둔 이유가 바로 workload별 locality 차이를 드러내기 위해서다.

처음에는 한 가지 루프만 미세 조정하는 것보다 행렬 크기별 패턴 차이를 먼저 드러내는 편이 설명력이 높다고 판단했다. 그런데 실제로 글의 중심이 된 조치는 naive 경로와 optimized 경로를 같이 두고, load/store helper를 통해 접근 패턴을 눈에 보이는 단위로 만들었다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/src/perflab.c`, `cpp/src/perflab.cpp`
- CLI: `make clean && make test`
- 검증 신호: 접근 helper와 전략 함수가 최적화 이유를 코드 수준에서 추적하게 해 준다.

### 이 장면을 고정하는 코드 — `transpose_32` (`cpp/src/perflab.cpp:145`)

판단이 뒤집히는 지점은 결국 이 구현 세부에서 드러난다.

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

`transpose_32`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 최적화는 코드 양을 늘리는 일이 아니라 locality를 어기는 이동을 줄이는 재배치라는 점이 분명해졌다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 trace/test 결과로 cost model과 구현을 다시 연결한다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 최적화는 코드 양을 늘리는 일이 아니라 locality를 어기는 이동을 줄이는 재배치라는 점이 분명해졌다.

그래서 다음 장면에서는 trace/test 결과로 cost model과 구현을 다시 연결한다.

## Phase 3. 검증을 기능 테스트와 cost signal 두 축으로 닫는다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다.

이 시점의 목표는 performance lab은 정답 여부와 cost improvement를 같이 닫아야 한다.

처음에는 unit test만 통과해도 충분하지 않고, trace/run 결과가 README의 설명과 맞아야 프로젝트가 끝난다고 봤다. 그런데 실제로 글의 중심이 된 조치는 `make test` 경로와 `problem/`의 status/compile entrypoint를 같이 두어 기능과 지표를 한 흐름으로 묶었다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/tests/test_perflab.c`
- CLI: `make clean && make test`
- 검증 신호: 테스트 바이너리와 trace runner가 마지막 확인 루프를 맡는다.

### 이 장면을 고정하는 코드 — `../problem/data/traces/study.trace` (`c/tests/test_perflab.c:33`)

끝을 닫는 순간은 늘 테스트나 CLI 쪽 코드가 더 솔직하게 보여 준다.

```c
    perflab_run_trace_file("../problem/data/traces/study.trace", 1, 1, 1, 0, &stats);
    expect_equal_int("study trace config 1 hits", stats.hits, 5);
    expect_equal_int("study trace config 1 misses", stats.misses, 10);
    expect_equal_int("study trace config 1 evictions", stats.evictions, 8);
```

`../problem/data/traces/study.trace`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 성능 검증은 '빠르다'라는 문장보다 cost signal이 남아 있는지로 평가해야 한다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 simulator, transpose 전략, 검증 지표를 한 축으로 정리한다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 성능 검증은 '빠르다'라는 문장보다 cost signal이 남아 있는지로 평가해야 한다.

그래서 다음 장면에서는 simulator, transpose 전략, 검증 지표를 한 축으로 정리한다.

## CLI로 다시 닫기

문장과 코드만으로는 마지막 닫힘이 약해질 수 있어서, 저장소에서 다시 실행 가능한 대표 명령을 마지막에 그대로 남긴다. 이 출력은 기능이 돌아간다는 사실뿐 아니라 README가 약속한 검증 entrypoint가 아직 살아 있다는 사실까지 함께 보여 준다.

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

## 이번에 남은 질문

- 개념 축: `cache sim lru`, `transpose strategies`
- 대표 테스트/fixture: `c/tests/test_perflab.c`, `cpp/tests/test_perflab.cpp`
- 다음 질문: 최종 글은 simulator, transpose 전략, 검증 지표를 한 축으로 정리한다.
