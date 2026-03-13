# Shell Lab 문제지

## 왜 서버 개발자에게 중요한가

이 랩은 서버 프로세스가 OS와 어떻게 상호작용하는지를 몸으로 익히게 해 준다.

- `fork` / `execvp`
- process group
- foreground / background job control
- `SIGCHLD`, `SIGINT`, `SIGTSTP`
- race-free child reaping

## 목표

foreground job, background job, signal forwarding을 지원하는 tiny shell을 구현하라.
이 shell은 사용자가 입력한 외부 명령을 실행하고, job table을 유지하며, 시그널을 올바른 프로세스 그룹으로 전달해야 한다.

## 시작 위치

- 문제 경계: `study/Systems-Programming/shlab/problem/`
- 공용 하네스: `study/Systems-Programming/shlab/tests/direct_shell_case.sh`
- 공용 테스트 실행기: `study/Systems-Programming/shlab/c/tests/run_tests.sh`

주의:
이 레포에는 원본 starter shell과 공식 trace가 들어 있지 않다.
즉, `shlab/problem/`은 계약 문서만 남긴 상태이고, 실제 구현 파일은 스스로 만들어야 한다.

## starter code 유무

이 문제는 이 레포 안에 공개된 starter code가 없다.
즉, 문제지는 요구사항과 검증 방법만 제공하고, 구현 파일은 네가 새로 만들어야 한다.

## 제출물 성격

실행 가능한 tiny shell 프로그램 하나를 만든다.
관례상 이름은 `tsh`를 많이 쓰지만, 테스트 하네스는 실행 파일 경로만 맞으면 된다.

## 반드시 만족해야 하는 기능 요구사항

1. 한 줄씩 명령을 읽고 외부 프로그램을 실행한다.

2. 명령 끝의 `&`를 인식해 background job으로 실행한다.

3. 아래 builtin command를 지원한다.

- `quit`
- `jobs`
- `bg`
- `fg`

4. job table을 유지한다.
각 job에 대해 최소한 아래 정보는 관리할 수 있어야 한다.

- PID
- job id
- 상태, `FG`, `BG`, `ST`
- 원래 명령줄

5. 외부 명령 실행은 `fork` 후 `execvp`로 처리한다.

6. 자식은 shell과 다른 process group으로 분리해야 한다.
즉, interactive signal이 shell 본체가 아니라 foreground job으로 가도록 해야 한다.

7. foreground job이 있을 때 shell은 그 job 상태가 바뀔 때까지 기다릴 수 있어야 한다.

8. `SIGINT`와 `SIGTSTP`는 현재 foreground job의 process group으로 전달되어야 한다.
shell 자신이 종료되거나 멈추면 안 된다.

9. `SIGCHLD` handler는 종료된 자식과 중단된 자식을 회수해야 한다.

10. `fork`와 job 등록 사이의 race를 막아야 한다.
대표적으로, 자식이 너무 빨리 끝나 `SIGCHLD`가 먼저 와도 job table이 깨지면 안 된다.

11. `bg`와 `fg`는 PID 또는 `%jobid` 형식의 인자를 받아 stopped job을 다시 실행할 수 있어야 한다.

12. foreground job이 signal로 종료되거나 중단되면 적절한 상태 메시지를 출력해야 한다.

## 이번 문제에서 일부러 제외한 범위

- pipe
- redirection
- quoting
- command history
- job persistence
- full POSIX shell grammar

## 핵심 설계 포인트

- 부모는 `fork` 전후로 `SIGCHLD` race를 제어해야 한다.
- 자식은 `execvp` 전에 signal mask를 적절히 복구해야 한다.
- foreground wait는 단순한 `waitpid` 한 번으로 끝내기보다, signal handler와 job table이 협력하는 구조가 안전하다.

## 성공 체크리스트

- `/bin/echo hello` 같은 단순 명령이 실행된다.
- `/bin/sleep 1 &` 실행 후 `jobs`에서 background job이 보인다.
- foreground job 실행 중 `SIGINT`가 오면 shell이 아니라 job이 종료된다.
- foreground job 실행 중 `SIGTSTP`가 오면 stopped 상태로 바뀐다.
- `fg %1` 또는 `fg <pid>`로 stopped job을 다시 foreground로 가져올 수 있다.
- 자식이 매우 빨리 끝나도 job table이 망가지지 않는다.

## 검증 방법

개별 시나리오 하나만 확인:

```bash
study/Systems-Programming/shlab/tests/direct_shell_case.sh /path/to/your/tsh basic_echo
study/Systems-Programming/shlab/tests/direct_shell_case.sh /path/to/your/tsh bg_jobs
study/Systems-Programming/shlab/tests/direct_shell_case.sh /path/to/your/tsh sigint
study/Systems-Programming/shlab/tests/direct_shell_case.sh /path/to/your/tsh stop_fg
```

공용 테스트 한 번에 실행:

```bash
study/Systems-Programming/shlab/c/tests/run_tests.sh /path/to/your/tsh
```

## 스포일러 경계

아래는 답안 구현이므로 먼저 풀어볼 때는 열지 않는 것을 권한다.

- `study/Systems-Programming/shlab/c/src/tsh.c`
- `study/Systems-Programming/shlab/cpp/src/tsh.cpp`
- `study/Systems-Programming/shlab/notion/`
- `study/blog/Systems-Programming/shlab/`
