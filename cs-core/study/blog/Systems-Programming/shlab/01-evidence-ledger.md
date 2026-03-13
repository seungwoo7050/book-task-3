# Shell Lab Evidence Ledger

이 문서는 최종 글보다 한 단계 앞에 있는 근거 문서다. 기존 `blog/` 초안은 입력에서 제외했고, 지금 남아 있는 README, problem 설명, 구현 파일, 테스트, git history, 재실행한 CLI만으로 chronology를 다시 세웠다.

## 근거 묶음

`shlab`은 프로세스 그룹, foreground/background job control, `SIGCHLD` 처리, `fork` 주변 race를 작은 셸 구현으로 익히는 프로젝트다. 구현의 중심은 `c`, `cpp`에 퍼져 있고, 글에서 반복해서 참조할 핵심 파일은 `c/src/tsh.c`, `cpp/src/tsh.cpp`다. 검증 표면은 `tests/direct_shell_case.sh`, `c/tests/run_tests.sh`, `c/tests/traces/trace_bg_jobs.txt`, `c/tests/traces/trace_sigint.txt`, `c/tests/traces/trace_stop_fg.txt`, `cpp/tests/run_tests.sh`, `cpp/tests/traces/trace_bg_jobs.txt`, `cpp/tests/traces/trace_sigint.txt`와 `make clean && make test`에 걸쳐 있으며, 이번에 다시 붙잡은 개념 축은 `job control flow`, `signal and race discipline`이다.

## Git History Anchor

- `2026-03-09	b1cbad9	docs(notion): cs-core, network-atda`
- `2026-03-10	ced9d08	docs: enhance cs-core`
- `2026-03-11	bbb6673	Track 1에 대한 전반적인 개선 완료`
- `2026-03-13	abeead6	docs: TRACK 1 에대한 blog/ 작업 1차 완료`

## 1. Phase 1 - 파서, builtin, job table부터 고정한다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다. 이 시점의 목표는 tiny shell도 결국 먼저 필요한 것은 command surface와 job bookkeeping이다.

그때 세운 가설은 `eval`과 `parseline`이 흔들리면 foreground/background 구분조차 무의미해질 거라고 봤다. 실제 조치는 파서, builtin 분기, `addjob`/`clearjob` 같은 job table helper를 먼저 묶었다.

- 정리해 둔 근거:
- 변경 단위: `c/src/tsh.c`
- CLI: `make clean && make test`
- 검증 신호: job table helper가 남아 있어 signal reasoning을 뒤에서 덧붙일 수 있다.
- 새로 배운 것: 셸 구현의 출발점은 signal handler가 아니라 '지금 무엇을 실행하려는가'를 안정적으로 기록하는 일이다.

### 코드 앵커 — `eval` (`c/src/tsh.c:106`)

```c
static void eval(char *cmdline)
{
    char *argv[MAXARGS];
    int bg = parseline(cmdline, argv);
    pid_t pid;
    sigset_t mask_child;
    sigset_t mask_all;
    sigset_t prev;
```

이 조각은 job table helper가 남아 있어 signal reasoning을 뒤에서 덧붙일 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `Eval`를 읽고 나면 다음 장면이 왜 foreground wait와 signal forwarding으로 이동한다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `Builtin_Cmd` (`c/src/tsh.c:119`)

```c
    if (builtin_cmd(argv)) {
        return;
    }

    sigemptyset(&mask_child);
    sigaddset(&mask_child, SIGCHLD);
    sigfillset(&mask_all);
```

이 조각은 job table helper가 남아 있어 signal reasoning을 뒤에서 덧붙일 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `Builtin_Cmd`를 읽고 나면 다음 장면이 왜 foreground wait와 signal forwarding으로 이동한다로 이어지는지도 한 번에 보인다.

다음 단계에서는 foreground wait와 signal forwarding으로 이동한다.

## 2. Phase 2 - `waitfg`와 signal handler에서 race discipline을 고정한다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다. 이 시점의 목표는 `waitfg`, `sigchld_handler`, `sigint_handler`, `sigtstp_handler`는 shell의 실제 난점이 어디인지 드러내는 함수들이다.

