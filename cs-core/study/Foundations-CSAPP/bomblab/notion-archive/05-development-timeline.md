# Bomb Lab — 개발 타임라인

## 이 문서의 목적

소스코드만으로는 추적할 수 없는 개발 과정의 전체 흐름을 기록한다. 공식 봄 리버스 엔지니어링과 미니 봄 구현 두 트랙의 작업 순서, 사용한 CLI, 설치한 도구, 결정의 맥락을 포함한다.

---

## Phase 0: 환경 준비

### 작업 환경

- **OS**: macOS (Apple Silicon, M시리즈)
- **컴파일러**: Xcode Command Line Tools (clang/gcc), C11/C++20
- **Docker**: Docker Desktop for Mac (ARM64), `--platform linux/amd64` 에뮬레이션
- **디버거**: Docker 내 `gdb` (공식 봄 분석용)
- **Python**: Python 3 (핸드아웃 복원 스크립트용)

### 디렉토리 구조 생성

레포 규칙에 따라 표준 구조를 준비했다:

```
bomblab/
  README.md
  problem/          ← 공식 과제 계약서, Makefile, 분석 스크립트
  c/                ← C companion 미니 봄
  cpp/              ← C++ companion 미니 봄
  docs/             ← 공개용 워크플로우/패턴 설명
  notion/           ← 비공개 프로세스 노트
```

### Docker 이미지 (Data Lab에서 재사용)

Data Lab에서 이미 빌드한 `csapp-official-linux-amd64` Docker 이미지를 그대로 사용했다. `gdb`가 포함되어 있어 공식 봄 분석에도 사용할 수 있다.

```bash
# 이미지가 없는 경우에만
cd problem
make docker-image
```

---

## Phase 1: 공식 봄 복원 및 리버스 엔지니어링

### 공식 셀프스터디 봄 다운로드

```bash
cd problem
make restore-official
```

이 명령은 `study/scripts/restore_csapp_self_study_assets.py`를 실행하여 `csapp.cs.cmu.edu`에서 `bomb.tar`를 다운로드하고 `problem/official/bomb/` 아래에 압축을 해제한다.

### 분석 파일 생성

```bash
cd problem
make disas       # objdump -d 결과 → bomb_disas.txt
make strings     # strings 결과 → bomb_strings.txt
make symbols     # nm 결과 → bomb_symbols.txt
```

이 파일들은 `.gitignore`에 포함되어 버전 관리에서 제외된다.

### gdb 분석 워크플로우

```bash
cd problem
# Docker 안에서 gdb 실행
docker run --rm -it --platform linux/amd64 \
  -v "$(pwd)/official/bomb:/work" \
  -w /work csapp-official-linux-amd64 \
  gdb ./bomb
```

gdb 세션 내 기본 명령 순서:
```
(gdb) break explode_bomb
(gdb) break phase_1
(gdb) run
(gdb) disas phase_1
(gdb) x/s [문자열 주소]
```

### 정답 파일 관리

각 페이즈의 정답을 `problem/data/solutions.txt`에 저장했다. 이 파일은 공식 셀프스터디 봄에 대한 것이므로 공개 가능하다.

### 공식 검증

```bash
cd problem
make verify-official
# 또는 수동
make test
```

Docker 안에서 봄 바이너리에 정답 파일을 넘겨 실행하고, 6개 페이즈 모두 "Phase N defused" 출력을 확인했다.

---

## Phase 2: C 미니 봄 구현

### 헤더 및 페이즈 함수 설계

`c/include/mini_bomb.h`에 7개 함수(6개 페이즈 + 시크릿)의 시그니처를 정의했다.

`c/src/mini_bomb.c`에 각 페이즈의 구현을 작성했다:

1. **Phase 1**: `strcmp`로 고정 문자열 비교
2. **Phase 2**: 6개 정수 파싱 → 첫 값 1 확인 → 각 값이 이전 값의 2배
3. **Phase 3**: 2개 정수 파싱 → `switch` 문으로 인덱스-값 매핑 검사
4. **Phase 4**: 2개 정수 파싱 → `func4` 재귀 호출 → 반환값과 두 번째 인자 검사
5. **Phase 5**: 6글자 문자열 → 각 글자 `& 0x0f` → 룩업 테이블 → 결과 비교
6. **Phase 6**: 6개 정수 → 중복/범위 검사 → `7-x` 변환 → 노드 재정렬 → 내림차순 검증
7. **Secret**: 정수 하나 → BST에서 `fun7` 실행 → 반환값 검사

