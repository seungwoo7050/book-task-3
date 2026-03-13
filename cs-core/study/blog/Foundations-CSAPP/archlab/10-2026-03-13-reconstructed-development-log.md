# Architecture Lab 재구성 개발 로그

`archlab`은 Y86-64 프로그램 작성, 제어 로직 구현, 파이프라인 성능 개선을 한 흐름으로 묶는 프로젝트다.

2026-03-13에 기존 초안을 `_legacy`로 격리한 뒤, `README`, `problem/`, 실제 구현 파일, `docs/`, 테스트, 현재 다시 실행한 CLI만으로 이 글을 다시 썼다. 그래서 아래 서사는 나중에 답을 알고 난 뒤 매끈하게 정리한 회고가 아니라, 남아 있는 증거를 따라 다시 세운 개발 흐름에 가깝다.

## 이 프로젝트를 다시 읽는 순서

Y86 프로그램, `iaddq` 제어 로직, `ncopy` 성능 개선이 왜 세 개의 다른 문제처럼 느껴지는지 코드 순서로 복원한다. 이 질문이 너무 빨리 추상적으로 흘러가지 않도록, 글은 세 개의 phase로 나눠 진행한다.

- Phase 1: Y86 문제를 companion 코드와 part split으로 분해한다 — `c/src/mini_archlab.c`, `y86/src/ncopy.ys`
- Phase 2: `iaddq`를 단일 명령 추가가 아니라 control-signal 변화로 본다 — `c/src/mini_archlab.c`
- Phase 3: `ncopy`를 '더 빠르게'가 아니라 cycle budget으로 해석한다 — `c/src/mini_archlab.c`

## Phase 1. Y86 문제를 companion 코드와 part split으로 분해한다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다.

이 시점의 목표는 `sum`, `rsum`, `copy`, `ncopy` 같은 Y86 작업과 companion C 테스트가 같은 문제를 다른 표면으로 설명하게 만든다.

처음에는 원문 lab의 파트 구성이 그대로 남아 있어야 나중에 성능/제어 로직 작업으로 넘어가도 길을 잃지 않을 거라고 봤다. 그런데 실제로 글의 중심이 된 조치는 Y86 소스는 `y86/src/`에, 재현 가능한 샘플과 테스트는 `c/src/mini_archlab.c`로 분리해 공개 경계를 만들었다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/src/mini_archlab.c`, `y86/src/ncopy.ys`
- CLI: `make clean && make test`
- 검증 신호: 문제 분해가 먼저 되어 있어 이후 제어/성능 논의를 붙일 자리가 생긴다.

### 이 장면을 고정하는 코드 — `ncopy` (`y86/src/ncopy.ys:3`)

이 단계에서 가장 먼저 붙잡아야 하는 코드는 아래 조각이다.

```asm
ncopy:
    xorq %rax, %rax
    andq %rdx, %rdx
    jle Done
    irmovq $1, %rbp
```

`ncopy`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 파트를 분리한 덕분에 'isa 문법'과 '검증 가능한 결과'를 따로 읽을 수 있게 됐다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 `iaddq`가 실제로 제어 신호를 얼마나 흔드는지로 초점을 옮긴다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 파트를 분리한 덕분에 'ISA 문법'과 '검증 가능한 결과'를 따로 읽을 수 있게 됐다.

그래서 다음 장면에서는 `iaddq`가 실제로 제어 신호를 얼마나 흔드는지로 초점을 옮긴다.

## Phase 2. `iaddq`를 단일 명령 추가가 아니라 control-signal 변화로 본다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다.

이 시점의 목표는 `seq_iaddq`와 overflow helper를 보면 결국 핵심은 새 opcode를 넣는 일이 아니라 decode/execute 경계에서 어떤 신호를 더 건드려야 하는지다.

처음에는 Y86 instruction을 하나 추가해도 데이터 경로와 condition code 규칙을 건드리는 지점이 더 클 것이라고 예상했다. 그런데 실제로 글의 중심이 된 조치는 `seq_iaddq`, `add_overflow`, docs의 control-signal 메모를 중심으로 구현/설명을 묶었다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/src/mini_archlab.c`
- CLI: `make clean && make test`
- 검증 신호: 제어 로직을 companion 함수로 둔 덕분에 결과를 C 테스트로 다시 확인할 수 있다.

### 이 장면을 고정하는 코드 — `add_overflow` (`c/src/mini_archlab.c:36`)

판단이 뒤집히는 지점은 결국 이 구현 세부에서 드러난다.

```c
static int add_overflow(int64_t a, int64_t b, int64_t result)
{
    return ((a ^ result) & (b ^ result)) < 0;
}
```

`add_overflow`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 isa 확장은 새 문법보다 기존 datapath contract를 얼마나 덜 깨뜨리느냐가 더 중요했다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 마지막 국면에서는 `ncopy`를 성능 지표와 연결한다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 ISA 확장은 새 문법보다 기존 datapath contract를 얼마나 덜 깨뜨리느냐가 더 중요했다.

그래서 다음 장면에서는 마지막 국면에서는 `ncopy`를 성능 지표와 연결한다.

## Phase 3. `ncopy`를 '더 빠르게'가 아니라 cycle budget으로 해석한다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다.

이 시점의 목표는 `baseline_cycles`, `optimized_cycles`, `arch_ncopy_optimized`를 같이 보면 최적화는 감이 아니라 cost model을 맞추는 작업이다.

처음에는 copy correctness만 통과하면 끝이 아니라, pipeline cost를 숫자로 보지 않으면 왜 unroll/branch 정리가 필요한지 설명할 수 없다고 봤다. 그런데 실제로 글의 중심이 된 조치는 baseline/optimized 두 경로를 같이 두고 테스트 바이너리에서 기능과 비용을 동시에 비교하게 만들었다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/src/mini_archlab.c`
- CLI: `make clean && make test`
- 검증 신호: 샘플 실행과 테스트 바이너리가 남아 있어 마지막 국면을 CLI로 닫을 수 있다.

### 이 장면을 고정하는 코드 — `baseline_cycles` (`c/src/mini_archlab.c:58`)

끝을 닫는 순간은 늘 테스트나 CLI 쪽 코드가 더 솔직하게 보여 준다.

```c
static uint64_t baseline_cycles(int64_t len)
{
    if (len <= 0) {
        return 6;
    }
    return 8 + (uint64_t)len * 9;
}
```

`baseline_cycles`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 성능 최적화는 별도 마법이 아니라 동일한 contract를 유지한 채 낭비 cycle을 줄이는 재배치였다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 Y86 파트 분리, control signal, cost model을 한 줄로 연결한다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 성능 최적화는 별도 마법이 아니라 동일한 contract를 유지한 채 낭비 cycle을 줄이는 재배치였다.

그래서 다음 장면에서는 Y86 파트 분리, control signal, cost model을 한 줄로 연결한다.

## CLI로 다시 닫기

문장과 코드만으로는 마지막 닫힘이 약해질 수 있어서, 저장소에서 다시 실행 가능한 대표 명령을 마지막에 그대로 남긴다. 이 출력은 기능이 돌아간다는 사실뿐 아니라 README가 약속한 검증 entrypoint가 아직 살아 있다는 사실까지 함께 보여 준다.

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

## 이번에 남은 질문

- 개념 축: `iaddq and control signals`, `part split`, `pipeline cost model`
- 대표 테스트/fixture: `c/tests/test_mini_archlab.c`, `cpp/tests/test_mini_archlab.cpp`
- 다음 질문: 최종 글에서는 Y86 파트 분리, control signal, cost model을 한 줄로 연결한다.
