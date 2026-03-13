# CS-Core 블로그

`cs-core/study/blog`는 루트 README나 각 프로젝트 README로는 다 담기지 않는 구현 순서와 판단 이동을 다시 읽기 위한 계층이다. 각 프로젝트를 독립 단위로 나눠, source-first evidence와 최종 서사를 같은 자리에서 따라가게 만든다.

이 디렉터리를 읽는 가장 좋은 순서는 트랙 README에서 큰 지도를 본 뒤, 프로젝트별 `00-series-map.md`로 들어가 `01-evidence-ledger.md`, `_structure-outline.md`, 최종 blog를 차례로 읽는 것이다. 기존 초안은 모두 `_legacy`에 보관했고, 현재 활성 문서는 그 본문을 입력으로 삼지 않는다.

## 트랙 가이드

### [Foundations-CSAPP](Foundations-CSAPP/)

CS:APP 계열 lab들을 source-first chronology로 다시 읽는 트랙이다. bit puzzle, Y86, reverse engineering, cache-aware optimization처럼 표면은 달라도 결국은 문제 계약을 검증 가능한 코드와 companion test로 번역하는 과정이 중심이 된다.

- [Architecture Lab](Foundations-CSAPP/archlab/00-series-map.md) — `archlab`은 Y86-64 프로그램 작성, 제어 로직 구현, 파이프라인 성능 개선을 한 흐름으로 묶는 프로젝트다.
- [Attack Lab](Foundations-CSAPP/attacklab/00-series-map.md) — `attacklab`은 stack layout, code injection, ROP, 상대 주소 계산을 단계적으로 익히는 프로젝트다.
- [Bomb Lab](Foundations-CSAPP/bomblab/00-series-map.md) — `bomblab`은 x86-64 bomb를 brute force가 아니라 해석 절차로 풀어 가는 프로젝트다.
- [Data Lab](Foundations-CSAPP/datalab/00-series-map.md) — `datalab`은 bit-level 제약을 지키면서 정수 표현과 부동소수점 경계를 직접 구현하는 프로젝트다.
- [Performance Lab](Foundations-CSAPP/perflab/00-series-map.md) — `perflab`은 cache simulator와 transpose 최적화를 통해 "왜 더 빠른가"를 코드와 지표로 설명하는 프로젝트다.

### [Systems-Programming](Systems-Programming/)

시스템 프로그래밍 트랙은 allocator, shell, proxy처럼 운영체제와 네트워크의 경계에 있는 프로그램을 다시 읽는다. 공통 질문은 언제나 같다. 상태를 어떻게 관리했고, 어떤 invariant를 먼저 고정했으며, 어떤 테스트로 그 약속을 닫았는가.

- [Malloc Lab](Systems-Programming/malloclab/00-series-map.md) — `malloclab`은 힙 블록 레이아웃, 정렬 규칙, explicit free list, coalescing, `realloc`을 한 번에 다루는 allocator 프로젝트다.
- [Proxy Lab](Systems-Programming/proxylab/00-series-map.md) — `proxylab`은 HTTP 요청 파싱, header 정규화, concurrent connection 처리, in-memory cache 설계를 하나의 프록시 구현으로 묶는 프로젝트다.
- [Shell Lab](Systems-Programming/shlab/00-series-map.md) — `shlab`은 프로세스 그룹, foreground/background job control, `SIGCHLD` 처리, `fork` 주변 race를 작은 셸 구현으로 익히는 프로젝트다.

### [Operating-Systems-Internals](Operating-Systems-Internals/)

운영체제 내부 동작을 작은 실험으로 끌어내린 트랙이다. scheduler, virtual memory, journaling, synchronization을 모두 장난감 모델로 축소했지만, 각 프로젝트는 상태 전이와 복구 규칙을 실제 CLI와 테스트로 끝까지 확인하는 데 초점을 둔다.

- [Filesystem Mini Lab](Operating-Systems-Internals/filesystem-mini-lab/00-series-map.md) — `filesystem-mini-lab`은 root-only toy filesystem으로 inode allocation, block allocation, metadata journaling, recovery를 작은 JSON disk image 위에서 설명하는 실험이다.
- [Scheduling Simulator](Operating-Systems-Internals/scheduling-simulator/00-series-map.md) — `scheduling-simulator`는 단일 CPU 위에서 scheduling policy가 waiting time, response time, turnaround time을 어떻게 바꾸는지 replay와 지표로 보여 주는 실험이다.
- [Synchronization Contention Lab](Operating-Systems-Internals/synchronization-contention-lab/00-series-map.md) — `synchronization-contention-lab`는 mutex, semaphore, condition variable이 서로 다른 contention pattern에서 correctness와 timing을 어떻게 드러내는지 보여 주는 C 실험이다.
- [Virtual Memory Lab](Operating-Systems-Internals/virtual-memory-lab/00-series-map.md) — `virtual-memory-lab`는 page reference trace를 따라가며 replacement policy와 locality가 page fault 수를 어떻게 바꾸는지 보여 주는 실험이다.

### [Programming-Languages-Foundations](Programming-Languages-Foundations/)

작은 함수형 언어를 parser, type checker, bytecode VM으로 차례로 다시 구현하는 트랙이다. 같은 언어 표면을 유지한 채 실행 모델만 바뀔 때 무엇이 달라지는지, 그리고 그 차이를 어떤 진단·테스트·demo로 보여 줄 수 있는지를 따라간다.

- [Bytecode IR](Programming-Languages-Foundations/bytecode-ir/00-series-map.md) — `bytecode-ir`는 같은 toy language를 stack-based bytecode로 낮춘 뒤 작은 VM으로 실행해 표면 문법은 유지한 채 실행 모델만 바꾸는 프로젝트다.
- [Parser Interpreter](Programming-Languages-Foundations/parser-interpreter/00-series-map.md) — `parser-interpreter`는 작은 함수형 코어 언어를 직접 토큰화하고, recursive descent parser로 AST를 만들고, tree-walk evaluator로 실행하는 프로젝트다.
- [Static Type Checking](Programming-Languages-Foundations/static-type-checking/00-series-map.md) — `static-type-checking`은 같은 toy language를 다시 파싱한 뒤 runtime에 넘기기 전에 어떤 오류를 미리 거를 수 있는지 정리하는 프로젝트다.

## 문서 구조

- `00-series-map.md` — 시리즈의 문제의식, source-of-truth, 읽는 순서를 설명하는 입구
- `01-evidence-ledger.md` — 소스코드, README, docs, 테스트, CLI를 바탕으로 phase별 근거를 모아 둔 문서
- `_structure-outline.md` — 최종 글이 어떤 장면 순서로 읽혀야 하는지 정리한 설계 메모
- `10-2026-03-13-reconstructed-development-log.md` — 구현 순서와 검증 신호를 한 흐름으로 다시 쓴 최종 글

## Legacy 정책

- `_legacy/2026-03-13-isolate-and-rewrite/`는 이전 초안을 보관하는 장소다.
- 현재 활성 문서는 `_legacy` 본문을 입력 근거로 사용하지 않는다.
- 비교 검토가 필요할 때만 `_legacy`를 참고한다.
