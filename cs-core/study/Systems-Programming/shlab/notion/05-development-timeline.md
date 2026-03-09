# Shell Lab — 개발 타임라인

이 문서는 소스 코드에 드러나지 않는 개발 과정의 시간 순서, 사용한 CLI 명령, 환경 구축 절차를 기록한다.

---

## Phase 1: 문제 경계 정의

### problem/ 구성

공식 핸드아웃의 starter shell, trace 파일, Perl 드라이버를 재배포하지 않는 것으로 결정. `problem/`에는 계약만 남긴 공개 경계를 배치:
- `README.md` — 공식 과제의 요구사항 정리
- `Makefile` — `make status`로 현재 상태 확인
- `code/`, `data/`, `script/` — 최소한의 스캐폴딩

```bash
cd study/Systems-Programming/shlab/problem
make status
```

---

## Phase 2: C 트랙 — tsh 구현

### 스켈레톤 작성

- `c/include/tsh_helper.h` — `sio_puts()`, `sio_putl()` 시그널 안전 출력 함수
- `c/src/tsh.c` — 메인 루프, eval, 잡 테이블, 시그널 핸들러

### 핵심 구현 순서

1. `main()` + `parseline()` — 명령어 읽기/파싱
2. `eval()` — fork/exec + 내장 명령 판정
3. 잡 테이블 (`addjob`, `deletejob`, `fgpid`, `getjobpid`, `getjobjid`)
4. `sigchld_handler()` — waitpid 기반 자식 회수
5. `sigint_handler()`, `sigtstp_handler()` — 전경 잡 시그널 전달
6. fork/addjob 레이스 수정 — sigprocmask 보호
7. `waitfg()` — sigsuspend 기반 전경 대기
8. `do_bgfg()` — bg/fg 내장 명령

### 빌드 및 수동 테스트

```bash
cd study/Systems-Programming/shlab/c
make clean && make
./build/tsh
tsh> /bin/echo hello
tsh> /bin/sleep 3 &
tsh> jobs
tsh> quit
```

---

## Phase 3: 테스트 하네스 구축

### 공유 하네스 스크립트

`tests/direct_shell_case.sh` 작성 — FIFO 기반 쉘 직접 테스트:
- FIFO 파이프 생성 → 쉘 `-p` 모드 실행 → 명령어/시그널 주입 → 출력 캡처

### C 트랙 테스트 러너

`c/tests/run_tests.sh` — 네 가지 케이스 순차 실행:
1. `basic_echo`: `/bin/echo study-shell-basic` 실행 → 출력 확인
2. `bg_jobs`: 배경 잡 실행 → `jobs` 출력에 "Running" 확인
3. `sigint`: 전경 잡 실행 → `kill -INT` → "terminated by signal" 확인
4. `stop_fg`: 전경 잡 → `kill -TSTP` → `fg %1` → `kill -INT` → "stopped"와 "terminated" 모두 확인

### 실행

```bash
cd c
make clean && make test
```

---

## Phase 4: C++ 트랙

### 구현

C 트랙과 동일한 잡 컨트롤 로직을 C++ 스타일로 재구현:
- `std::array` 기반 잡 테이블
- `std::string` 기반 명령어 라인 처리
- 동일한 시그널 핸들러 구조 (POSIX API는 C/C++ 동일)

### 검증

```bash
cd study/Systems-Programming/shlab/cpp
make clean && make test
```

C 트랙과 동일한 테스트 케이스 전부 통과 확인.

---

## Phase 5: 문서 작성

### docs/ 구성

- `docs/concepts/signal-and-race-discipline.md` — fork/addjob 레이스, SIGCHLD 차단 규칙, 프로세스 그룹
- `docs/concepts/job-control-flow.md` — 내장 명령 흐름, sigsuspend 전경 대기
- `docs/references/verification.md` — 검증 명령, 테스트 커버리지, 현재 결과

---

## 의존성 요약

| 항목 | 내용 |
|---|---|
| 컴파일러 | gcc (C99 + `_POSIX_C_SOURCE=200809L`) |
| 빌드 | make |
| 테스트 | bash + FIFO (`mkfifo`) |
| POSIX API | `fork`, `execvp`, `waitpid`, `sigprocmask`, `sigsuspend`, `setpgid`, `kill` |
| 외부 의존성 | 없음 (Docker 불필요) |
| 공식 에셋 | 미사용 (starter shell, trace, driver 모두 제외) |
| 로컬 환경 | macOS (POSIX 호환) |
