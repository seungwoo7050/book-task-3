# proxylab-cpp 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 프록시 구현 전에 기본 계약과 제약을 확인하고 싶은 학습자, shared helper와 driver wrapper의 역할을 알고 싶은 사람, 구현 디렉터리와 문제 경계를 분리하고 싶은 사람을 한 흐름으로 설명하고 검증한다. 핵심은 `remove_entry`와 `insert_front`, `promote_entry` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 프록시 구현 전에 기본 계약과 제약을 확인하고 싶은 학습자
- shared helper와 driver wrapper의 역할을 알고 싶은 사람
- 구현 디렉터리와 문제 경계를 분리하고 싶은 사람
- 첫 진입점은 `../study/Systems-Programming/proxylab/cpp/src/proxy.cpp`이고, 여기서 `remove_entry`와 `insert_front` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/Systems-Programming/proxylab/cpp/src/proxy.cpp`: `remove_entry`, `insert_front`, `promote_entry`, `cache_lookup`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Systems-Programming/proxylab/problem/code/csapp.h`: `rio_readinitb`, `rio_readnb`, `rio_readlineb`, `rio_writen`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Systems-Programming/proxylab/problem/code/csapp.c`: `rio_read`, `rio_readinitb`, `rio_readnb`, `rio_readlineb`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Systems-Programming/proxylab/problem/script/driver.sh`: 검증 절차나 보조 자동화를 담아 결과를 재현하는 스크립트다.
- `../study/Systems-Programming/proxylab/cpp/Makefile`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.
- `../study/Systems-Programming/proxylab/problem/Makefile`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.
- `remove_entry` 등이 맡는 책임을 한 함수에 뭉개지 말고 상태 전이 단위로 분리한다.
- 회귀 게이트는 `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/proxylab/cpp test`이며, 핵심 상태 전이를 바꿀 때마다 중간 검증으로 다시 실행한다.

## 정답을 재구성하는 절차

1. `../study/Systems-Programming/proxylab/problem/code/csapp.c`와 `../study/Systems-Programming/proxylab/cpp/src/proxy.cpp`를 나란히 열어 먼저 바뀌는 경계를 잡는다.
2. `remove_entry` 등이 맡는 책임을 분리해 각 출력 계약을 완성한다.
3. `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/proxylab/cpp test`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/proxylab/cpp test
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/proxylab/problem
```

- `../study/Systems-Programming/proxylab/problem/code/csapp.c` starter skeleton의 빈칸을 그대로 정답으로 착각하지 않는다.
- `../study/Systems-Programming/proxylab/problem/script/driver.sh` fixture/trace를 읽지 않고 동작을 추측하지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/proxylab/cpp test`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/Systems-Programming/proxylab/cpp/src/proxy.cpp`
- `../study/Systems-Programming/proxylab/problem/code/csapp.h`
- `../study/Systems-Programming/proxylab/problem/code/csapp.c`
- `../study/Systems-Programming/proxylab/problem/script/driver.sh`
- `../study/Systems-Programming/proxylab/cpp/Makefile`
- `../study/Systems-Programming/proxylab/problem/Makefile`
