# cs-core study

`cs-core/study`는 4개 트랙, 15개 프로젝트를 `문제 계약 -> 실행 가능한 답 -> 검증 -> 학습 노트`로 분리해 둔 multi-track 학습 아카이브다.
GitHub 방문자가 루트에서 바로 `무슨 문제를 풀었는지`, `답이 어디 있는지`, `어떻게 검증하는지`를 찾을 수 있게 공개 표면을 짧고 반복 가능한 형태로 유지한다.

## 먼저 읽을 곳

1. [`docs/curriculum-map.md`](docs/curriculum-map.md)
2. [`docs/repository-architecture.md`](docs/repository-architecture.md)
3. [`Foundations-CSAPP/README.md`](Foundations-CSAPP/README.md)
4. [`Systems-Programming/README.md`](Systems-Programming/README.md)
5. [`Operating-Systems-Internals/README.md`](Operating-Systems-Internals/README.md)
6. [`Programming-Languages-Foundations/README.md`](Programming-Languages-Foundations/README.md)

## 트랙 요약

| 트랙 | 핵심 질문 | 프로젝트 수 | 시작점 |
| --- | --- | --- | --- |
| `Foundations-CSAPP` | 비트 표현, ISA, 캐시, 역공학의 바닥을 어떻게 세울까 | 5 | [`datalab`](Foundations-CSAPP/datalab/README.md) |
| `Systems-Programming` | 프로세스, 시그널, 메모리, 네트워크를 직접 구현하면 어떤 계약이 보일까 | 3 | [`shlab`](Systems-Programming/shlab/README.md) |
| `Operating-Systems-Internals` | scheduler, VM, filesystem, synchronization을 작은 실험으로 어떻게 재설명할까 | 4 | [`scheduling-simulator`](Operating-Systems-Internals/scheduling-simulator/README.md) |
| `Programming-Languages-Foundations` | parser, type checker, VM을 같은 언어 표면으로 어떻게 이어 볼까 | 3 | [`parser-interpreter`](Programming-Languages-Foundations/parser-interpreter/README.md) |

## 프로젝트 카탈로그

