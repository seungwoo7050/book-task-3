# Shell Lab — 지식 인덱스

## 프로세스 제어

### fork/exec 모델
- `fork()`: 현재 프로세스를 복제. 반환값으로 부모/자식 구분 (부모: 자식 PID, 자식: 0)
- `execvp()`: 현재 프로세스 이미지를 새 프로그램으로 교체. PATH 검색 포함
- `_exit()`: 자식에서 `execvp` 실패 시 사용. `exit()`는 버퍼 플러시 등 부작용 있음

### waitpid() 옵션

| 옵션 | 의미 |
|---|---|
| `WNOHANG` | 회수할 자식이 없으면 즉시 반환 (0 반환) |
| `WUNTRACED` | 정지된 자식도 보고 |
| `WNOHANG \| WUNTRACED` | 핸들러에서 사용: 비블로킹 + 정지 감지 |

### 상태 매크로

| 매크로 | 의미 |
|---|---|
| `WIFEXITED(status)` | 정상 종료 (`exit()` 또는 `return`) |
| `WIFSIGNALED(status)` | 시그널에 의한 종료 |
| `WIFSTOPPED(status)` | 정지 (`SIGTSTP`, `SIGSTOP`) |
| `WTERMSIG(status)` | 종료시킨 시그널 번호 |
| `WSTOPSIG(status)` | 정지시킨 시그널 번호 |

### setpgid(0, 0)
- 자식 프로세스를 자신의 PID와 같은 새 프로세스 그룹에 배치
- 쉘이 Ctrl-C를 받아도 자식 그룹에만 전달 가능
- `kill(-pid, sig)`: 마이너스 PID로 프로세스 그룹 전체에 시그널 전달

## 시그널

### 핵심 시그널

| 시그널 | 번호 | 기본 동작 | 쉘에서의 역할 |
|---|---|---|---|
| `SIGINT` | 2 | 종료 | Ctrl-C → 전경 잡에 전달 |
| `SIGTSTP` | 20 (macOS) / 18 | 정지 | Ctrl-Z → 전경 잡 정지 |
| `SIGCHLD` | 20 (Linux) | 무시 | 자식 종료/정지 시 부모에게 전달 |
| `SIGCONT` | 18 (macOS) / 19 | 재개 | `bg`/`fg` 명령에서 정지된 잡 재개 |

### 시그널 마스킹

```c
sigset_t mask, prev;
sigemptyset(&mask);
sigaddset(&mask, SIGCHLD);
sigprocmask(SIG_BLOCK, &mask, &prev);   // SIGCHLD 차단, 이전 상태 저장
// ... 임계 구역 ...
sigprocmask(SIG_SETMASK, &prev, NULL);  // 이전 상태 복원
```

### sigsuspend 패턴

```c
sigset_t empty;
sigemptyset(&empty);
while (condition) {
    sigsuspend(&empty);  // 시그널 대기 (원자적)
}
```

- 시그널 마스크를 일시적으로 `empty`로 설정하고 대기
- 시그널 핸들러 실행 후 원래 마스크가 복원되면서 반환
- `pause()`보다 안전: 마스크 변경과 대기가 원자적

## Async-Signal-Safe

### 핸들러에서 호출 가능한 함수 (발췌)
- `write()`, `read()`, `open()`, `close()`
- `fork()`, `execve()`, `_exit()`
- `waitpid()`, `kill()`, `getpid()`
- `sigprocmask()`, `sigaction()`

### 핸들러에서 호출 불가능한 함수
- `printf()`, `fprintf()`, `sprintf()` — 내부 락으로 인한 데드락 위험
- `malloc()`, `free()` — 비재진입
- `exit()` — atexit 핸들러 실행으로 인한 부작용

### sio (Signal-safe I/O) 구현
- `sio_puts(s)`: `write(STDOUT_FILENO, s, strlen(s))`
- `sio_putl(v)`: 정수를 문자열로 변환 + `write()`

## 잡 테이블

### 상태

| 상태 | 값 | 의미 |
|---|---|---|
| UNDEF | 0 | 빈 슬롯 |
| FG | 1 | 전경 실행 중 |
| BG | 2 | 배경 실행 중 |
| ST | 3 | 정지됨 |

### 잡 테이블 연산
- `addjob()`: SIGCHLD 차단 상태에서 호출 (레이스 방지)
- `deletejob()`: 핸들러에서 호출 (자식 회수 후)
- `fgpid()`: 현재 전경 잡의 PID 반환
- `listjobs()`: `jobs` 내장 명령 구현

## 내장 명령

| 명령 | 동작 |
|---|---|
| `quit` | `exit(0)` |
| `jobs` | 잡 테이블 출력 |
| `bg %jid` 또는 `bg pid` | 정지된 잡에 SIGCONT 전송, 상태를 BG로 변경 |
| `fg %jid` 또는 `fg pid` | 잡에 SIGCONT 전송, 상태를 FG로 변경, waitfg() |

## 테스트 패턴

### FIFO 기반 직접 하네스
1. `mkfifo`로 파이프 생성
2. 쉘을 `-p` 모드로 FIFO 입력과 함께 배경 실행
3. 명령어를 FIFO에 쓰기 (`printf '...\n' >&3`)
4. 시그널 전송 (`kill -INT "$SHELL_PID"`)
5. 출력 파일에서 기대 문자열 `grep`

### 테스트 케이스

| 케이스 | 검증 내용 |
|---|---|
| basic_echo | 외부 명령 실행 + 출력 |
| bg_jobs | 배경 잡 등록 + jobs 출력 |
| sigint | SIGINT 전달 + 종료 메시지 |
| stop_fg | SIGTSTP 정지 + fg 재개 + SIGINT 종료 |
