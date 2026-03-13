# Foundations-CSAPP 블로그 트랙

CS:APP 계열 lab들을 source-first chronology로 다시 읽는 트랙이다. bit puzzle, Y86, reverse engineering, cache-aware optimization처럼 표면은 달라도 결국은 문제 계약을 검증 가능한 코드와 companion test로 번역하는 과정이 중심이 된다.

이 트랙의 문서는 모두 같은 원칙을 따른다. 프로젝트별 `00-series-map.md`에서 읽는 순서를 잡고, `01-evidence-ledger.md`에서 근거를 확인한 뒤, `_structure-outline.md`와 최종 blog로 넘어간다. `_legacy`는 비교용 보관소일 뿐 현재 시리즈의 입력 근거가 아니다.

## 프로젝트 가이드

### [Architecture Lab](archlab/)

`archlab`은 Y86-64 프로그램 작성, 제어 로직 구현, 파이프라인 성능 개선을 한 흐름으로 묶는 프로젝트다.

- 시리즈 입구: [archlab/00-series-map.md](archlab/00-series-map.md)
- 핵심 질문: Y86 프로그램, `iaddq` 제어 로직, `ncopy` 성능 개선이 왜 세 개의 다른 문제처럼 느껴지는지 코드 순서로 복원한다.
- 대표 검증 명령: `make clean && make test`

### [Attack Lab](attacklab/)

`attacklab`은 stack layout, code injection, ROP, 상대 주소 계산을 단계적으로 익히는 프로젝트다.

- 시리즈 입구: [attacklab/00-series-map.md](attacklab/00-series-map.md)
- 핵심 질문: hex payload를 읽는 표면부터 phase validator까지 이어 붙여, code injection/ROP를 raw exploit dump가 아닌 재현 가능한 companion lab로 재구성한 흐름을 다룬다.
- 대표 검증 명령: `make clean && make test`

### [Bomb Lab](bomblab/)

`bomblab`은 x86-64 bomb를 brute force가 아니라 해석 절차로 풀어 가는 프로젝트다.

- 시리즈 입구: [bomblab/00-series-map.md](bomblab/00-series-map.md)
- 핵심 질문: phase별 입력 조건을 brute force 대신 해석 절차로 옮기고, 그 해석이 테스트 가능한 mini bomb로 바뀌는 흐름을 복원한다.
- 대표 검증 명령: `make clean && make test`

### [Data Lab](datalab/)

`datalab`은 bit-level 제약을 지키면서 정수 표현과 부동소수점 경계를 직접 구현하는 프로젝트다.

- 시리즈 입구: [datalab/00-series-map.md](datalab/00-series-map.md)
- 핵심 질문: 정수 퍼즐에서 mask와 sign bit를 먼저 고정하고, 그 다음 float bit pattern으로 넘어가는 흐름을 복원한다.
- 대표 검증 명령: `gcc -O1 -Wall -Werror -o test_bits test_bits.c ../src/bits.c && ./test_bits`

### [Performance Lab](perflab/)

`perflab`은 cache simulator와 transpose 최적화를 통해 "왜 더 빠른가"를 코드와 지표로 설명하는 프로젝트다.

- 시리즈 입구: [perflab/00-series-map.md](perflab/00-series-map.md)
- 핵심 질문: cache simulator와 transpose 최적화를 따로 떼지 않고, 같은 cost model을 두 개의 다른 구현 표면에 배치한 흐름으로 복원한다.
- 대표 검증 명령: `make clean && make test`

## 공통 문서 구조

- `00-series-map.md` — 왜 이 프로젝트를 이런 순서로 읽어야 하는지 설명하는 입구
- `01-evidence-ledger.md` — source-first 근거와 phase별 코드/CLI 앵커를 모아 둔 문서
- `_structure-outline.md` — 최종 글의 장면 배치와 전환 문장을 정리한 편집 메모
- `10-2026-03-13-reconstructed-development-log.md` — 구현 순서와 검증 신호를 하나의 서사로 다시 쓴 최종 blog
