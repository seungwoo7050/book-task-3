# Architecture Lab Evidence Ledger

이 문서는 최종 글보다 한 단계 앞에 있는 근거 문서다. 기존 `blog/` 초안은 입력에서 제외했고, 지금 남아 있는 README, problem 설명, 구현 파일, 테스트, git history, 재실행한 CLI만으로 chronology를 다시 세웠다.

## 근거 묶음

`archlab`은 Y86-64 프로그램 작성, 제어 로직 구현, 파이프라인 성능 개선을 한 흐름으로 묶는 프로젝트다. 구현의 중심은 `c`, `cpp`, `y86`에 퍼져 있고, 글에서 반복해서 참조할 핵심 파일은 `c/src/main.c`, `c/src/mini_archlab.c`, `cpp/src/main.cpp`, `cpp/src/mini_archlab.cpp`, `y86/src/copy.ys`, `y86/src/ncopy.ys`, `y86/src/rsum.ys`, `y86/src/sum.ys`다. 검증 표면은 `c/tests/test_mini_archlab.c`, `cpp/tests/test_mini_archlab.cpp`와 `make clean && make test`에 걸쳐 있으며, 이번에 다시 붙잡은 개념 축은 `iaddq and control signals`, `part split`, `pipeline cost model`이다.

## Git History Anchor

- `2026-03-09	b1cbad9	docs(notion): cs-core, network-atda`
- `2026-03-10	ced9d08	docs: enhance cs-core`
- `2026-03-11	bbb6673	Track 1에 대한 전반적인 개선 완료`
- `2026-03-13	abeead6	docs: TRACK 1 에대한 blog/ 작업 1차 완료`

## 1. Phase 1 - Y86 문제를 companion 코드와 part split으로 분해한다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다. 이 시점의 목표는 `sum`, `rsum`, `copy`, `ncopy` 같은 Y86 작업과 companion C 테스트가 같은 문제를 다른 표면으로 설명하게 만든다.

그때 세운 가설은 원문 lab의 파트 구성이 그대로 남아 있어야 나중에 성능/제어 로직 작업으로 넘어가도 길을 잃지 않을 거라고 봤다. 실제 조치는 Y86 소스는 `y86/src/`에, 재현 가능한 샘플과 테스트는 `c/src/mini_archlab.c`로 분리해 공개 경계를 만들었다.

- 정리해 둔 근거:
- 변경 단위: `c/src/mini_archlab.c`, `y86/src/ncopy.ys`
- CLI: `make clean && make test`
- 검증 신호: 문제 분해가 먼저 되어 있어 이후 제어/성능 논의를 붙일 자리가 생긴다.
- 새로 배운 것: 파트를 분리한 덕분에 'ISA 문법'과 '검증 가능한 결과'를 따로 읽을 수 있게 됐다.

### 코드 앵커 — `ncopy` (`y86/src/ncopy.ys:3`)

```asm
ncopy:
    xorq %rax, %rax
    andq %rdx, %rdx
    jle Done
    irmovq $1, %rbp
```

이 조각은 문제 분해가 먼저 되어 있어 이후 제어/성능 논의를 붙일 자리가 생긴다는 설명이 실제로 어디서 나오는지 보여 준다. `ncopy`를 읽고 나면 다음 장면이 왜 `iaddq`가 실제로 제어 신호를 얼마나 흔드는지로 초점을 옮긴다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `arch_copy_block` (`c/src/mini_archlab.c:24`)

```c
int64_t arch_copy_block(const int64_t *src, int64_t *dst, int64_t len)
{
    int64_t checksum = 0;
    int64_t index;
```

이 조각은 문제 분해가 먼저 되어 있어 이후 제어/성능 논의를 붙일 자리가 생긴다는 설명이 실제로 어디서 나오는지 보여 준다. `arch_copy_block`를 읽고 나면 다음 장면이 왜 `iaddq`가 실제로 제어 신호를 얼마나 흔드는지로 초점을 옮긴다로 이어지는지도 한 번에 보인다.

다음 단계에서는 `iaddq`가 실제로 제어 신호를 얼마나 흔드는지로 초점을 옮긴다.

## 2. Phase 2 - `iaddq`를 단일 명령 추가가 아니라 control-signal 변화로 본다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다. 이 시점의 목표는 `seq_iaddq`와 overflow helper를 보면 결국 핵심은 새 opcode를 넣는 일이 아니라 decode/execute 경계에서 어떤 신호를 더 건드려야 하는지다.

