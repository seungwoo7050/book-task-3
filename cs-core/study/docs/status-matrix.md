# status-matrix

2026-03-11 문서 정비 기준 상태표다. 각 프로젝트의 세부 명령은 해당 README를 따른다.

| 트랙 | 프로젝트 | 상태 | 대표 검증 경로 |
| --- | --- | --- | --- |
| `Foundations-CSAPP` | [`datalab`](../Foundations-CSAPP/datalab/README.md) | `verified (local-only asset)` | `problem: make restore-official && make verify-official`, `c/tests`, `cpp/tests` |
| `Foundations-CSAPP` | [`archlab`](../Foundations-CSAPP/archlab/README.md) | `verified (local-only asset)` | `problem: make restore-official && make verify-official`, `c`, `cpp` |
| `Foundations-CSAPP` | [`bomblab`](../Foundations-CSAPP/bomblab/README.md) | `verified (local-only asset)` | `problem: make restore-official && make verify-official`, `c`, `cpp` |
| `Foundations-CSAPP` | [`attacklab`](../Foundations-CSAPP/attacklab/README.md) | `verified (local-only asset)` | `problem: make restore-official && make verify-official`, `c`, `cpp` |
| `Foundations-CSAPP` | [`perflab`](../Foundations-CSAPP/perflab/README.md) | `public verified` | `problem: make status && make compile`, `c`, `cpp` |
| `Systems-Programming` | [`shlab`](../Systems-Programming/shlab/README.md) | `public verified` | `problem: make status`, `c`, `cpp` |
| `Systems-Programming` | [`malloclab`](../Systems-Programming/malloclab/README.md) | `public verified` | `problem: make clean && make`, `c`, `cpp` |
| `Systems-Programming` | [`proxylab`](../Systems-Programming/proxylab/README.md) | `public verified` | `problem: make clean && make`, `c`, `cpp` |
| `Operating-Systems-Internals` | [`scheduling-simulator`](../Operating-Systems-Internals/scheduling-simulator/README.md) | `public verified` | `problem: make test && make run-demo` |
| `Operating-Systems-Internals` | [`virtual-memory-lab`](../Operating-Systems-Internals/virtual-memory-lab/README.md) | `public verified` | `problem: make test && make run-demo` |
| `Operating-Systems-Internals` | [`filesystem-mini-lab`](../Operating-Systems-Internals/filesystem-mini-lab/README.md) | `public verified` | `problem: make test && make run-demo` |
| `Operating-Systems-Internals` | [`synchronization-contention-lab`](../Operating-Systems-Internals/synchronization-contention-lab/README.md) | `public verified` | `problem: make test && make run-demo` |
| `Programming-Languages-Foundations` | [`parser-interpreter`](../Programming-Languages-Foundations/parser-interpreter/README.md) | `public verified` | `python3 -m pytest`, `PYTHONPATH=src python3 -m parser_interpreter --demo all` |
| `Programming-Languages-Foundations` | [`static-type-checking`](../Programming-Languages-Foundations/static-type-checking/README.md) | `public verified` | `python3 -m pytest`, `PYTHONPATH=src python3 -m static_type_checking --demo all` |
| `Programming-Languages-Foundations` | [`bytecode-ir`](../Programming-Languages-Foundations/bytecode-ir/README.md) | `public verified` | `python3 -m pytest`, `PYTHONPATH=src python3 -m bytecode_ir --demo all --emit run` |
