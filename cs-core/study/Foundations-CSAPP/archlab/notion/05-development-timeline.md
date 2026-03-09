# Architecture Lab — 개발 타임라인

이 문서는 소스 코드에 드러나지 않는 개발 과정의 시간 순서, 사용한 CLI 명령, 환경 구축 절차를 기록한다.

---

## Phase 1: 환경 준비

### 공식 핸드아웃 복원

```bash
cd study/Foundations-CSAPP/archlab/problem
python3 ../../tools/restore_csapp_self_study_assets.py archlab
```

공식 Architecture Lab self-study 핸드아웃이 `problem/official/archlab-handout/`에 다운로드된다. 이 디렉토리는 `.gitignore`에 등록되어 로컬에만 존재한다.

### Docker 이미지 빌드

```bash
cd study/Foundations-CSAPP/archlab/problem
make docker-image
```

내부 동작:
```bash
docker build --platform linux/amd64 -t csapp-official-linux-amd64 \
  -f ../../tools/Dockerfile.csapp-official ../../../..
```

Dockerfile은 `debian:bookworm-slim` 기반으로 `gcc-multilib`, `make`, `flex`, `bison`, `gdb` 등을 포함한다. Apple Silicon에서 `--platform linux/amd64`으로 QEMU 에뮬레이션으로 실행된다.

### 시뮬레이터 빌드 확인

```bash
docker run --rm --platform linux/amd64 \
  -v "$REPO_ROOT:$REPO_ROOT" -w "$PWD" \
  csapp-official-linux-amd64 bash -lc \
  'cd official/archlab-handout/sim/misc && \
   make CFLAGS="-Wall -O1 -g -fcommon" LCFLAGS="-O1 -fcommon"'
```

`-fcommon` 플래그는 GCC 10+ 기본값 변경(`-fno-common`) 때문에 필수다. 이것 없이는 tentative definition 충돌로 링크 에러가 발생한다.

---

## Phase 2: Part A — Y86-64 어셈블리 작성

### 파일 작성

`y86/src/` 디렉토리에 세 개의 어셈블리 파일 작성:
- `sum.ys` — 반복 연결 리스트 합산
- `rsum.ys` — 재귀 연결 리스트 합산  
- `copy.ys` — 블록 복사 + XOR 체크섬

### 공식 검증

```bash
cd problem
make sync-official    # y86/src/*.ys를 official 트리로 복사
make verify-part-a    # Docker에서 yas + yis 실행
```

Docker 내부에서 실행되는 실제 명령:
```bash
cd sim/misc
./yas sum.ys && ./yis sum.yo | grep -Eq "%rax:.*0x0000000000000cba"
./yas rsum.ys && ./yis rsum.yo | grep -Eq "%rax:.*0x0000000000000cba"
./yas copy.ys && ./yis copy.yo | grep -Eq "%rax:.*0x0000000000000cba"
```

세 프로그램 모두 `%rax = 0xcba` 확인.

---

## Phase 3: Part B — iaddq HCL 패치

### 패치 스크립트 작성

`y86/script/apply_hcl_patches.py` 작성. SEQ용 `patch_seq()`와 PIPE용 `patch_pipe()` 함수를 분리해서, 각각의 HCL 파일에 8개의 치환을 적용한다.

### 공식 검증

```bash
cd problem
make sync-official    # HCL 패치도 적용됨
make verify-part-b    # Docker에서 ssim 빌드 + ptest
```

Docker 내부 동작:
```bash
cd sim/seq
make ssim VERSION=full GUIMODE= TKLIBS= TKINC= CFLAGS="-Wall -O2 -fcommon"
cd ../ptest
make SIM=../seq/ssim TFLAGS=-i
```

`ptest`가 `iaddq` 포함 전체 명령어 회귀 테스트 통과 확인.

---

## Phase 4: Part C — ncopy 최적화

### 최적화 과정

1. 기본 ncopy 구현 (원소당 ~9사이클)
2. 8-way 언롤링 적용
3. 양수 판정을 `cmovg` 패턴으로 분기 제거
4. 테일 디스패치를 폴스루 방식으로 구현

### 공식 검증

```bash
cd problem
make sync-official    # ncopy.ys를 pipe/ 디렉토리로 복사
make verify-part-c    # Docker에서 psim 빌드 + correctness + benchmark
```

Docker 내부 동작:
```bash
cd sim/pipe
make psim VERSION=full GUIMODE= TKLIBS= TKINC= CFLAGS="-Wall -O2 -fcommon"
make drivers
cd ../ptest
make SIM=../pipe/psim TFLAGS=-i   # iaddq 포함 회귀 테스트
cd ../pipe
./correctness.pl -f ncopy.ys      # 정확성 테스트
./benchmark.pl -f ncopy.ys        # CPE 벤치마크
```

결과: `Average CPE 9.16`, `Score 26.8/60.0`

---

## Phase 5: 컴패니언 모델 구현

### C 트랙

```bash
cd study/Foundations-CSAPP/archlab/c
make clean && make test
```

파일 구성:
- `include/mini_archlab.h` — 구조체 정의 (ArchNode, SeqIaddqTrace, NcopyReport)
- `src/mini_archlab.c` — Part A/B/C 핵심 로직
- `src/main.c` — 샘플 실행
- `tests/test_mini_archlab.c` — 단위 테스트

### C++ 트랙

```bash
cd study/Foundations-CSAPP/archlab/cpp
make clean && make test
```

C와 동일한 구조를 `archlab` 네임스페이스로 래핑. `std::vector` 사용.

---

## Phase 6: 전체 공식 검증

```bash
cd problem
make verify-official
```

이 명령은 `verify-part-a`, `verify-part-b`, `verify-part-c`를 순차 실행한다. 세 파트 모두 Docker 기반으로 실행되므로 로컬 환경에 의존하지 않는다.

---

## Phase 7: 문서 작성

### docs/ 작성

- `docs/concepts/part-split.md` — 세 파트의 이질성과 컴패니언 매핑 설명
- `docs/concepts/iaddq-and-control-signals.md` — 제어 신호 추론 과정
- `docs/concepts/pipeline-cost-model.md` — pseudo-CPE 근사 모델 설명
- `docs/references/verification.md` — 공식/컴패니언 검증 명령과 결과 정리

---

## 의존성 요약

| 항목 | 내용 |
|---|---|
| Docker 이미지 | `csapp-official-linux-amd64` (debian:bookworm-slim 기반) |
| 복원 스크립트 | `study/tools/restore_csapp_self_study_assets.py` |
| 추가 빌드 플래그 | `-fcommon` (GCC 10+ 호환) |
| 핸드아웃 위치 | `problem/official/archlab-handout/` (gitignored) |
| Y86-64 도구 | `yas`, `yis`, `ssim`, `psim`, `ptest`, `correctness.pl`, `benchmark.pl` |
| 로컬 환경 | macOS Apple Silicon + Docker Desktop (linux/amd64 QEMU 에뮬레이션) |