그때 세운 가설은 문제의 중심은 명령 실행 자체가 아니라 `fork` 주변 마스킹 순서와 job state 전이일 것이라고 판단했다. 실제 조치는 signal handler와 foreground wait를 분리하고, docs에서 job control flow와 race discipline을 설명하는 구조로 정리했다.

- 정리해 둔 근거:
- 변경 단위: `c/src/tsh.c`
- CLI: `make clean && make test`
- 검증 신호: 핵심 race가 함수 수준으로 드러나 있어 블로그에서도 판단 전환점을 분명히 보여 줄 수 있다.
- 새로 배운 것: process group과 signal forwarding은 API 호출 목록보다 상태 전이 순서를 맞추는 일이었다.

### 코드 앵커 — `waitfg` (`c/src/tsh.c:221`)

```c
static void waitfg(pid_t pid)
{
    sigset_t empty;

    sigemptyset(&empty);
    while (fgpid(jobs) == pid) {
        sigsuspend(&empty);
    }
}
```

이 조각은 핵심 race가 함수 수준으로 드러나 있어 블로그에서도 판단 전환점을 분명히 보여 줄 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `Waitfg`를 읽고 나면 다음 장면이 왜 trace와 direct-shell case로 동작을 닫는다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `sigchld_handler` (`c/src/tsh.c:231`)

```c
static void sigchld_handler(int sig)
{
    int olderrno = errno;
    int status;
    pid_t pid;
```

이 조각은 핵심 race가 함수 수준으로 드러나 있어 블로그에서도 판단 전환점을 분명히 보여 줄 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `Sigchld_Handler`를 읽고 나면 다음 장면이 왜 trace와 direct-shell case로 동작을 닫는다로 이어지는지도 한 번에 보인다.

다음 단계에서는 trace와 direct-shell case로 동작을 닫는다.

## 3. Phase 3 - trace와 direct shell case로 shell contract를 닫는다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다. 이 시점의 목표는 shell은 한두 개의 unit test보다 trace sequence가 더 많은 것을 말해 준다.

그때 세운 가설은 공식 trace 없이도 self-owned trace와 `direct_shell_case.sh`가 있으면 핵심 job-control contract를 재현할 수 있다고 봤다. 실제 조치는 `tests/`와 `c/tests/run_tests.sh`를 중심으로 foreground stop, bg jobs, SIGINT 시나리오를 다시 확인하게 만들었다.

- 정리해 둔 근거:
- 변경 단위: `c/tests/traces/trace_stop_fg.txt`, `tests/direct_shell_case.sh`
- CLI: `make clean && make test`
- 검증 신호: 현재 테스트 출력이 마지막 단계의 닫힘을 명확히 보여 준다.
- 새로 배운 것: 시스템 프로그램은 단발성 성공보다 상태 전이 시나리오를 재생할 수 있는 테스트가 더 중요했다.

### 코드 앵커 — `$SHELL_PATH` (`tests/direct_shell_case.sh:8`)

```bash
if [[ "$SHELL_PATH" != /* ]]; then
    SHELL_PATH="$(cd "$(dirname "$SHELL_PATH")" && pwd)/$(basename "$SHELL_PATH")"
fi

TMP_DIR="$(mktemp -d)"
SHELL_PID=""
INPUT_FD_OPEN=0
```

이 조각은 현재 테스트 출력이 마지막 단계의 닫힘을 명확히 보여 준다는 설명이 실제로 어디서 나오는지 보여 준다. `$SHELL_PATH`를 읽고 나면 다음 장면이 왜 shell surface -> race discipline -> trace verification 순서를 유지한다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `C` (`c/tests/traces/trace_stop_fg.txt:13`)

```text
CLOSE
```

이 조각은 현재 테스트 출력이 마지막 단계의 닫힘을 명확히 보여 준다는 설명이 실제로 어디서 나오는지 보여 준다. `C`를 읽고 나면 다음 장면이 왜 shell surface -> race discipline -> trace verification 순서를 유지한다로 이어지는지도 한 번에 보인다.

다음 단계에서는 shell surface -> race discipline -> trace verification 순서를 유지한다.

## Latest CLI Excerpt

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/shlab/c && make clean && make test)
```

```text
C shlab tests passed
bash tests/run_tests.sh ./build/tsh
```
