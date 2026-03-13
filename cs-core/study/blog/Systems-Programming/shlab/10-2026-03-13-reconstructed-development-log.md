# Shell Lab 재구성 개발 로그

`shlab`은 프로세스 그룹, foreground/background job control, `SIGCHLD` 처리, `fork` 주변 race를 작은 셸 구현으로 익히는 프로젝트다.

2026-03-13에 기존 초안을 `_legacy`로 격리한 뒤, `README`, `problem/`, 실제 구현 파일, `docs/`, 테스트, 현재 다시 실행한 CLI만으로 이 글을 다시 썼다. 그래서 아래 서사는 나중에 답을 알고 난 뒤 매끈하게 정리한 회고가 아니라, 남아 있는 증거를 따라 다시 세운 개발 흐름에 가깝다.

## 이 프로젝트를 다시 읽는 순서

command parsing과 builtin에서 출발해, `SIGCHLD`/`waitfg` race discipline이 왜 마지막 병목이 되는지 따라간다. 이 질문이 너무 빨리 추상적으로 흘러가지 않도록, 글은 세 개의 phase로 나눠 진행한다.

- Phase 1: 파서, builtin, job table부터 고정한다 — `c/src/tsh.c`
- Phase 2: `waitfg`와 signal handler에서 race discipline을 고정한다 — `c/src/tsh.c`
- Phase 3: trace와 direct shell case로 shell contract를 닫는다 — `c/tests/traces/trace_stop_fg.txt`, `tests/direct_shell_case.sh`

## Phase 1. 파서, builtin, job table부터 고정한다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다.

이 시점의 목표는 tiny shell도 결국 먼저 필요한 것은 command surface와 job bookkeeping이다.

처음에는 `eval`과 `parseline`이 흔들리면 foreground/background 구분조차 무의미해질 거라고 봤다. 그런데 실제로 글의 중심이 된 조치는 파서, builtin 분기, `addjob`/`clearjob` 같은 job table helper를 먼저 묶었다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/src/tsh.c`
- CLI: `make clean && make test`
- 검증 신호: job table helper가 남아 있어 signal reasoning을 뒤에서 덧붙일 수 있다.

### 이 장면을 고정하는 코드 — `eval` (`c/src/tsh.c:106`)

이 단계에서 가장 먼저 붙잡아야 하는 코드는 아래 조각이다.

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

`Eval`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 셸 구현의 출발점은 signal handler가 아니라 '지금 무엇을 실행하려는가'를 안정적으로 기록하는 일이다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 foreground wait와 signal forwarding으로 이동한다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 셸 구현의 출발점은 signal handler가 아니라 '지금 무엇을 실행하려는가'를 안정적으로 기록하는 일이다.

그래서 다음 장면에서는 foreground wait와 signal forwarding으로 이동한다.

## Phase 2. `waitfg`와 signal handler에서 race discipline을 고정한다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다.

이 시점의 목표는 `waitfg`, `sigchld_handler`, `sigint_handler`, `sigtstp_handler`는 shell의 실제 난점이 어디인지 드러내는 함수들이다.

처음에는 문제의 중심은 명령 실행 자체가 아니라 `fork` 주변 마스킹 순서와 job state 전이일 것이라고 판단했다. 그런데 실제로 글의 중심이 된 조치는 signal handler와 foreground wait를 분리하고, docs에서 job control flow와 race discipline을 설명하는 구조로 정리했다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/src/tsh.c`
- CLI: `make clean && make test`
- 검증 신호: 핵심 race가 함수 수준으로 드러나 있어 블로그에서도 판단 전환점을 분명히 보여 줄 수 있다.

### 이 장면을 고정하는 코드 — `waitfg` (`c/src/tsh.c:221`)

판단이 뒤집히는 지점은 결국 이 구현 세부에서 드러난다.

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

`Waitfg`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 process group과 signal forwarding은 api 호출 목록보다 상태 전이 순서를 맞추는 일이었다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 trace와 direct-shell case로 동작을 닫는다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 process group과 signal forwarding은 API 호출 목록보다 상태 전이 순서를 맞추는 일이었다.

그래서 다음 장면에서는 trace와 direct-shell case로 동작을 닫는다.

## Phase 3. trace와 direct shell case로 shell contract를 닫는다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다.

이 시점의 목표는 shell은 한두 개의 unit test보다 trace sequence가 더 많은 것을 말해 준다.

처음에는 공식 trace 없이도 self-owned trace와 `direct_shell_case.sh`가 있으면 핵심 job-control contract를 재현할 수 있다고 봤다. 그런데 실제로 글의 중심이 된 조치는 `tests/`와 `c/tests/run_tests.sh`를 중심으로 foreground stop, bg jobs, SIGINT 시나리오를 다시 확인하게 만들었다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/tests/traces/trace_stop_fg.txt`, `tests/direct_shell_case.sh`
- CLI: `make clean && make test`
- 검증 신호: 현재 테스트 출력이 마지막 단계의 닫힘을 명확히 보여 준다.

### 이 장면을 고정하는 코드 — `$SHELL_PATH` (`tests/direct_shell_case.sh:8`)

끝을 닫는 순간은 늘 테스트나 CLI 쪽 코드가 더 솔직하게 보여 준다.

```bash
if [[ "$SHELL_PATH" != /* ]]; then
    SHELL_PATH="$(cd "$(dirname "$SHELL_PATH")" && pwd)/$(basename "$SHELL_PATH")"
fi

TMP_DIR="$(mktemp -d)"
SHELL_PID=""
INPUT_FD_OPEN=0
```

`$SHELL_PATH`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 시스템 프로그램은 단발성 성공보다 상태 전이 시나리오를 재생할 수 있는 테스트가 더 중요했다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 shell surface -> race discipline -> trace verification 순서를 유지한다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 시스템 프로그램은 단발성 성공보다 상태 전이 시나리오를 재생할 수 있는 테스트가 더 중요했다.

그래서 다음 장면에서는 shell surface -> race discipline -> trace verification 순서를 유지한다.

## CLI로 다시 닫기

문장과 코드만으로는 마지막 닫힘이 약해질 수 있어서, 저장소에서 다시 실행 가능한 대표 명령을 마지막에 그대로 남긴다. 이 출력은 기능이 돌아간다는 사실뿐 아니라 README가 약속한 검증 entrypoint가 아직 살아 있다는 사실까지 함께 보여 준다.

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/shlab/c && make clean && make test)
```

```text
C shlab tests passed
bash tests/run_tests.sh ./build/tsh
```

## 이번에 남은 질문

- 개념 축: `job control flow`, `signal and race discipline`
- 대표 테스트/fixture: `tests/direct_shell_case.sh`, `c/tests/run_tests.sh`, `c/tests/traces/trace_bg_jobs.txt`, `c/tests/traces/trace_sigint.txt`, `c/tests/traces/trace_stop_fg.txt`, `cpp/tests/run_tests.sh`
- 다음 질문: 최종 글은 shell surface -> race discipline -> trace verification 순서를 유지한다.
