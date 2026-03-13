# Systems-Programming 블로그 트랙

시스템 프로그래밍 트랙은 allocator, shell, proxy처럼 운영체제와 네트워크의 경계에 있는 프로그램을 다시 읽는다. 공통 질문은 언제나 같다. 상태를 어떻게 관리했고, 어떤 invariant를 먼저 고정했으며, 어떤 테스트로 그 약속을 닫았는가.

이 트랙의 문서는 모두 같은 원칙을 따른다. 프로젝트별 `00-series-map.md`에서 읽는 순서를 잡고, `01-evidence-ledger.md`에서 근거를 확인한 뒤, `_structure-outline.md`와 최종 blog로 넘어간다. `_legacy`는 비교용 보관소일 뿐 현재 시리즈의 입력 근거가 아니다.

## 프로젝트 가이드

### [Malloc Lab](malloclab/)

`malloclab`은 힙 블록 레이아웃, 정렬 규칙, explicit free list, coalescing, `realloc`을 한 번에 다루는 allocator 프로젝트다.

- 시리즈 입구: [malloclab/00-series-map.md](malloclab/00-series-map.md)
- 핵심 질문: 힙 메타데이터, free list, `realloc`/coalescing이 한 번에 얽히는 allocator를 invariants 중심으로 복원한다.
- 대표 검증 명령: `make clean && make test`

### [Proxy Lab](proxylab/)

`proxylab`은 HTTP 요청 파싱, header 정규화, concurrent connection 처리, in-memory cache 설계를 하나의 프록시 구현으로 묶는 프로젝트다.

- 시리즈 입구: [proxylab/00-series-map.md](proxylab/00-series-map.md)
- 핵심 질문: HTTP parsing, request rewriting, concurrent serve, cache promotion이 한 파일에서 어떻게 나뉘는지 순서대로 풀어낸다.
- 대표 검증 명령: `make clean && make test`

### [Shell Lab](shlab/)

`shlab`은 프로세스 그룹, foreground/background job control, `SIGCHLD` 처리, `fork` 주변 race를 작은 셸 구현으로 익히는 프로젝트다.

- 시리즈 입구: [shlab/00-series-map.md](shlab/00-series-map.md)
- 핵심 질문: command parsing과 builtin에서 출발해, `SIGCHLD`/`waitfg` race discipline이 왜 마지막 병목이 되는지 따라간다.
- 대표 검증 명령: `make clean && make test`

## 공통 문서 구조

- `00-series-map.md` — 왜 이 프로젝트를 이런 순서로 읽어야 하는지 설명하는 입구
- `01-evidence-ledger.md` — source-first 근거와 phase별 코드/CLI 앵커를 모아 둔 문서
- `_structure-outline.md` — 최종 글의 장면 배치와 전환 문장을 정리한 편집 메모
- `10-2026-03-13-reconstructed-development-log.md` — 구현 순서와 검증 신호를 하나의 서사로 다시 쓴 최종 blog
