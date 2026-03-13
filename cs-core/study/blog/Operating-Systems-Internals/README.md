# Operating-Systems-Internals 블로그 트랙

운영체제 내부 동작을 작은 실험으로 끌어내린 트랙이다. scheduler, virtual memory, journaling, synchronization을 모두 장난감 모델로 축소했지만, 각 프로젝트는 상태 전이와 복구 규칙을 실제 CLI와 테스트로 끝까지 확인하는 데 초점을 둔다.

이 트랙의 문서는 모두 같은 원칙을 따른다. 프로젝트별 `00-series-map.md`에서 읽는 순서를 잡고, `01-evidence-ledger.md`에서 근거를 확인한 뒤, `_structure-outline.md`와 최종 blog로 넘어간다. `_legacy`는 비교용 보관소일 뿐 현재 시리즈의 입력 근거가 아니다.

## 프로젝트 가이드

### [Filesystem Mini Lab](filesystem-mini-lab/)

`filesystem-mini-lab`은 root-only toy filesystem으로 inode allocation, block allocation, metadata journaling, recovery를 작은 JSON disk image 위에서 설명하는 실험이다.

- 시리즈 입구: [filesystem-mini-lab/00-series-map.md](filesystem-mini-lab/00-series-map.md)
- 핵심 질문: inode/block allocator를 먼저 세운 뒤 journal prepare/commit/apply/recover가 왜 별도 단계여야 하는지 따라간다.
- 대표 검증 명령: `make test && make run-demo`

### [Scheduling Simulator](scheduling-simulator/)

`scheduling-simulator`는 단일 CPU 위에서 scheduling policy가 waiting time, response time, turnaround time을 어떻게 바꾸는지 replay와 지표로 보여 주는 실험이다.

- 시리즈 입구: [scheduling-simulator/00-series-map.md](scheduling-simulator/00-series-map.md)
- 핵심 질문: workload fixture와 공통 시뮬레이션 루프를 먼저 세운 뒤, policy별 차이가 replay/metric으로 어떻게 보이는지 따라간다.
- 대표 검증 명령: `make test && make run-demo`

### [Synchronization Contention Lab](synchronization-contention-lab/)

`synchronization-contention-lab`는 mutex, semaphore, condition variable이 서로 다른 contention pattern에서 correctness와 timing을 어떻게 드러내는지 보여 주는 C 실험이다.

- 시리즈 입구: [synchronization-contention-lab/00-series-map.md](synchronization-contention-lab/00-series-map.md)
- 핵심 질문: counter/gate/buffer 세 시나리오를 먼저 세우고, mutex/semaphore/condvar가 각 시나리오에서 무엇을 보장하는지 따라간다.
- 대표 검증 명령: `make test && make run-demo`

### [Virtual Memory Lab](virtual-memory-lab/)

`virtual-memory-lab`는 page reference trace를 따라가며 replacement policy와 locality가 page fault 수를 어떻게 바꾸는지 보여 주는 실험이다.

- 시리즈 입구: [virtual-memory-lab/00-series-map.md](virtual-memory-lab/00-series-map.md)
- 핵심 질문: trace loader와 공통 simulator를 먼저 세운 뒤, replacement policy와 dirty-page/writeback 규칙이 결과 표에 어떻게 반영되는지 따라간다.
- 대표 검증 명령: `make test && make run-demo`

## 공통 문서 구조

- `00-series-map.md` — 왜 이 프로젝트를 이런 순서로 읽어야 하는지 설명하는 입구
- `01-evidence-ledger.md` — source-first 근거와 phase별 코드/CLI 앵커를 모아 둔 문서
- `_structure-outline.md` — 최종 글의 장면 배치와 전환 문장을 정리한 편집 메모
- `10-2026-03-13-reconstructed-development-log.md` — 구현 순서와 검증 신호를 하나의 서사로 다시 쓴 최종 blog
