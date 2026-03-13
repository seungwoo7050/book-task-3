# Data Lab Structure Outline

이 문서는 최종 blog를 어떤 곡선으로 읽히게 만들지 미리 고정하는 편집 설계 메모다. 근거는 모두 `01-evidence-ledger.md`와 실제 소스에서 왔고, 여기서는 그 근거를 어떤 순서로 보여 줄 때 가장 자연스럽게 이해되는지에 집중한다.

## 이 시리즈의 편집 원칙

Data Lab에서는 결론을 먼저 선언하기보다, 구현이 어디서부터 단단해졌는지를 보여 주는 편이 더 중요하다. 그래서 최종 글은 문제를 좁히는 첫 장면, 설계가 갈라지는 중간 장면, 검증이 닫히는 마지막 장면의 세 구간으로 나눈다. 각 구간은 코드와 CLI가 함께 등장해야 하고, 다음 phase로 넘어가는 질문이 문단 끝에 남아 있어야 한다.

## 최종 글의 흐름

1. 도입에서 `gcc -O1 -Wall -Werror -o test_bits test_bits.c ../src/bits.c && ./test_bits`와 현재 재작성 범위를 먼저 밝히고, 독자가 이 글이 어떤 evidence layer 위에 서 있는지 알게 한다.
2. 본문은 Phase 1 정수 퍼즐 contract를 mask 규칙으로 고정한다 -> Phase 2 float 문제를 '실수'가 아니라 bit pattern 변환으로 옮긴다 -> Phase 3 공식 boundary와 companion test를 한 번에 닫는다 순서로 간다. 순서를 바꾸지 않는 이유는 이 흐름이 README와 테스트가 실제로 요구하는 구현 순서에 가장 가깝기 때문이다.
3. 마지막에는 CLI excerpt와 남은 질문을 붙여, 이 프로젝트가 어디까지 닫혔고 어디가 다음 학습 포인트인지 분명하게 남긴다.

## 1. Phase 1 - 정수 퍼즐 contract를 mask 규칙으로 고정한다

이 구간의 중심 장면은 허용 연산자만으로도 `bitXor`, `isAsciiDigit`, `logicalNeg`, `howManyBits` 같은 퍼즐을 풀 수 있는 공통 패턴을 먼저 세운다.

본문에서는 먼저 값을 직접 계산하기보다 sign extension과 mask propagation을 잡으면 나머지 퍼즐도 같은 어휘로 설명될 것이라고 봤다. 그 다음 문단에서는 C/C++의 `bits.c` / `bits.cpp`에서 정수 퍼즐을 한 덩어리로 다루고, 각 함수가 '범위 검사'인지 '비트 전파'인지로 분류했다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `bitXor`, `isAsciiDigit`
- 붙일 CLI: `gcc -O1 -Wall -Werror -o test_bits test_bits.c ../src/bits.c && ./test_bits`
- 강조할 검증 신호: 정수 퍼즐 함수군이 한 파일에서 같은 제약으로 묶여 있어 구현 순서를 역추적할 수 있다.
- 장면이 끝날 때 남길 문장: float 퍼즐을 unsigned bit pattern 관점으로 분리한다.

## 2. Phase 2 - float 문제를 '실수'가 아니라 bit pattern 변환으로 옮긴다

이 구간의 중심 장면은 `floatScale2`, `floatFloat2Int`, `floatPower2`가 정수 퍼즐과 다른 규칙을 쓰기 때문에 별도 국면으로 다룬다.

본문에서는 먼저 IEEE754도 결국 sign/exponent/fraction 경계를 쪼개면 동일한 bit rewrite 문제로 다룰 수 있다고 가정했다. 그 다음 문단에서는 정수 연산 대신 exponent 조정, denormal 처리, overflow sentinel을 명시하는 쪽으로 구현을 옮겼다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `floatScale2`, `floatFloat2Int`
- 붙일 CLI: `gcc -O1 -Wall -Werror -o test_bits test_bits.c ../src/bits.c && ./test_bits`
- 강조할 검증 신호: `docs/concepts/float-boundaries.md`와 float 함수 묶음이 같은 학습 전환점을 보여 준다.
- 장면이 끝날 때 남길 문장: handout verifier와 self-owned edge-case test를 한 흐름으로 닫는다.

## 3. Phase 3 - 공식 boundary와 companion test를 한 번에 닫는다

이 구간의 중심 장면은 로컬 handout 검증과 companion edge-case test를 같이 붙이면 '정답처럼 보이는 구현'과 '계약을 통과한 구현'을 구분할 수 있다.

본문에서는 먼저 공식 verifier는 local-only이지만, 공개 트리에서는 `c/tests/test_bits.c`가 같은 경계값 사고를 다시 확인해 줄 것이라고 봤다. 그 다음 문단에서는 README의 검증 명령을 따라 `problem/`과 `c/tests/`를 분리하고, 공개 가능한 테스트 하네스를 별도 유지했다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `isAsciiDigit(0x30)`, `isAsciiDigit(0x39)`
- 붙일 CLI: `gcc -O1 -Wall -Werror -o test_bits test_bits.c ../src/bits.c && ./test_bits`
- 강조할 검증 신호: 실행 출력이 남아 있어 최종 검증 단계를 명확히 닫을 수 있다.
- 장면이 끝날 때 남길 문장: '퍼즐 풀이 모음'이 아니라 '계약을 단계적으로 좁힌 기록'으로 정리한다.

## Fixed CLI Anchor

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/datalab/c/tests && gcc -O1 -Wall -Werror -o test_bits test_bits.c ../src/bits.c && ./test_bits)
```

이 명령은 최종 글 마지막에서 README 계약이 여전히 살아 있다는 사실을 다시 확인하는 closing shot로 사용한다.
