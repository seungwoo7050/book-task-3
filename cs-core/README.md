# cs-core

## 이 저장소가 하려는 일

`cs-core`는 정답 모음집이 아니라 시스템 프로그래밍, 컴퓨터 시스템, 운영체제 breadth, 프로그래밍 언어 기초를 프로젝트로 학습하기 위한 저장소입니다.
목표는 두 가지입니다.

- 이 저장소 자체가 다시 따라 읽을 수 있는 학습 기록이 되는 것
- 이 저장소를 참고한 학생이 더 나은 자신의 공개용 포트폴리오 저장소를 설계할 수 있게 돕는 것

저장소는 현재 `study/` 안의 네 학습 트랙과 이를 설명하는 `docs/`를 중심으로 읽는 편이 가장 자연스럽습니다.

- `study/`: 현재 기준으로 유지하는 학습용 작업 트리
- `docs/`: 저장소 전체 운영 기준, 재구성 메모, 역사적 정리 문서
- `study/blog/`: 실제 소스코드, 테스트, git history를 기준으로 재구성한 장문 학습 로그

별도의 `legacy/` 디렉터리는 더 이상 두지 않습니다.
예전 재구성 맥락은 [`docs/legacy-study-rebuild-plan.md`](docs/legacy-study-rebuild-plan.md) 같은 문서 이름에만 남아 있습니다.

## 먼저 읽을 곳

1. [`study/README.md`](study/README.md): 전체 학습 트리의 사용법과 문서 규칙
2. [`study/Foundations-CSAPP/README.md`](study/Foundations-CSAPP/README.md): CS:APP 기반 기초 트랙
3. [`study/Systems-Programming/README.md`](study/Systems-Programming/README.md): 시스템 프로그래밍 구현 트랙
4. [`study/Operating-Systems-Internals/README.md`](study/Operating-Systems-Internals/README.md): scheduler, VM, filesystem, synchronization으로 이어지는 운영체제 breadth 트랙
5. [`study/Programming-Languages-Foundations/README.md`](study/Programming-Languages-Foundations/README.md): parser, typing, VM으로 이어지는 PL/컴파일러 기초 트랙
6. 각 프로젝트의 `README.md`: 문제 경계, 구현 경로, 검증 방법
7. [`study/blog/README.md`](study/blog/README.md): 소스코드 우선 재구성 blog 허브

## 트랙 개요

| 트랙 | 핵심 질문 | 시작 문서 |
|---|---|---|
| `Foundations-CSAPP` | 비트 연산, 어셈블리, 공격 모델, 아키텍처, 캐시를 어떻게 코드로 체득할까 | [`study/Foundations-CSAPP/README.md`](study/Foundations-CSAPP/README.md) |
| `Systems-Programming` | 프로세스, 시그널, 메모리 할당, 네트워크 I/O를 어떻게 직접 구현해 볼까 | [`study/Systems-Programming/README.md`](study/Systems-Programming/README.md) |
| `Operating-Systems-Internals` | scheduling, virtual memory, filesystem, synchronization을 작은 실험으로 어떻게 설명할까 | [`study/Operating-Systems-Internals/README.md`](study/Operating-Systems-Internals/README.md) |
| `Programming-Languages-Foundations` | parser, static typing, bytecode/VM을 같은 언어로 어떻게 설명할까 | [`study/Programming-Languages-Foundations/README.md`](study/Programming-Languages-Foundations/README.md) |

## 추천 학습 경로

처음부터 모든 프로젝트를 같은 우선순위로 보지 말고, 아래 `필수 코어`를 먼저 끝낸 뒤 관심 분야에 따라 `심화/선택`으로 갈라지는 편이 읽기 쉽습니다.

서버 개발자 관점에서 1회독 범위를 더 줄이고 싶다면 [`problem-subject-essential/README.md`](problem-subject-essential/README.md)를 먼저 읽는 편이 빠릅니다.
필수에 포함되지 않은 나머지 문제지는 [`problem-subject-elective/README.md`](problem-subject-elective/README.md)에 따로 모아 두었습니다.

### 필수 코어

