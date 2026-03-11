# Data Lab — 개발 타임라인

## 이 문서의 목적

소스코드만으로는 추적할 수 없는 개발 과정의 전체 흐름을 기록한다. 어떤 순서로 작업했고, 어떤 CLI를 실행했고, 어떤 도구를 설치했고, 어떤 시점에 어떤 결정을 내렸는지를 포함한다. 시간이 지난 뒤 이 과제를 재현하거나 맥락을 복원할 때 소스코드와 함께 참조하는 문서다.

---

## Phase 0: 환경 준비

### 작업 환경

- **OS**: macOS (Apple Silicon, M시리즈)
- **컴파일러**: Xcode Command Line Tools에 포함된 `clang` (gcc symlink)
- **C++ 표준**: C++20 (`-std=c++20`)
- **Docker**: Docker Desktop for Mac (ARM64), `--platform linux/amd64` 에뮬레이션 사용
- **Python**: Python 3 (핸드아웃 복원 스크립트 실행용)

### 프로젝트 디렉토리 구조 생성

레포 규칙에 따라 `datalab/` 아래에 표준 디렉토리 구조를 준비했다:

```
datalab/
  README.md
  problem/          ← 공식 과제 계약서, Makefile, 검증 스크립트
  c/                ← C 솔루션 트랙
  cpp/              ← C++ 솔루션 트랙
  docs/             ← 공개용 설명 문서
  notion/           ← 비공개 프로세스 노트 (이 문서들)
```

### 공식 핸드아웃 복원

CMU 공식 셀프스터디 핸드아웃을 로컬에 받아왔다. 이 핸드아웃에는 `dlc`(연산자 합법성 검사기)와 `btest`(정확성 테스트 하네스)의 소스 및 바이너리가 포함되어 있다.

```bash
cd study/Foundations-CSAPP/datalab/problem
make restore-official
```

이 명령은 내부적으로 `study/scripts/restore_csapp_self_study_assets.py` 스크립트를 실행하여 `csapp.cs.cmu.edu`에서 `datalab-handout.tar`를 다운로드하고 `problem/official/datalab-handout/` 디렉토리에 압축을 해제한다.

---

## Phase 1: 문제 계약서 파악

### problem/ 디렉토리 세팅

`problem/code/bits.c`는 CMU가 제공하는 스켈레톤 파일로, 13개 함수의 시그니처와 제약 조건이 주석으로 명시되어 있다. 이 파일의 주석이 곧 과제의 계약서다.

```bash
# 스켈레톤 파일 확인
cat problem/code/bits.c
```

과제 테이블을 `problem/README.md`에 정리했다: 13개 함수, 각각의 난이도(1~4), 허용 연산자, 최대 연산자 수.

### btest 빌드 확인 (로컬)

```bash
cd problem
make clean && make
```

Apple Silicon에서 `-m32` 플래그 에러가 발생했다. Makefile에 아키텍처 감지 분기를 추가하여 해결:

```makefile
ifeq ($(UNAME_S),Darwin)
ifeq ($(UNAME_M),arm64)
ARCH_FLAGS :=
endif
endif
```

---

## Phase 2: C 솔루션 작성

### 정수 퍼즐 (#1–#10) 구현 순서

문제 번호 순서대로 풀었다. 각 함수를 `c/src/bits.c`에 작성했다.

1. **`bitXor`** — 드모르간 법칙 적용. `~(~(x & ~y) & ~(~x & y))`
2. **`tmin`** — `1 << 31`. 즉시 완료.
3. **`isTmax`** — 첫 시도에서 -1 false positive 발견, `!!y` 가드 추가
4. **`allOddBits`** — 0xAA를 시프트와 OR로 0xAAAAAAAA 생성
5. **`negate`** — `~x + 1`. INT_MIN 오버플로우 동작 확인
6. **`isAsciiDigit`** — 범위 [0x30, 0x39] 검사를 두 개의 뺄셈 부호 비트로
7. **`conditional`** — 부울-마스크 변환 패턴 첫 사용
8. **`isLessOrEqual`** — 오버플로우 문제 발견 → 부호 분리 로직으로 수정
9. **`logicalNeg`** — `(x | (~x + 1)) >> 31` 패턴
10. **`howManyBits`** — 가장 오래 걸림. 연산자 수 제한(90)에 맞추기 위해 이진 탐색 패턴 도출

### 부동소수점 퍼즐 (#11–#13) 구현

11. **`floatScale2`** — 입력 분류(NaN/∞, 비정규, 정규) 후 분기 처리
12. **`floatFloat2Int`** — exp > 30 경계 발견까지 여러 번 수정
13. **`floatPower2`** — 비정규 범위 `1 << (x + 149)` 식 도출

---

## Phase 3: C 솔루션 검증

### 로컬 btest 실행

```bash
cd problem
cp ../c/src/bits.c code/bits.c
make clean && make
make test
```

