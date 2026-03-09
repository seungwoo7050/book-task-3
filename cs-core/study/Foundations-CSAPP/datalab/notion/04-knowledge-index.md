# Data Lab — 핵심 개념 인덱스

## 이 문서의 목적

Data Lab을 풀면서 체화한 개념들을 정리한 인덱스다. 각 항목은 "어디서 등장했고 왜 중요한지"를 포함한다. 나중에 관련 주제를 다시 볼 때 빠르게 참조하기 위한 용도다.

---

## 2의 보수 (Two's Complement)

**등장**: 정수 퍼즐 전체, 특히 `negate`, `isLessOrEqual`, `howManyBits`

32비트 `int`에서 양수의 최상위 비트는 0, 음수는 1이다. INT_MIN(-2,147,483,648)과 INT_MAX(2,147,483,647)가 대칭이 아니라는 사실이 여러 퍼즐의 경계 조건을 결정한다.

`negate(x)`가 `~x + 1`인 이유도 2의 보수 인코딩에서 직접 나온다. INT_MIN을 `negate`하면 자기 자신이 돌아오는 것도 이 비대칭성의 결과다.

**참고**: CS:APP 3/e 2.2절 — 2의 보수 인코딩

---

## 부울-마스크 변환 (Boolean to Full-Width Mask)

**등장**: `conditional`, `isAsciiDigit`, `isLessOrEqual`

0 또는 1인 값을 0x00000000 또는 0xFFFFFFFF로 확장하는 패턴. 핵심은 `(!!x << 31) >> 31`에서 산술 우시프트가 부호 비트를 복제하는 성질을 이용하는 것이다.

이 마스크를 `(mask & a) | (~mask & b)` 형태에 넣으면 분기 없는 조건 선택이 완성된다. SIMD 프로그래밍에서도 같은 패턴이 핵심이므로, 비트 연산의 첫 관문이자 실용적 기법이기도 하다.

---

## 산술 시프트 vs 논리 시프트

**등장**: `conditional`, `isLessOrEqual`, `howManyBits`

C 표준에서 부호 있는 정수의 우시프트(`int >> n`)는 구현 정의(implementation-defined)다. 하지만 GCC, Clang 등 주요 컴파일러는 산술 시프트(sign-extending right shift)를 수행한다. Data Lab의 퍼즐은 이 사실에 의존한다.

`x >> 31`은 x가 음수이면 0xFFFFFFFF(-1), 비음수이면 0x00000000을 반환한다. 이 패턴이 부호 분기와 마스크 생성의 기반이 된다.

---

## IEEE 754 Single-Precision 부동소수점

**등장**: `floatScale2`, `floatFloat2Int`, `floatPower2`

32비트 float의 레이아웃: sign(1비트) + exp(8비트) + frac(23비트).

세 가지 범주 분류가 모든 부동소수점 퍼즐의 출발점이다:
- **정규수** (exp: 1~254): 유효숫자에 implicit 1이 포함됨
- **비정규수** (exp: 0, frac ≠ 0): 0 근처의 점진적 언더플로우를 위한 구간
- **특수값** (exp: 0xFF): NaN(frac ≠ 0) 또는 ±무한대(frac = 0)

**참고**: CS:APP 3/e 2.4절 — 부동소수점

---

## 이진 탐색을 시프트로 구현하기

**등장**: `howManyBits`

루프 없이 32비트 정수의 유효 비트 수를 세는 것이 핵심 과제. 16→8→4→2→1로 절반씩 탐색 범위를 줄이면서, `!!(x >> 16) << 4` 형태로 "이 구간에 비트가 있으면 시프트 양을 생성"하는 패턴을 사용한다.

이 기법은 비트 레벨 이진 탐색(bit-level binary search)의 정석으로, `__builtin_clz`(count leading zeros) 같은 컴파일러 내장 함수의 내부 구현과 동일한 원리다.

---

## 주요 경계값 테이블

이 퍼즐들을 디버깅하면서 반복적으로 확인한 값들:

| 값 | 16진 표현 | 의미 | 관련 퍼즐 |
|---|---|---|---|
| 0 | 0x00000000 | 유일하게 `x \| (~x+1)`이 비음수 | `logicalNeg` |
| -1 | 0xFFFFFFFF | INT_MAX와 비트 반전 성질 공유 | `isTmax` |
| INT_MIN | 0x80000000 | `negate` 오버플로우, 비대칭 | `negate`, `isLessOrEqual` |
| INT_MAX | 0x7FFFFFFF | `x+1`하면 모든 비트 반전 | `isTmax`, `howManyBits` |
| +0.0f | 0x00000000 | 비정규 경계 | `floatScale2` |
| 1.0f | 0x3F800000 | 정규수 기본값 | `floatFloat2Int` |
| +∞ | 0x7F800000 | exp=0xFF, frac=0 | 부동소수점 전체 |
| NaN | 0x7FC00000 | exp=0xFF, frac≠0 | 부동소수점 전체 |

---

## 도구 참조

| 도구 | 역할 | 비고 |
|---|---|---|
| `dlc` (Data Lab Checker) | 연산자 합법성/상수 범위 검사 | Linux/amd64 ELF, Docker 필요 |
| `btest` | 정확성 테스트 (전수/무작위) | `-T 20` 옵션: 에뮬레이션 환경용 |
| `gcc -m32` | 32비트 빌드 | Apple Silicon 비호환, Makefile 조건 분기 |
| Docker (debian:bookworm-slim) | 크로스 플랫폼 검증 | `gcc-multilib`, `libc6-dev-i386` 포함 |

---

## 참고 자료

- **CS:APP 3/e, Chapter 2** — 정보의 표현과 처리
- **IEEE 754-2008** — 부동소수점 산술 표준
- **CMU Data Lab 핸드아웃** — `csapp.cs.cmu.edu/3e/datalab-handout.tar`