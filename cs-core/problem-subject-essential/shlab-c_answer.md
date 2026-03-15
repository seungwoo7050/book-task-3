# shlab-c 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 공식 starter 없이도 과제 목적을 먼저 파악하고 싶은 학습자, 어떤 자산을 제거했고 무엇으로 대체했는지 알고 싶은 사람, 공개 가능한 문제 경계 문서를 설계하고 싶은 사람을 한 흐름으로 설명하고 검증한다. 핵심은 `handler_t`와 `eval`, `builtin_cmd` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 공식 starter 없이도 과제 목적을 먼저 파악하고 싶은 학습자
- 어떤 자산을 제거했고 무엇으로 대체했는지 알고 싶은 사람
- 공개 가능한 문제 경계 문서를 설계하고 싶은 사람
- 첫 진입점은 `../study/Systems-Programming/shlab/c/src/tsh.c`이고, 여기서 `handler_t`와 `eval` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/Systems-Programming/shlab/c/src/tsh.c`: `handler_t`, `eval`, `builtin_cmd`, `do_bgfg`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Systems-Programming/shlab/c/include/tsh_helper.h`: `sio_puts`, `sio_putl`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Systems-Programming/shlab/c/tests/run_tests.sh`: 검증 절차나 보조 자동화를 담아 결과를 재현하는 스크립트다.
- `../study/Systems-Programming/shlab/c/Makefile`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.
- `../study/Systems-Programming/shlab/problem/Makefile`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.
- `handler_t` 등이 맡는 책임을 한 함수에 뭉개지 말고 상태 전이 단위로 분리한다.
- 회귀 게이트는 `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/shlab/c test`이며, 핵심 상태 전이를 바꿀 때마다 중간 검증으로 다시 실행한다.
- `../study/Systems-Programming/shlab/c/Makefile`는 실행 루트와 모듈 경계를 고정해 검증이 어느 위치에서 돌아야 하는지 알려 준다.

## 정답을 재구성하는 절차

1. `../study/Systems-Programming/shlab/c/src/tsh.c`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `handler_t` 등이 맡는 책임을 분리해 각 출력 계약을 완성한다.
3. `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/shlab/c test`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/shlab/c test
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/shlab/problem
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `../study/Systems-Programming/shlab/c/tests/run_tests.sh` fixture/trace를 읽지 않고 동작을 추측하지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/shlab/c test`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/Systems-Programming/shlab/c/src/tsh.c`
- `../study/Systems-Programming/shlab/c/include/tsh_helper.h`
- `../study/Systems-Programming/shlab/c/tests/run_tests.sh`
- `../study/Systems-Programming/shlab/c/Makefile`
- `../study/Systems-Programming/shlab/problem/Makefile`