| 순서 | 프로젝트 | 왜 먼저 보는가 |
|---|---|---|
| 1 | [`datalab`](study/Foundations-CSAPP/datalab/README.md) | 비트 연산, 정수 표현, 부동소수 경계처럼 뒤 프로젝트의 언어가 되는 기초를 다집니다. |
| 2 | [`archlab`](study/Foundations-CSAPP/archlab/README.md) | ISA, pipeline, control signal, cache-aware 사고를 시스템 구현 전에 잡습니다. |
| 3 | [`shlab`](study/Systems-Programming/shlab/README.md) | process, signal, job control을 직접 구현하며 시스템 프로그래밍 감각을 만듭니다. |
| 4 | [`malloclab`](study/Systems-Programming/malloclab/README.md) | 메모리 레이아웃과 allocator invariant를 손으로 유지하는 훈련을 합니다. |
| 5 | [`scheduling-simulator`](study/Operating-Systems-Internals/scheduling-simulator/README.md) | 운영체제 정책을 작은 실험으로 정리하며 breadth 트랙에 진입합니다. |
| 6 | [`virtual-memory-lab`](study/Operating-Systems-Internals/virtual-memory-lab/README.md) | locality, replacement, page fault를 운영체제 핵심 모델로 연결합니다. |
| 7 | [`parser-interpreter`](study/Programming-Languages-Foundations/parser-interpreter/README.md) | 언어를 읽고 실행하는 최소 단위를 직접 구현합니다. |
| 8 | [`static-type-checking`](study/Programming-Languages-Foundations/static-type-checking/README.md) | 같은 언어에 static reasoning을 추가하며 PL 기초를 완성합니다. |

### 심화/선택

| 갈래 | 프로젝트 | 선행 권장 |
|---|---|---|
| 보안/역공학 | [`bomblab`](study/Foundations-CSAPP/bomblab/README.md) -> [`attacklab`](study/Foundations-CSAPP/attacklab/README.md) | `datalab` 이후 |
| 성능/캐시 | [`perflab`](study/Foundations-CSAPP/perflab/README.md) | `archlab` 이후 |
| 네트워크 시스템 | [`proxylab`](study/Systems-Programming/proxylab/README.md) | `shlab`, `malloclab` 이후 |
| 운영체제 breadth 확장 | [`filesystem-mini-lab`](study/Operating-Systems-Internals/filesystem-mini-lab/README.md) -> [`synchronization-contention-lab`](study/Operating-Systems-Internals/synchronization-contention-lab/README.md) | `scheduling-simulator`, `virtual-memory-lab` 이후 |
| PL runtime 확장 | [`bytecode-ir`](study/Programming-Languages-Foundations/bytecode-ir/README.md) | `parser-interpreter`, `static-type-checking` 이후 |

## 문서 원칙

- 설명 문장은 한국어를 기본으로 쓰고, 명령어·파일명·도구명·식별자는 영어 원문을 유지합니다.
- 공개 문서는 학습 가이드 역할을 해야 하며, 외부 과제의 정답 덤프처럼 보여서는 안 됩니다.
- `notion/`은 Notion 업로드용 문서이면서 저장소 안에 남겨 두는 현재판입니다.
- 현재 `notion/`은 `00`~`05` 세트로 유지하며, 특히 `05-development-timeline.md`는 새 환경에서 다시 따라 하기 위한 재현 문서로 씁니다.
- 현재 기준의 학습 노트는 `notion/`에 유지합니다. 더 긴 작업 로그가 필요하면 로컬 백업을 따로 둘 수 있지만, 새 프로젝트의 공개 표면에 `notion-archive/`를 필수로 두지는 않습니다.
- 공식 핸드아웃, 바이너리, 쿠키, 복원 툴체인은 계속 로컬 전용 자산으로 취급합니다.
- 긴 chronology와 코드 기반 구현 서사는 `study/blog/`에서 별도로 유지합니다.

## 스포일러 정책

- `datalab`, `perflab`, `malloclab`, `proxylab`, `shlab`은 구현 원리와 검증 흐름을 공개합니다.
- `bomblab`, `attacklab`은 풀이 사고법과 워크플로는 친절히 설명하되, 외부 타깃에 직접 재사용 가능한 해답 덤프는 늘리지 않습니다.
- `archlab`은 공개 가능한 학습 산출물과 로컬 복원 자산의 경계를 명확히 나눕니다.

## 이 저장소를 포트폴리오로 확장하는 방법

- 프로젝트마다 "무엇을 배웠는가"를 한 문단으로 요약해 두고, 본인 저장소에서는 여기에 실행 캡처와 성능 비교를 추가합니다.
- `problem/`, 구현 디렉터리, `docs/`, `notion/`을 분리한 구조는 다른 학습 저장소에도 그대로 재사용할 수 있습니다.
- 공개 저장소를 만들 때는 공식 자산 재배포 가능 여부를 먼저 확인하고, 필요하면 이 저장소처럼 계약 경계와 복원 스크립트만 남깁니다.

## 기준 문서

- [`docs/legacy-study-rebuild-plan.md`](docs/legacy-study-rebuild-plan.md)
- [`study/docs/readme-contract.md`](study/docs/readme-contract.md)
- [`study/docs/status-matrix.md`](study/docs/status-matrix.md)
