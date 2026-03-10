# Shell Lab에서 반드시 이해해야 하는 signal과 race

## 가장 유명한 race

Shell Lab의 대표적인 race는 다음 순서로 발생합니다.

1. 부모가 `fork`를 호출한다
2. 자식이 아주 빨리 끝난다
3. `SIGCHLD`가 먼저 도착해 handler가 자식을 reap한다
4. 부모는 그 뒤에야 job list에 자식을 추가하려 한다

이렇게 되면 job list가 실제 프로세스 상태와 어긋납니다.

## 왜 `SIGCHLD`를 막아야 하는가

그래서 부모는 보통 다음 순서를 택합니다.

1. `SIGCHLD` block
2. `fork`
3. 부모에서 job list에 추가
4. 이전 mask 복구

자식은 `execvp` 전에 원래 mask를 복구해야 합니다.
이 순서를 이해하지 못하면 job control이 간헐적으로만 깨지는 현상을 잡기 어렵습니다.

## process group이 중요한 이유

Ctrl-C, Ctrl-Z는 셸 자신이 아니라 foreground job에 전달돼야 합니다.
그래서 자식은 보통 `setpgid(0, 0)`을 호출해 자신의 process group을 분리합니다.

이 구분이 없으면, interactive signal이 셸 본체까지 잘못 전달될 수 있습니다.

## 이 문서를 읽고 확인할 것

- 왜 `waitpid`를 메인 흐름에서 단순 blocking으로만 쓰지 않는가
- 왜 signal handler와 foreground wait loop가 같은 job table 규칙을 공유해야 하는가
- 왜 테스트도 signal-aware 해야 하는가
