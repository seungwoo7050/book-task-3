# 04. 지식 인덱스

## 핵심 개념과 다시 볼 이유

- process group과 terminal signal: foreground job이 누구인지 명확히 하지 않으면 셸 전체가 비정상 동작한다.
- `SIGCHLD` masking discipline: `fork`와 `addjob` 사이의 race를 막는 핵심 규칙이다.
- foreground/background job state: builtin 명령이 바꾸는 상태를 표처럼 정리해 두면 디버깅이 훨씬 빨라진다.
- `waitpid` 기반 reaping: `WNOHANG`, `WUNTRACED`, `WCONTINUED` 의미를 구분해야 zombie와 stop/resume 문제가 풀린다.
- builtin과 child execution 분리: 파싱이 끝난 뒤 어떤 경로가 부모에서 끝나고 어떤 경로가 자식으로 내려가는지 분리해서 봐야 한다.

## 재현 중 막히면 먼저 확인할 것

- signal/race 설명: `../docs/concepts/signal-and-race-discipline.md`
- job control 흐름: `../docs/concepts/job-control-flow.md`
- 현재 검증 순서: `../docs/references/verification.md`

## 이후 프로젝트와 연결되는 메모

- race를 막는 규칙을 먼저 문장으로 쓰는 습관은 `proxylab`의 동시성 문서에도 그대로 이어진다.
- 시스템 코드는 기능 구현보다 상태 전이 설명이 먼저여야 포트폴리오 문서로도 강해진다.
