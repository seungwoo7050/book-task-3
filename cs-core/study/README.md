# study

## 이 디렉터리가 맡는 역할

`study/`는 이 저장소의 실제 학습 작업 트리입니다.
과거 흔적을 별도 `legacy/` 트리로 남겨 두는 방식은 더 이상 쓰지 않고, 더 읽기 쉽고 다시 실행하기 쉬운 학습 아카이브를 현재 구조 안에서 유지하는 것이 목적입니다.

## 누구를 위한 문서인가

- CS:APP 계열 프로젝트를 처음부터 다시 따라가고 싶은 학습자
- 이미 과제를 해 봤지만 공개용 저장소 구조를 더 깔끔하게 만들고 싶은 사람
- 과거 재구성 메모보다 현재 기준의 정리된 구조부터 보고 싶은 사람

## 먼저 읽을 곳

1. [`Foundations-CSAPP/README.md`](Foundations-CSAPP/README.md)
2. [`Systems-Programming/README.md`](Systems-Programming/README.md)
3. [`Operating-Systems-Internals/README.md`](Operating-Systems-Internals/README.md)
4. [`Programming-Languages-Foundations/README.md`](Programming-Languages-Foundations/README.md)
5. 관심 있는 프로젝트의 `README.md`
6. 프로젝트 안의 `problem/README.md`, `docs/README.md`, `notion/README.md`

현재 레포에는 별도의 `legacy/` 디렉터리가 없습니다.
예전 맥락은 루트 `docs/` 아래의 계획 문서 이름에만 남겨 둡니다.

## 권장 학습 레이어

처음 읽는 사람 기준으로는 `필수 코어`를 먼저 따라가고, 이후 관심 분야에 따라 `심화/선택`으로 들어가는 편이 가장 자연스럽습니다.

### 필수 코어

| 순서 | 프로젝트 | 이유 |
|---|---|---|
| 1 | [`Foundations-CSAPP/datalab`](Foundations-CSAPP/datalab/README.md) | 비트와 표현 규칙을 먼저 잡아 이후 시스템/아키텍처 설명의 바닥을 만듭니다. |
| 2 | [`Foundations-CSAPP/archlab`](Foundations-CSAPP/archlab/README.md) | ISA와 pipeline 관점을 먼저 잡아 두면 뒤의 성능/시스템 문서가 훨씬 읽기 쉬워집니다. |
| 3 | [`Systems-Programming/shlab`](Systems-Programming/shlab/README.md) | 프로세스, 시그널, job control을 직접 구현하며 시스템 프로그래밍 핵심 계약을 익힙니다. |
| 4 | [`Systems-Programming/malloclab`](Systems-Programming/malloclab/README.md) | 메모리 레이아웃과 allocator invariant를 코드와 trace로 다룹니다. |
| 5 | [`Operating-Systems-Internals/scheduling-simulator`](Operating-Systems-Internals/scheduling-simulator/README.md) | 운영체제 정책을 작은 실험으로 정리합니다. |
| 6 | [`Operating-Systems-Internals/virtual-memory-lab`](Operating-Systems-Internals/virtual-memory-lab/README.md) | locality와 replacement를 OS 핵심 개념으로 연결합니다. |
| 7 | [`Programming-Languages-Foundations/parser-interpreter`](Programming-Languages-Foundations/parser-interpreter/README.md) | 언어를 읽고 실행하는 최소 단위를 직접 구현합니다. |
| 8 | [`Programming-Languages-Foundations/static-type-checking`](Programming-Languages-Foundations/static-type-checking/README.md) | 같은 언어에 static reasoning을 추가해 PL 기초를 마무리합니다. |

### 심화/선택

