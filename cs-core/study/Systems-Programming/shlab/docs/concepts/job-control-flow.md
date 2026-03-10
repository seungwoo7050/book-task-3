# job control 흐름을 어떻게 읽을까

## 이 프로젝트의 핵심 built-in

Shell Lab에서 셸이 직접 책임지는 명령은 네 가지입니다.

- `quit`
- `jobs`
- `bg`
- `fg`

이 네 개가 제대로 되려면, 사실상 job table과 signal 처리 전체가 맞아야 합니다.

## foreground wait의 핵심

좋은 구현은 메인 경로에서 단순 `waitpid` 한 번으로 끝나지 않습니다.
보통은 "현재 PID가 foreground job인가"를 기준으로 기다리고,
실제 상태 갱신은 `SIGCHLD` handler가 담당합니다.

즉, `fg` 흐름은 다음 협업으로 봐야 합니다.

- 메인 루프: foreground job을 기다림
- signal handler: 종료, 중단, 재개 상태 반영
- job table: 두 경로가 같이 보는 진실 소스

## `bg`와 `fg`가 자주 틀리는 이유

- stopped 상태를 올바르게 다시 `Running`으로 바꾸지 않음
- signal을 프로세스 그룹 전체가 아니라 단일 PID에만 보냄
- foreground로 전환한 뒤 기다리지 않음

이런 실수는 셸이 "대체로 되는 것처럼" 보이게 만들어서 더 위험합니다.

## 이 저장소의 테스트가 보는 것

- background job이 `jobs`에 보이는가
- foreground job에 `SIGINT`가 전달되는가
- stopped job을 `fg`로 되살린 뒤 다시 끝까지 추적되는가

즉, 셸이 죽지 않는지만 보는 것이 아니라 job control semantics를 확인합니다.
