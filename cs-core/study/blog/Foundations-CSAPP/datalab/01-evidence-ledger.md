# Data Lab Evidence Ledger

이 문서는 최종 글보다 한 단계 앞에 있는 근거 문서다. 기존 `blog/` 초안은 입력에서 제외했고, 지금 남아 있는 README, problem 설명, 구현 파일, 테스트, git history, 재실행한 CLI만으로 chronology를 다시 세웠다.

## 근거 묶음

`datalab`은 bit-level 제약을 지키면서 정수 표현과 부동소수점 경계를 직접 구현하는 프로젝트다. 구현의 중심은 `c`, `cpp`에 퍼져 있고, 글에서 반복해서 참조할 핵심 파일은 `c/src/bits.c`, `cpp/src/bits.cpp`다. 검증 표면은 `c/tests/test_bits.c`, `cpp/tests/test_bits.cpp`와 `gcc -O1 -Wall -Werror -o test_bits test_bits.c ../src/bits.c && ./test_bits`에 걸쳐 있으며, 이번에 다시 붙잡은 개념 축은 `float boundaries`, `integer patterns`이다.

## Git History Anchor

- `2026-03-09	b1cbad9	docs(notion): cs-core, network-atda`
- `2026-03-10	ced9d08	docs: enhance cs-core`
- `2026-03-11	bbb6673	Track 1에 대한 전반적인 개선 완료`
- `2026-03-13	abeead6	docs: TRACK 1 에대한 blog/ 작업 1차 완료`

## 1. Phase 1 - 정수 퍼즐 contract를 mask 규칙으로 고정한다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다. 이 시점의 목표는 허용 연산자만으로도 `bitXor`, `isAsciiDigit`, `logicalNeg`, `howManyBits` 같은 퍼즐을 풀 수 있는 공통 패턴을 먼저 세운다.

그때 세운 가설은 값을 직접 계산하기보다 sign extension과 mask propagation을 잡으면 나머지 퍼즐도 같은 어휘로 설명될 것이라고 봤다. 실제 조치는 C/C++의 `bits.c` / `bits.cpp`에서 정수 퍼즐을 한 덩어리로 다루고, 각 함수가 '범위 검사'인지 '비트 전파'인지로 분류했다.

- 정리해 둔 근거:
- 변경 단위: `c/src/bits.c`
- CLI: `gcc -O1 -Wall -Werror -o test_bits test_bits.c ../src/bits.c && ./test_bits`
- 검증 신호: 정수 퍼즐 함수군이 한 파일에서 같은 제약으로 묶여 있어 구현 순서를 역추적할 수 있다.
- 새로 배운 것: two's complement 퍼즐은 공식을 외우기보다 비트가 어떻게 퍼지는지 추적하는 편이 더 안정적이었다.

### 코드 앵커 — `bitXor` (`c/src/bits.c:8`)

```c
int bitXor(int x, int y) {
    return ~(~(x & ~y) & ~(~x & y));
}

int tmin(void) {
    return 1 << 31;
}
```

이 조각은 정수 퍼즐 함수군이 한 파일에서 같은 제약으로 묶여 있어 구현 순서를 역추적할 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `bitXor`를 읽고 나면 다음 장면이 왜 float 퍼즐을 unsigned bit pattern 관점으로 분리한다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `isAsciiDigit` (`c/src/bits.c:31`)

```c
int isAsciiDigit(int x) {
    int lower = x + (~0x30 + 1);
    int upper = 0x39 + (~x + 1);
    return !((lower >> 31) | (upper >> 31));
}
```

이 조각은 정수 퍼즐 함수군이 한 파일에서 같은 제약으로 묶여 있어 구현 순서를 역추적할 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `isAsciiDigit`를 읽고 나면 다음 장면이 왜 float 퍼즐을 unsigned bit pattern 관점으로 분리한다로 이어지는지도 한 번에 보인다.

다음 단계에서는 float 퍼즐을 unsigned bit pattern 관점으로 분리한다.

## 2. Phase 2 - float 문제를 '실수'가 아니라 bit pattern 변환으로 옮긴다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다. 이 시점의 목표는 `floatScale2`, `floatFloat2Int`, `floatPower2`가 정수 퍼즐과 다른 규칙을 쓰기 때문에 별도 국면으로 다룬다.

그때 세운 가설은 IEEE754도 결국 sign/exponent/fraction 경계를 쪼개면 동일한 bit rewrite 문제로 다룰 수 있다고 가정했다. 실제 조치는 정수 연산 대신 exponent 조정, denormal 처리, overflow sentinel을 명시하는 쪽으로 구현을 옮겼다.

- 정리해 둔 근거:
- 변경 단위: `c/src/bits.c`
- CLI: `gcc -O1 -Wall -Werror -o test_bits test_bits.c ../src/bits.c && ./test_bits`
- 검증 신호: `docs/concepts/float-boundaries.md`와 float 함수 묶음이 같은 학습 전환점을 보여 준다.
- 새로 배운 것: float 경계는 숫자 의미보다 bit layout이 먼저고, denormal/overflow를 branch로 고정해야 실수가 줄었다.