| 갈래 | 프로젝트 | 선행 권장 |
|---|---|---|
| 보안/역공학 | [`Foundations-CSAPP/bomblab`](Foundations-CSAPP/bomblab/README.md) -> [`Foundations-CSAPP/attacklab`](Foundations-CSAPP/attacklab/README.md) | `datalab` 이후 |
| 성능/캐시 | [`Foundations-CSAPP/perflab`](Foundations-CSAPP/perflab/README.md) | `archlab` 이후 |
| 네트워크 시스템 | [`Systems-Programming/proxylab`](Systems-Programming/proxylab/README.md) | `shlab`, `malloclab` 이후 |
| 운영체제 breadth 확장 | [`Operating-Systems-Internals/filesystem-mini-lab`](Operating-Systems-Internals/filesystem-mini-lab/README.md) -> [`Operating-Systems-Internals/synchronization-contention-lab`](Operating-Systems-Internals/synchronization-contention-lab/README.md) | `scheduling-simulator`, `virtual-memory-lab` 이후 |
| PL runtime 확장 | [`Programming-Languages-Foundations/bytecode-ir`](Programming-Languages-Foundations/bytecode-ir/README.md) | `parser-interpreter`, `static-type-checking` 이후 |

## 디렉터리 구조

```text
study/
  README.md
  Foundations-CSAPP/
  Systems-Programming/
  Operating-Systems-Internals/
  Programming-Languages-Foundations/
  PUBLISHABILITY_REVIEW.md
  TODO.md
  tools/
```

- `Foundations-CSAPP/`: 비트 연산부터 캐시/아키텍처까지 이어지는 기초 트랙
- `Systems-Programming/`: 셸, 메모리 할당기, 프록시를 통해 시스템 프로그래밍 감각을 다지는 트랙
- `Operating-Systems-Internals/`: scheduler, VM, filesystem, synchronization을 작은 실험으로 다시 묶는 운영체제 breadth 트랙
- `Programming-Languages-Foundations/`: parser, typing, bytecode/VM을 작은 언어로 이어 보는 PL/컴파일러 기초 트랙
- `PUBLISHABILITY_REVIEW.md`: 공개 가능한 자산과 로컬 전용 자산의 경계
- `TODO.md`: 남아 있는 유지보수와 확장 백로그

## 검증 방법

2026-03-10 문서 정비 기준으로 각 프로젝트 README에 적힌 명령을 그대로 실행하면 됩니다.

- 공식 자산이 필요한 프로젝트는 `problem/`에서 `make restore-official`과 `make verify-official`을 사용합니다.
- 공개 구현 검증은 각 `c/`, `cpp/`, `y86/` README에 적힌 명령을 따릅니다.
- 운영체제 breadth 프로젝트는 `problem/`에서 `make test`와 `make run-demo`를 사용합니다.
- Python 기반 PL 프로젝트는 각 디렉터리 README에 적힌 `pytest`와 CLI demo 명령을 따릅니다.
- 루트 수준 점검은 링크 검색과 정책 검색으로 수행합니다.

## 스포일러 경계

- 공개 README는 문제 목적, 읽는 순서, 검증 방법, 공개 범위를 설명합니다.
- 세부 개념 설명은 `docs/`에 두되, 외부 과제의 정답 덤프처럼 보이는 문서는 만들지 않습니다.
- `bomblab`과 `attacklab`은 워크플로와 사고법 중심으로 설명하고, 특정 비공개 타깃에 직접 재사용 가능한 정보는 공개하지 않습니다.

## 포트폴리오로 확장하는 힌트

- 프로젝트별 README 구조를 그대로 가져가도 개인 포트폴리오 저장소의 기본 뼈대로 충분합니다.
- 본인 저장소에서는 여기에 실행 캡처, 실패 사례 요약, 성능 전후 비교를 추가하면 설득력이 더 좋아집니다.
- `notion/`은 긴 글과 재현 로그를 담는 현재판으로 유지하고, 공개 README는 짧고 탐색 가능한 안내문에 집중하는 방식이 재사용하기 좋습니다.
- 특히 `05-development-timeline.md`를 꾸준히 갱신하면, 나중에 같은 프로젝트를 새 저장소에서 다시 세우기도 쉬워집니다.
