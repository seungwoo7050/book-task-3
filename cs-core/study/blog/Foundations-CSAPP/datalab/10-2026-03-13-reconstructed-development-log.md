# Data Lab 재구성 개발 로그

`datalab`은 bit-level 제약을 지키면서 정수 표현과 부동소수점 경계를 직접 구현하는 프로젝트다.

2026-03-13에 기존 초안을 `_legacy`로 격리한 뒤, `README`, `problem/`, 실제 구현 파일, `docs/`, 테스트, 현재 다시 실행한 CLI만으로 이 글을 다시 썼다. 그래서 아래 서사는 나중에 답을 알고 난 뒤 매끈하게 정리한 회고가 아니라, 남아 있는 증거를 따라 다시 세운 개발 흐름에 가깝다.

## 이 프로젝트를 다시 읽는 순서

정수 퍼즐에서 mask와 sign bit를 먼저 고정하고, 그 다음 float bit pattern으로 넘어가는 흐름을 복원한다. 이 질문이 너무 빨리 추상적으로 흘러가지 않도록, 글은 세 개의 phase로 나눠 진행한다.

- Phase 1: 정수 퍼즐 contract를 mask 규칙으로 고정한다 — `c/src/bits.c`
- Phase 2: float 문제를 '실수'가 아니라 bit pattern 변환으로 옮긴다 — `c/src/bits.c`
- Phase 3: 공식 boundary와 companion test를 한 번에 닫는다 — `c/tests/test_bits.c`

## Phase 1. 정수 퍼즐 contract를 mask 규칙으로 고정한다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다.

이 시점의 목표는 허용 연산자만으로도 `bitXor`, `isAsciiDigit`, `logicalNeg`, `howManyBits` 같은 퍼즐을 풀 수 있는 공통 패턴을 먼저 세운다.

처음에는 값을 직접 계산하기보다 sign extension과 mask propagation을 잡으면 나머지 퍼즐도 같은 어휘로 설명될 것이라고 봤다. 그런데 실제로 글의 중심이 된 조치는 C/C++의 `bits.c` / `bits.cpp`에서 정수 퍼즐을 한 덩어리로 다루고, 각 함수가 '범위 검사'인지 '비트 전파'인지로 분류했다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/src/bits.c`
- CLI: `gcc -O1 -Wall -Werror -o test_bits test_bits.c ../src/bits.c && ./test_bits`
- 검증 신호: 정수 퍼즐 함수군이 한 파일에서 같은 제약으로 묶여 있어 구현 순서를 역추적할 수 있다.

### 이 장면을 고정하는 코드 — `bitXor` (`c/src/bits.c:8`)

이 단계에서 가장 먼저 붙잡아야 하는 코드는 아래 조각이다.

```c
int bitXor(int x, int y) {
    return ~(~(x & ~y) & ~(~x & y));
}

int tmin(void) {
    return 1 << 31;
}
```

`bitXor`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 two's complement 퍼즐은 공식을 외우기보다 비트가 어떻게 퍼지는지 추적하는 편이 더 안정적이었다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 float 퍼즐을 unsigned bit pattern 관점으로 분리한다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 two's complement 퍼즐은 공식을 외우기보다 비트가 어떻게 퍼지는지 추적하는 편이 더 안정적이었다.

그래서 다음 장면에서는 float 퍼즐을 unsigned bit pattern 관점으로 분리한다.

## Phase 2. float 문제를 '실수'가 아니라 bit pattern 변환으로 옮긴다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다.

이 시점의 목표는 `floatScale2`, `floatFloat2Int`, `floatPower2`가 정수 퍼즐과 다른 규칙을 쓰기 때문에 별도 국면으로 다룬다.

처음에는 IEEE754도 결국 sign/exponent/fraction 경계를 쪼개면 동일한 bit rewrite 문제로 다룰 수 있다고 가정했다. 그런데 실제로 글의 중심이 된 조치는 정수 연산 대신 exponent 조정, denormal 처리, overflow sentinel을 명시하는 쪽으로 구현을 옮겼다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/src/bits.c`
- CLI: `gcc -O1 -Wall -Werror -o test_bits test_bits.c ../src/bits.c && ./test_bits`
- 검증 신호: `docs/concepts/float-boundaries.md`와 float 함수 묶음이 같은 학습 전환점을 보여 준다.

