# 00. 문제 정의

## 문제를 어떻게 이해했는가

`shlab`은 "작은 셸 만들기"보다 "job control과 signal의 순서를 맞추는 프로젝트"라고 이해했다.
공식 starter shell과 traces를 공개 트리에 그대로 둘 수 없었기 때문에,
문제 계약과 self-owned 검증 경로를 분리하는 구조가 필요했다.

## 저장소 기준 성공 조건

- foreground/background job이 구분된다
- `quit`, `jobs`, `bg`, `fg` built-in이 동작한다
- interactive signal이 foreground process group으로 전달된다
- `SIGCHLD` race를 막는 흐름이 설명 가능하다
- 공식 starter 없이도 self-owned 테스트로 기능을 재확인할 수 있다

## 선수 지식

- process group
- signal mask와 `sigprocmask`
- `waitpid`와 상태 플래그
- race condition 기본 개념