그때 세운 가설은 Y86 instruction을 하나 추가해도 데이터 경로와 condition code 규칙을 건드리는 지점이 더 클 것이라고 예상했다. 실제 조치는 `seq_iaddq`, `add_overflow`, docs의 control-signal 메모를 중심으로 구현/설명을 묶었다.

- 정리해 둔 근거:
- 변경 단위: `c/src/mini_archlab.c`
- CLI: `make clean && make test`
- 검증 신호: 제어 로직을 companion 함수로 둔 덕분에 결과를 C 테스트로 다시 확인할 수 있다.
- 새로 배운 것: ISA 확장은 새 문법보다 기존 datapath contract를 얼마나 덜 깨뜨리느냐가 더 중요했다.

### 코드 앵커 — `add_overflow` (`c/src/mini_archlab.c:36`)

```c
static int add_overflow(int64_t a, int64_t b, int64_t result)
{
    return ((a ^ result) & (b ^ result)) < 0;
}
```

이 조각은 제어 로직을 companion 함수로 둔 덕분에 결과를 c 테스트로 다시 확인할 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `add_overflow`를 읽고 나면 다음 장면이 왜 마지막 국면에서는 `ncopy`를 성능 지표와 연결한다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `arch_seq_iaddq` (`c/src/mini_archlab.c:41`)

```c
SeqIaddqTrace arch_seq_iaddq(uint64_t pc, uint8_t dst_reg, int64_t valB, int64_t valC)
{
    SeqIaddqTrace trace;
    uint64_t raw = (uint64_t)valB + (uint64_t)valC;
```

이 조각은 제어 로직을 companion 함수로 둔 덕분에 결과를 c 테스트로 다시 확인할 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `arch_seq_iaddq`를 읽고 나면 다음 장면이 왜 마지막 국면에서는 `ncopy`를 성능 지표와 연결한다로 이어지는지도 한 번에 보인다.

다음 단계에서는 마지막 국면에서는 `ncopy`를 성능 지표와 연결한다.

## 3. Phase 3 - `ncopy`를 '더 빠르게'가 아니라 cycle budget으로 해석한다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다. 이 시점의 목표는 `baseline_cycles`, `optimized_cycles`, `arch_ncopy_optimized`를 같이 보면 최적화는 감이 아니라 cost model을 맞추는 작업이다.

그때 세운 가설은 copy correctness만 통과하면 끝이 아니라, pipeline cost를 숫자로 보지 않으면 왜 unroll/branch 정리가 필요한지 설명할 수 없다고 봤다. 실제 조치는 baseline/optimized 두 경로를 같이 두고 테스트 바이너리에서 기능과 비용을 동시에 비교하게 만들었다.

- 정리해 둔 근거:
- 변경 단위: `c/src/mini_archlab.c`
- CLI: `make clean && make test`
- 검증 신호: 샘플 실행과 테스트 바이너리가 남아 있어 마지막 국면을 CLI로 닫을 수 있다.
- 새로 배운 것: 성능 최적화는 별도 마법이 아니라 동일한 contract를 유지한 채 낭비 cycle을 줄이는 재배치였다.

### 코드 앵커 — `baseline_cycles` (`c/src/mini_archlab.c:58`)

```c
static uint64_t baseline_cycles(int64_t len)
{
    if (len <= 0) {
        return 6;
    }
    return 8 + (uint64_t)len * 9;
}
```

이 조각은 샘플 실행과 테스트 바이너리가 남아 있어 마지막 국면을 cli로 닫을 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `baseline_cycles`를 읽고 나면 다음 장면이 왜 Y86 파트 분리, control signal, cost model을 한 줄로 연결한다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `optimized_cycles` (`c/src/mini_archlab.c:66`)

```c
static uint64_t optimized_cycles(int64_t len)
{
    uint64_t chunks4;
    uint64_t remainder;
```

이 조각은 샘플 실행과 테스트 바이너리가 남아 있어 마지막 국면을 cli로 닫을 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `optimized_cycles`를 읽고 나면 다음 장면이 왜 Y86 파트 분리, control signal, cost model을 한 줄로 연결한다로 이어지는지도 한 번에 보인다.

다음 단계에서는 Y86 파트 분리, control signal, cost model을 한 줄로 연결한다.

## Latest CLI Excerpt

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/archlab/c && make clean && make test)
```

```text
C mini-archlab tests passed
Part A iterative sum: 3258
Part A recursive sum: 3258
Part A copy xor: 3258
Part B iaddq sample: pc=0x100 next=0x10a valE=4 ZF=0 SF=0 OF=0
Part C baseline: count=5 cycles=80 cpe=10.00
Part C optimized: count=5 cycles=54 cpe=6.75
./build/test_mini_archlab
```