### 이 장면을 고정하는 코드 — `floatScale2` (`c/src/bits.c:81`)

판단이 뒤집히는 지점은 결국 이 구현 세부에서 드러난다.

```c
unsigned floatScale2(unsigned uf) {
    unsigned sign = uf & 0x80000000u;
    unsigned exp = (uf >> 23) & 0xFFu;
    unsigned frac = uf & 0x7FFFFFu;
```

`floatScale2`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 float 경계는 숫자 의미보다 bit layout이 먼저고, denormal/overflow를 branch로 고정해야 실수가 줄었다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 handout verifier와 self-owned edge-case test를 한 흐름으로 닫는다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 float 경계는 숫자 의미보다 bit layout이 먼저고, denormal/overflow를 branch로 고정해야 실수가 줄었다.

그래서 다음 장면에서는 handout verifier와 self-owned edge-case test를 한 흐름으로 닫는다.

## Phase 3. 공식 boundary와 companion test를 한 번에 닫는다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다.

이 시점의 목표는 로컬 handout 검증과 companion edge-case test를 같이 붙이면 '정답처럼 보이는 구현'과 '계약을 통과한 구현'을 구분할 수 있다.

처음에는 공식 verifier는 local-only이지만, 공개 트리에서는 `c/tests/test_bits.c`가 같은 경계값 사고를 다시 확인해 줄 것이라고 봤다. 그런데 실제로 글의 중심이 된 조치는 README의 검증 명령을 따라 `problem/`과 `c/tests/`를 분리하고, 공개 가능한 테스트 하네스를 별도 유지했다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/tests/test_bits.c`
- CLI: `gcc -O1 -Wall -Werror -o test_bits test_bits.c ../src/bits.c && ./test_bits`
- 검증 신호: 실행 출력이 남아 있어 최종 검증 단계를 명확히 닫을 수 있다.

### 이 장면을 고정하는 코드 — `isAsciiDigit(0x30)` (`c/tests/test_bits.c:64`)

끝을 닫는 순간은 늘 테스트나 CLI 쪽 코드가 더 솔직하게 보여 준다.

```c
    TEST("isAsciiDigit(0x30)", isAsciiDigit(0x30) == 1);
    TEST("isAsciiDigit(0x39)", isAsciiDigit(0x39) == 1);
    TEST("isAsciiDigit(0x3A)", isAsciiDigit(0x3A) == 0);
    TEST("isAsciiDigit(0x2F)", isAsciiDigit(0x2F) == 0);
    TEST("isAsciiDigit(-1)",   isAsciiDigit(-1) == 0);
```

`isAsciiDigit(0x30)`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 검증 경계를 분리해 두면 local-only 자산이 빠져도 공개 표면에서 구현 이유를 설명할 수 있다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 '퍼즐 풀이 모음'이 아니라 '계약을 단계적으로 좁힌 기록'으로 정리한다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 검증 경계를 분리해 두면 local-only 자산이 빠져도 공개 표면에서 구현 이유를 설명할 수 있다.

그래서 다음 장면에서는 '퍼즐 풀이 모음'이 아니라 '계약을 단계적으로 좁힌 기록'으로 정리한다.

## CLI로 다시 닫기

문장과 코드만으로는 마지막 닫힘이 약해질 수 있어서, 저장소에서 다시 실행 가능한 대표 명령을 마지막에 그대로 남긴다. 이 출력은 기능이 돌아간다는 사실뿐 아니라 README가 약속한 검증 entrypoint가 아직 살아 있다는 사실까지 함께 보여 준다.

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/datalab/c/tests && gcc -O1 -Wall -Werror -o test_bits test_bits.c ../src/bits.c && ./test_bits)
```

```text
=== 55 / 55 edge-case tests passed ===
```

## 이번에 남은 질문

- 개념 축: `float boundaries`, `integer patterns`
- 대표 테스트/fixture: `c/tests/test_bits.c`, `cpp/tests/test_bits.cpp`
- 다음 질문: 최종 글에서는 '퍼즐 풀이 모음'이 아니라 '계약을 단계적으로 좁힌 기록'으로 정리한다.