### 코드 앵커 — `floatScale2` (`c/src/bits.c:81`)

```c
unsigned floatScale2(unsigned uf) {
    unsigned sign = uf & 0x80000000u;
    unsigned exp = (uf >> 23) & 0xFFu;
    unsigned frac = uf & 0x7FFFFFu;
```

이 조각은 `docs/concepts/float-boundaries.md`와 float 함수 묶음이 같은 학습 전환점을 보여 준다는 설명이 실제로 어디서 나오는지 보여 준다. `floatScale2`를 읽고 나면 다음 장면이 왜 handout verifier와 self-owned edge-case test를 한 흐름으로 닫는다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `floatFloat2Int` (`c/src/bits.c:99`)

```c
int floatFloat2Int(unsigned uf) {
    int sign = uf >> 31;
    int exp = ((uf >> 23) & 0xFF) + (~127 + 1);
    int frac = (uf & 0x7FFFFF) | 0x800000;
```

이 조각은 `docs/concepts/float-boundaries.md`와 float 함수 묶음이 같은 학습 전환점을 보여 준다는 설명이 실제로 어디서 나오는지 보여 준다. `floatFloat2Int`를 읽고 나면 다음 장면이 왜 handout verifier와 self-owned edge-case test를 한 흐름으로 닫는다로 이어지는지도 한 번에 보인다.

다음 단계에서는 handout verifier와 self-owned edge-case test를 한 흐름으로 닫는다.

## 3. Phase 3 - 공식 boundary와 companion test를 한 번에 닫는다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다. 이 시점의 목표는 로컬 handout 검증과 companion edge-case test를 같이 붙이면 '정답처럼 보이는 구현'과 '계약을 통과한 구현'을 구분할 수 있다.

그때 세운 가설은 공식 verifier는 local-only이지만, 공개 트리에서는 `c/tests/test_bits.c`가 같은 경계값 사고를 다시 확인해 줄 것이라고 봤다. 실제 조치는 README의 검증 명령을 따라 `problem/`과 `c/tests/`를 분리하고, 공개 가능한 테스트 하네스를 별도 유지했다.

- 정리해 둔 근거:
- 변경 단위: `c/tests/test_bits.c`
- CLI: `gcc -O1 -Wall -Werror -o test_bits test_bits.c ../src/bits.c && ./test_bits`
- 검증 신호: 실행 출력이 남아 있어 최종 검증 단계를 명확히 닫을 수 있다.
- 새로 배운 것: 검증 경계를 분리해 두면 local-only 자산이 빠져도 공개 표면에서 구현 이유를 설명할 수 있다.

### 코드 앵커 — `isAsciiDigit(0x30)` (`c/tests/test_bits.c:64`)

```c
    TEST("isAsciiDigit(0x30)", isAsciiDigit(0x30) == 1);
    TEST("isAsciiDigit(0x39)", isAsciiDigit(0x39) == 1);
    TEST("isAsciiDigit(0x3A)", isAsciiDigit(0x3A) == 0);
    TEST("isAsciiDigit(0x2F)", isAsciiDigit(0x2F) == 0);
    TEST("isAsciiDigit(-1)",   isAsciiDigit(-1) == 0);
```

이 조각은 실행 출력이 남아 있어 최종 검증 단계를 명확히 닫을 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `isAsciiDigit(0x30)`를 읽고 나면 다음 장면이 왜 '퍼즐 풀이 모음'이 아니라 '계약을 단계적으로 좁힌 기록'으로 정리한다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `isAsciiDigit(0x39)` (`c/tests/test_bits.c:65`)

```c
    TEST("isAsciiDigit(0x39)", isAsciiDigit(0x39) == 1);
    TEST("isAsciiDigit(0x3A)", isAsciiDigit(0x3A) == 0);
    TEST("isAsciiDigit(0x2F)", isAsciiDigit(0x2F) == 0);
    TEST("isAsciiDigit(-1)",   isAsciiDigit(-1) == 0);
```

이 조각은 실행 출력이 남아 있어 최종 검증 단계를 명확히 닫을 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `isAsciiDigit(0x39)`를 읽고 나면 다음 장면이 왜 '퍼즐 풀이 모음'이 아니라 '계약을 단계적으로 좁힌 기록'으로 정리한다로 이어지는지도 한 번에 보인다.

다음 단계에서는 '퍼즐 풀이 모음'이 아니라 '계약을 단계적으로 좁힌 기록'으로 정리한다.

## Latest CLI Excerpt

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/datalab/c/tests && gcc -O1 -Wall -Werror -o test_bits test_bits.c ../src/bits.c && ./test_bits)
```

```text
=== 55 / 55 edge-case tests passed ===
```