| 트랙 | 프로젝트 | 문제 | 이 레포의 답 | 검증 시작점 | 상태 |
| --- | --- | --- | --- | --- | --- |
| `Foundations-CSAPP` | [`datalab`](Foundations-CSAPP/datalab/README.md) | 제한된 연산자로 `bits.c` 13개 퍼즐 구현 | `c/src/bits.c`, `cpp/src/bits.cpp`, `docs/` | [`problem`](Foundations-CSAPP/datalab/problem/README.md), [`c`](Foundations-CSAPP/datalab/c/README.md), [`cpp`](Foundations-CSAPP/datalab/cpp/README.md) | `verified (local-only asset)` |
| `Foundations-CSAPP` | [`archlab`](Foundations-CSAPP/archlab/README.md) | Y86 작성, `iaddq` 제어 로직, `ncopy` 성능 개선 | `y86/src/*.ys`, `c/src/mini_archlab.c`, `cpp/src/mini_archlab.cpp` | [`problem`](Foundations-CSAPP/archlab/problem/README.md), [`y86`](Foundations-CSAPP/archlab/y86/README.md), [`c`](Foundations-CSAPP/archlab/c/README.md) | `verified (local-only asset)` |
| `Foundations-CSAPP` | [`bomblab`](Foundations-CSAPP/bomblab/README.md) | phase별 입력 조건을 assembly에서 복원 | `c/src/mini_bomb.c`, `cpp/src/mini_bomb.cpp`, `docs/` | [`problem`](Foundations-CSAPP/bomblab/problem/README.md), [`c`](Foundations-CSAPP/bomblab/c/README.md), [`cpp`](Foundations-CSAPP/bomblab/cpp/README.md) | `verified (local-only asset)` |
| `Foundations-CSAPP` | [`attacklab`](Foundations-CSAPP/attacklab/README.md) | code injection, ROP, 상대 주소 계산 이해 | `c/src/mini_attacklab.c`, `cpp/src/mini_attacklab.cpp`, `docs/` | [`problem`](Foundations-CSAPP/attacklab/problem/README.md), [`c`](Foundations-CSAPP/attacklab/c/README.md), [`cpp`](Foundations-CSAPP/attacklab/cpp/README.md) | `verified (local-only asset)` |
| `Foundations-CSAPP` | [`perflab`](Foundations-CSAPP/perflab/README.md) | cache simulator와 cache-friendly transpose 구현 | `c/src/perflab.c`, `cpp/src/perflab.cpp`, `docs/` | [`problem`](Foundations-CSAPP/perflab/problem/README.md), [`c`](Foundations-CSAPP/perflab/c/README.md), [`cpp`](Foundations-CSAPP/perflab/cpp/README.md) | `public verified` |
| `Systems-Programming` | [`shlab`](Systems-Programming/shlab/README.md) | process group과 job control shell 구현 | `c/src/tsh.c`, `cpp/src/tsh.cpp`, `tests/` | [`problem`](Systems-Programming/shlab/problem/README.md), [`c`](Systems-Programming/shlab/c/README.md), [`cpp`](Systems-Programming/shlab/cpp/README.md) | `public verified` |
| `Systems-Programming` | [`malloclab`](Systems-Programming/malloclab/README.md) | explicit free list allocator 구현 | `c/src/mm.c`, `cpp/src/mm.cpp`, `docs/` | [`problem`](Systems-Programming/malloclab/problem/README.md), [`c`](Systems-Programming/malloclab/c/README.md), [`cpp`](Systems-Programming/malloclab/cpp/README.md) | `public verified` |
| `Systems-Programming` | [`proxylab`](Systems-Programming/proxylab/README.md) | concurrent HTTP proxy와 in-memory cache 구현 | `c/src/proxy.c`, `cpp/src/proxy.cpp`, `tests/` | [`problem`](Systems-Programming/proxylab/problem/README.md), [`c`](Systems-Programming/proxylab/c/README.md), [`cpp`](Systems-Programming/proxylab/cpp/README.md) | `public verified` |
| `Operating-Systems-Internals` | [`scheduling-simulator`](Operating-Systems-Internals/scheduling-simulator/README.md) | scheduling policy가 지표를 어떻게 바꾸는지 실험 | `python/src`, fixture, replay CLI | [`problem`](Operating-Systems-Internals/scheduling-simulator/problem/README.md), [`python`](Operating-Systems-Internals/scheduling-simulator/python/README.md) | `public verified` |
| `Operating-Systems-Internals` | [`virtual-memory-lab`](Operating-Systems-Internals/virtual-memory-lab/README.md) | replacement policy와 locality 비교 | `python/src`, trace fixture, replay CLI | [`problem`](Operating-Systems-Internals/virtual-memory-lab/problem/README.md), [`python`](Operating-Systems-Internals/virtual-memory-lab/python/README.md) | `public verified` |
| `Operating-Systems-Internals` | [`filesystem-mini-lab`](Operating-Systems-Internals/filesystem-mini-lab/README.md) | inode/block/journaling recovery toy filesystem | `python/src`, JSON disk image, demo fixture | [`problem`](Operating-Systems-Internals/filesystem-mini-lab/problem/README.md), [`python`](Operating-Systems-Internals/filesystem-mini-lab/python/README.md) | `public verified` |
| `Operating-Systems-Internals` | [`synchronization-contention-lab`](Operating-Systems-Internals/synchronization-contention-lab/README.md) | mutex, semaphore, condvar contention 실험 | `c/src`, shell test, demo scenario | [`problem`](Operating-Systems-Internals/synchronization-contention-lab/problem/README.md), [`c`](Operating-Systems-Internals/synchronization-contention-lab/c/README.md) | `public verified` |
| `Programming-Languages-Foundations` | [`parser-interpreter`](Programming-Languages-Foundations/parser-interpreter/README.md) | lexer, parser, tree-walk evaluator 구현 | `src/parser_interpreter`, `tests/`, `examples/` | [`problem`](Programming-Languages-Foundations/parser-interpreter/problem/README.md), [`docs`](Programming-Languages-Foundations/parser-interpreter/docs/README.md) | `public verified` |
| `Programming-Languages-Foundations` | [`static-type-checking`](Programming-Languages-Foundations/static-type-checking/README.md) | 같은 언어에 static type rule 추가 | `src/static_type_checking`, `tests/`, `examples/` | [`problem`](Programming-Languages-Foundations/static-type-checking/problem/README.md), [`docs`](Programming-Languages-Foundations/static-type-checking/docs/README.md) | `public verified` |
| `Programming-Languages-Foundations` | [`bytecode-ir`](Programming-Languages-Foundations/bytecode-ir/README.md) | 같은 언어를 bytecode와 VM으로 lowering | `src/bytecode_ir`, `tests/`, `examples/` | [`problem`](Programming-Languages-Foundations/bytecode-ir/problem/README.md), [`docs`](Programming-Languages-Foundations/bytecode-ir/docs/README.md) | `public verified` |

## 공통 규칙

- README 표면 계약은 [`docs/readme-contract.md`](docs/readme-contract.md)를 따른다.
- 디렉터리 책임은 [`docs/repository-architecture.md`](docs/repository-architecture.md)에 고정한다.
- 프로젝트별 현재 상태와 대표 검증 경로는 [`docs/status-matrix.md`](docs/status-matrix.md)에서 한눈에 확인한다.

## 공개 경계

- 공개 README는 `문제`, `답`, `검증`, `공개 범위`만 짧게 보여 주고, 긴 reasoning은 각 프로젝트의 `docs/`, `notion/`으로 내린다.
- `bomblab`, `attacklab`, 공식 handout 기반 프로젝트는 local-only asset 경계를 명시하고 직접 재사용 가능한 raw 답안은 늘리지 않는다.
- authored prose와 code comment는 한국어를 기본으로 유지하되, 명령어와 code identifier는 English 그대로 둔다.