### 메인 드라이버 작성

`c/src/main.c`에 파일 또는 stdin에서 한 줄씩 읽어 각 페이즈를 순차 실행하는 드라이버를 작성했다.

### 빌드 및 실행

```bash
cd c
make clean && make
# 정답 파일로 실행
printf 'Assembly reveals intent.\n1 2 4 8 16 32\n1 311\n6 6\n01234.\n4 6 2 3 5 1\n35\n' > /tmp/bomblab_c_answers.txt
./build/mini_bomb /tmp/bomblab_c_answers.txt
rm /tmp/bomblab_c_answers.txt
```

### 유닛 테스트 작성

`c/tests/test_mini_bomb.c`에 각 페이즈의 accept/reject 케이스를 작성했다:
- 정상 입력이 통과하는지
- 잘못된 입력이 거절되는지
- NULL 입력이 안전하게 처리되는지

```bash
cd c
make test
# 출력: C mini-bomb tests passed
```

---

## Phase 3: C++ 미니 봄 구현

### C와 동일한 구조로 C++ 작성

`cpp/src/mini_bomb.cpp`와 `cpp/src/main.cpp`에 C 구현과 동일한 로직을 C++ 스타일로 작성했다.

### 빌드 및 테스트

```bash
cd cpp
make clean && make test
printf 'Assembly reveals intent.\n1 2 4 8 16 32\n1 311\n6 6\n01234.\n4 6 2 3 5 1\n35\n' > /tmp/bomblab_cpp_answers.txt
./build/mini_bomb /tmp/bomblab_cpp_answers.txt
rm /tmp/bomblab_cpp_answers.txt
```

---

## Phase 4: 문서화

### docs/ 작성

- `docs/concepts/reverse-engineering-workflow.md` — 기본 분석 루프 (안전 브레이크 → 입력 계약 → 제어 흐름 분류 → 의사코드 → 검증)
- `docs/concepts/phase-patterns.md` — 페이즈 패밀리 분류와 인식 방법
- `docs/references/publication-policy.md` — 공개 가능/불가능 범위 정의
- `docs/references/verification.md` — 검증 명령어와 결과

### notion/ 작성

- `notion/00-problem-framing.md` — 과제 정의와 접근 전제
- `notion/01-approach-log.md` — 페이즈별 접근 과정
- `notion/02-debug-log.md` — 디버깅 과정과 교훈
- `notion/03-retrospective.md` — 회고
- `notion/04-knowledge-index.md` — 핵심 개념 인덱스
- `notion/05-development-timeline.md` — 이 문서

---

## 최종 검증 상태

| 검증 항목 | 결과 | 명령어 |
|---|---|---|
| 공식 셀프스터디 봄 (6 phases) | PASS | `make verify-official` |
| C 미니 봄 유닛 테스트 | PASS | `cd c && make test` |
| C 미니 봄 end-to-end (7 phases) | PASS | `./build/mini_bomb answers.txt` |
| C++ 미니 봄 유닛 테스트 | PASS | `cd cpp && make test` |
| C++ 미니 봄 end-to-end (7 phases) | PASS | `./build/mini_bomb answers.txt` |

---

## 사용된 도구 및 의존성 총정리

| 도구 | 용도 |
|---|---|
| macOS (Apple Silicon) | 개발 호스트 |
| Xcode CLT (clang) | C/C++ 컴파일 |
| Docker Desktop (ARM64) | 공식 봄 실행 및 분석 (linux/amd64 에뮬레이션) |
| debian:bookworm-slim | Docker 이미지 베이스 |
| gdb | 공식 봄 리버스 엔지니어링 |
| objdump | 디스어셈블리 생성 |
| strings | 바이너리 문자열 추출 |
| nm | 심볼 테이블 조회 |
| Python 3 | 핸드아웃 복원 스크립트 |
| GNU Make | 빌드 자동화 |
| Git | 버전 관리 |
