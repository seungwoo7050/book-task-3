# filesystem-mini-lab 문제지

## 왜 중요한가

디스크 이미지는 JSON 파일 하나로 고정한다. root directory 하나만 지원하고, 파일 연산은 create, write, cat, ls, unlink, recover만 다룬다. inode bitmap과 block bitmap이 실제 allocation/free를 반영해야 한다. journaling은 metadata-only write-ahead log로 제한하고, crash 이후 recover가 committed entry를 replay하고 prepared entry를 폐기해야 한다.

## 목표

시작 위치의 구현을 완성해 create/write/read/delete가 JSON image 위에서 일관되게 동작한다, reopen 후 상태가 유지된다, committed journal replay와 incomplete journal discard가 tests로 재현된다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/Operating-Systems-Internals/filesystem-mini-lab/python/src/os_mini_fs/__init__.py`
- `../study/Operating-Systems-Internals/filesystem-mini-lab/python/src/os_mini_fs/__main__.py`
- `../study/Operating-Systems-Internals/filesystem-mini-lab/python/src/os_mini_fs/cli.py`
- `../study/Operating-Systems-Internals/filesystem-mini-lab/python/src/os_mini_fs/core.py`
- `../study/Operating-Systems-Internals/filesystem-mini-lab/python/tests/test_os_mini_fs.py`
- `../study/Operating-Systems-Internals/filesystem-mini-lab/problem/script/run_demo.py`
- `../study/Operating-Systems-Internals/filesystem-mini-lab/problem/Makefile`

## starter code / 입력 계약

- `../study/Operating-Systems-Internals/filesystem-mini-lab/python/src/os_mini_fs/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- create/write/read/delete가 JSON image 위에서 일관되게 동작한다.
- reopen 후 상태가 유지된다.
- committed journal replay와 incomplete journal discard가 tests로 재현된다.

## 제외 범위

- `../study/Operating-Systems-Internals/filesystem-mini-lab/problem/script/run_demo.py` fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `build_parser`와 `main`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `make_fs`와 `test_create_write_read_round_trip`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/Operating-Systems-Internals/filesystem-mini-lab/problem/script/run_demo.py` fixture/trace 기준으로 결과를 대조했다.
- `make test && make run-demo`가 통과한다.

## 검증 방법

```bash
make test && make run-demo
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Operating-Systems-Internals/filesystem-mini-lab/problem test
```

- `filesystem-mini-lab`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`filesystem-mini-lab_answer.md`](filesystem-mini-lab_answer.md)에서 확인한다.
