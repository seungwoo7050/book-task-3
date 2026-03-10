# 01. 접근 기록

## 실제로 택한 접근

이 프로젝트는 문법보다 순서가 중요했다.
그래서 기능 구현 순서를 다음처럼 잡았다.

1. `SIGCHLD` 마스킹 규칙 먼저 고정
2. child에서 `setpgid(0, 0)` 적용
3. 기본 command 실행과 foreground wait
4. `jobs`, `bg`, `fg`
5. self-owned signal 테스트 추가

## 왜 이렇게 했는가

- job table race를 먼저 막지 않으면 뒤 기능이 전부 불안정해진다
- process group 처리가 없으면 Ctrl-C와 Ctrl-Z 의미가 흐려진다
- shell은 "대부분 된다"가 가장 위험한 상태라, 테스트를 빨리 붙이는 편이 낫다
