# Shell Lab — 접근 기록

## eval() — 명령어 평가의 전체 흐름

### 파싱부터 실행까지

쉘의 핵심 루프는 단순하다: 한 줄 읽고, `parseline()`으로 인자 배열을 만들고, `eval()`에 넘긴다. `eval()` 안에서 내장 명령인지 확인하고, 아니면 `fork` + `execvp`로 외부 명령을 실행한다.

배경 실행 여부는 `parseline()`이 `&` 토큰을 발견했는지로 결정된다. 전경이면 `waitfg()`로 완료를 기다리고, 배경이면 잡 정보를 출력하고 즉시 반환한다.

### fork/addjob 사이의 레이스 제거

이 프로젝트에서 가장 중요한 코드 패턴은 다음과 같다:

```c
sigprocmask(SIG_BLOCK, &mask_child, &prev);  // SIGCHLD 차단
pid = fork();
if (pid == 0) {
    sigprocmask(SIG_SETMASK, &prev, NULL);    // 자식에서 복원
    setpgid(0, 0);
    execvp(argv[0], argv);
    _exit(1);
}
sigprocmask(SIG_BLOCK, &mask_all, NULL);      // 잡 테이블 보호
addjob(jobs, pid, bg ? BG : FG, cmdline);
sigprocmask(SIG_SETMASK, &prev, NULL);        // 원래 마스크 복원
```

이 순서가 아니면 레이스가 발생한다. 핵심은:
1. `fork()` 전에 `SIGCHLD`를 차단 — 자식이 즉시 종료해도 핸들러가 실행되지 않음
2. 자식에서 시그널 마스크 복원 — 자식은 부모의 차단 상태를 물려받으므로 복원 필수
3. `addjob()` 완료 후 마스크 복원 — 이제 핸들러가 안전하게 잡을 삭제할 수 있음

## 시그널 핸들러 설계

### SIGCHLD — 자식 회수

`sigchld_handler()`의 핵심은 `waitpid(-1, &status, WNOHANG | WUNTRACED)`다.

- `WNOHANG`: 회수할 자식이 없으면 즉시 반환 (핸들러가 블록되면 안 됨)
- `WUNTRACED`: 정지된 자식도 보고 (SIGTSTP으로 정지된 잡을 감지)
- `while` 루프: 동시에 여러 자식이 종료할 수 있으므로, 더 이상 회수할 것이 없을 때까지 반복

상태 판정 세 가지:
- `WIFEXITED`: 정상 종료 → 잡 삭제
- `WIFSIGNALED`: 시그널에 의한 종료 → 메시지 출력 + 잡 삭제
- `WIFSTOPPED`: 정지 → 잡 상태를 ST로 변경

### SIGINT/SIGTSTP — 전경 잡에 전달

```c
pid_t pid = fgpid(jobs);
if (pid > 0) {
    kill(-pid, sig);  // 프로세스 그룹 전체에 전달
}
```

`kill(-pid, sig)`에서 마이너스 부호가 핵심이다. `setpgid(0, 0)`으로 자식을 별도 프로세스 그룹에 넣었으므로, 그 그룹 전체에 시그널이 전달된다. 쉘 자신에게는 전달되지 않는다.

`errno` 보존도 중요하다. 시그널 핸들러가 다른 시스템 콜의 `errno`를 덮어쓰면, 호출자가 잘못된 에러를 보게 된다.

## 전경 대기 — sigsuspend 패턴

```c
void waitfg(pid_t pid) {
    sigset_t empty;
    sigemptyset(&empty);
    while (fgpid(jobs) == pid) {
        sigsuspend(&empty);
    }
}
```

이 패턴이 `waitpid`보다 나은 이유: `SIGCHLD` 핸들러가 잡 테이블을 갱신하므로, 전경 대기는 잡 테이블 상태만 확인하면 된다. `sigsuspend`는 시그널이 도착할 때까지 원자적으로 대기하고, 시그널 핸들러 실행 후 반환한다. 바쁜 대기(busy wait)를 피하면서도 시그널과의 레이스를 방지한다.

## 내장 명령 — bg/fg

`do_bgfg()`는 PID 또는 `%jobid` 형식의 인자를 파싱해서 잡을 찾고, `SIGCONT`를 보내서 재개한다.

- `bg`: 잡 상태를 BG로 변경, 잡 정보 출력, 즉시 반환
- `fg`: 잡 상태를 FG로 변경, `waitfg()`로 완료 대기

`SIGCONT`는 `kill(-job->pid, SIGCONT)`로 프로세스 그룹 전체에 보낸다.

## 시그널 안전 출력

핸들러에서 `printf`를 쓸 수 없으므로, `sio_puts()`와 `sio_putl()`을 직접 구현했다.

- `sio_puts()`: `write(STDOUT_FILENO, s, strlen(s))`
- `sio_putl()`: 정수를 문자열로 변환 후 `write()`

둘 다 async-signal-safe하다. `write()`는 POSIX에서 시그널 안전 함수 목록에 포함된다.

## 테스트 하네스 설계

공식 trace/driver 없이 검증하기 위해 FIFO 기반 직접 하네스를 만들었다:

1. FIFO 파이프 생성
2. 쉘을 `-p`(프롬프트 없음) 모드로 FIFO 입력과 함께 실행
3. 명령어를 FIFO에 쓰고, 적절한 타이밍에 시그널 전송
4. 출력을 파일로 캡처해서 `grep`으로 기대 문자열 확인

네 가지 테스트 케이스: `basic_echo`, `bg_jobs`, `sigint`, `stop_fg`.
