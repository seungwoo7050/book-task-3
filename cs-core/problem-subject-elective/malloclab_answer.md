# malloclab 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 allocator API 계약을 먼저 확인하고 싶은 학습자, trace 형식과 driver 역할을 이해하고 싶은 사람, 구현 디렉터리와 문제 경계를 분리하고 싶은 사람을 한 흐름으로 설명하고 검증한다. 핵심은 `align_size`와 `pack`, `load_word` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- allocator API 계약을 먼저 확인하고 싶은 학습자
- trace 형식과 driver 역할을 이해하고 싶은 사람
- 구현 디렉터리와 문제 경계를 분리하고 싶은 사람
- 첫 진입점은 `../study/Systems-Programming/malloclab/c/src/mm.c`이고, 여기서 `align_size`와 `pack` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/Systems-Programming/malloclab/c/src/mm.c`: `align_size`, `pack`, `load_word`, `store_word`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Systems-Programming/malloclab/cpp/src/mm.cpp`: `store_word`, `is_allocated`, `add_to_free_list`, `remove_from_free_list`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Systems-Programming/malloclab/problem/code/memlib.c`: `mem_init`, `mem_deinit`, `mem_reset_brk`, `mem_heapsize`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Systems-Programming/malloclab/problem/code/memlib.h`: `mem_init`, `mem_deinit`, `mem_reset_brk`, `mem_heapsize`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Systems-Programming/malloclab/problem/code/mm.c`: `mm_init`, `mm_free`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Systems-Programming/malloclab/problem/data/traces/basic.rep`: 핵심 구현을 담는 파일이다.
- `../study/Systems-Programming/malloclab/problem/data/traces/coalesce.rep`: 핵심 구현을 담는 파일이다.
- `../study/Systems-Programming/malloclab/problem/data/traces/mixed.rep`: 핵심 구현을 담는 파일이다.

## 정답을 재구성하는 절차

1. `../study/Systems-Programming/malloclab/problem/code/memlib.c`와 `../study/Systems-Programming/malloclab/c/src/mm.c`를 나란히 열어 먼저 바뀌는 경계를 잡는다.
2. `align_size` 등이 맡는 책임을 분리해 각 출력 계약을 완성한다.
3. `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/malloclab/c test`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/malloclab/c test
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/malloclab/cpp test
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/malloclab/problem
```

- `../study/Systems-Programming/malloclab/problem/code/memlib.c` starter skeleton의 빈칸을 그대로 정답으로 착각하지 않는다.
- `../study/Systems-Programming/malloclab/problem/data/traces/basic.rep` 등 fixture/trace를 읽지 않고 동작을 추측하지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/malloclab/c test`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/Systems-Programming/malloclab/c/src/mm.c`
- `../study/Systems-Programming/malloclab/cpp/src/mm.cpp`
- `../study/Systems-Programming/malloclab/problem/code/memlib.c`
- `../study/Systems-Programming/malloclab/problem/code/memlib.h`
- `../study/Systems-Programming/malloclab/problem/code/mm.c`
- `../study/Systems-Programming/malloclab/problem/data/traces/basic.rep`
- `../study/Systems-Programming/malloclab/problem/data/traces/coalesce.rep`
- `../study/Systems-Programming/malloclab/problem/data/traces/mixed.rep`
- `../study/Systems-Programming/malloclab/problem/data/traces/realloc.rep`
- `../study/Systems-Programming/malloclab/c/Makefile`
