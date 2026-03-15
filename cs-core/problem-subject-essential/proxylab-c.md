# proxylab-c 문제지

## 왜 중요한가

이 디렉터리는 프록시의 문제 계약과 starter boundary를 보존합니다. 절대형 GET 요청 파싱, server 연결, 응답 전달, 작은 object cache가 핵심 계약입니다.

## 목표

시작 위치의 구현을 완성해 프록시 구현 전에 기본 계약과 제약을 확인하고 싶은 학습자, shared helper와 driver wrapper의 역할을 알고 싶은 사람, 구현 디렉터리와 문제 경계를 분리하고 싶은 사람을 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/Systems-Programming/proxylab/problem/code/csapp.c`
- `../study/Systems-Programming/proxylab/problem/code/csapp.h`
- `../study/Systems-Programming/proxylab/c/src/proxy.c`
- `../study/Systems-Programming/proxylab/problem/script/driver.sh`
- `../study/Systems-Programming/proxylab/c/Makefile`
- `../study/Systems-Programming/proxylab/problem/Makefile`

## starter code / 입력 계약

- ../study/Systems-Programming/proxylab/problem/code/csapp.c에서 starter 코드와 입력 경계를 잡는다.
- ../study/Systems-Programming/proxylab/problem/code/csapp.h에서 starter 코드와 입력 경계를 잡는다.
- ../study/Systems-Programming/proxylab/problem/code/proxy.c에서 starter 코드와 입력 경계를 잡는다.

## 핵심 요구사항

- 프록시 구현 전에 기본 계약과 제약을 확인하고 싶은 학습자
- shared helper와 driver wrapper의 역할을 알고 싶은 사람
- 구현 디렉터리와 문제 경계를 분리하고 싶은 사람
- code/csapp.h

## 제외 범위

- `../study/Systems-Programming/proxylab/problem/code/csapp.c` starter skeleton을 정답 구현으로 착각하지 않는다.
- `../study/Systems-Programming/proxylab/problem/script/driver.sh` fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- `../study/Systems-Programming/proxylab/problem/code/csapp.c`의 빈 확장 지점을 실제 구현으로 채웠다.
- 핵심 흐름은 `handle_client`와 `client_error`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- `../study/Systems-Programming/proxylab/problem/script/driver.sh` fixture/trace 기준으로 결과를 대조했다.
- `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/proxylab/c test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/proxylab/c test
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/proxylab/problem
```

- `proxylab`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`proxylab-c_answer.md`](proxylab-c_answer.md)에서 확인한다.