### 엣지케이스 테스트 작성 및 실행

`btest`의 랜덤 벡터만으로는 경계값을 놓칠 수 있어서, 별도 테스트 파일 `c/tests/test_bits.c`를 작성했다.

```bash
cd c/tests
gcc -O1 -Wall -Werror -o test_bits test_bits.c ../src/bits.c
./test_bits
# 출력: === 55 / 55 edge-case tests passed ===
```

### Docker 검증 이미지 빌드

`dlc`가 Linux/amd64 ELF 바이너리이므로, macOS에서 실행하기 위해 Docker 이미지를 빌드했다.

```bash
cd problem
make docker-image
```

이 명령은 `study/scripts/Dockerfile.csapp-official`을 사용하여 `debian:bookworm-slim` 기반 이미지를 빌드한다. 설치되는 핵심 패키지:

- `gcc`, `gcc-multilib` — 32비트 크로스 컴파일
- `libc6-dev-i386` — 32비트 C 런타임
- `make`, `flex`, `bison` — 빌드 도구
- `perl` — 일부 CMU 스크립트 의존

### 공식 dlc + btest 검증

```bash
cd problem
make verify-official
```

이 타겟은:
1. `c/src/bits.c`를 `official/datalab-handout/bits.c`로 복사
2. Docker 컨테이너 안에서 `make clean && make && ./dlc bits.c && ./btest -T 20` 실행

첫 실행에서 `btest` 타임아웃 발생(`-T 10` 기본값). QEMU 에뮬레이션 오버헤드 때문. `-T 20`으로 수정하여 해결.

### 채점 스크립트 실행

```bash
cd problem
bash script/grade.sh
```

`grade.sh`는 `dlc` + `btest`를 순차 실행하고 결과를 컬러 출력한다.

---

## Phase 4: C++ 트랙 작성

### C++ 솔루션 미러링

C 솔루션과 동일한 로직을 `cpp/src/bits.cpp`에 새로 작성했다. 레거시 코드를 복사하지 않고 처음부터 다시 작성하는 것이 레포 규칙이다.

### C++ 테스트 작성 및 실행

`cpp/tests/test_bits.cpp`에 C 테스트와 동일한 55개 엣지케이스를 C++ 스타일로 작성했다.

```bash
cd cpp/tests
g++ -std=c++20 -O1 -Wall -Werror -o test_bits_cpp test_bits.cpp ../src/bits.cpp
./test_bits_cpp
# 출력: === 55 / 55 C++ edge-case tests passed ===
```

---

## Phase 5: 문서화

### docs/ 작성

공개용 설명 문서를 세 파일로 나누어 작성했다:

- `docs/concepts/integer-patterns.md` — 정수 퍼즐에서 반복되는 패턴 (부울-마스크, 2의 보수 뺄셈, 이진 탐색)
- `docs/concepts/float-boundaries.md` — 부동소수점 퍼즐의 분류 규칙과 경계값
- `docs/references/verification.md` — 검증 명령어와 현재 결과

### notion/ 작성

프로세스 기록 문서를 작성했다:

- `notion/00-problem-framing.md` — 과제 정의, 제약 조건, 환경 전제
- `notion/01-approach-log.md` — 풀이 접근 방식과 주요 발견
- `notion/02-debug-log.md` — 디버깅 과정과 교훈
- `notion/03-retrospective.md` — 회고
- `notion/04-knowledge-index.md` — 핵심 개념 인덱스
- `notion/05-development-timeline.md` — 이 문서 (개발 전체 타임라인)

---

## 최종 검증 상태

| 검증 항목 | 결과 | 명령어 |
|---|---|---|
| dlc (연산자 합법성) | PASS | `make verify-official` |
| btest (정확성, -T 20) | PASS | `make verify-official` |
| C 엣지케이스 (55개) | PASS | `cd c/tests && gcc ... && ./test_bits` |
| C++ 엣지케이스 (55개) | PASS | `cd cpp/tests && g++ ... && ./test_bits_cpp` |
| grade.sh | ALL TESTS PASSED | `bash script/grade.sh` |

---

## 사용된 도구 및 의존성 총정리

| 도구 | 버전/출처 | 용도 |
|---|---|---|
| macOS (Apple Silicon) | M시리즈 | 개발 호스트 OS |
| Xcode CLT (clang) | 시스템 기본 | C/C++ 컴파일 |
| Docker Desktop | ARM64 + QEMU | 크로스 플랫폼 검증 |
| debian:bookworm-slim | Docker 이미지 | 검증 컨테이너 베이스 |
| gcc-multilib | apt | 32비트 크로스 컴파일 |
| libc6-dev-i386 | apt | 32비트 C 런타임 |
| flex, bison | apt | dlc 빌드 의존 |
| Python 3 | 시스템 | 핸드아웃 복원 스크립트 |
| GNU Make | 시스템 | 빌드 자동화 |
| Git | 시스템 | 버전 관리 |
