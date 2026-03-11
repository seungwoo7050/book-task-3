# cs-core

## 이 저장소가 하려는 일

`cs-core`는 정답 모음집이 아니라 시스템 프로그래밍, 컴퓨터 시스템, 운영체제 breadth, 프로그래밍 언어 기초를 프로젝트로 학습하기 위한 저장소입니다.
목표는 두 가지입니다.

- 이 저장소 자체가 다시 따라 읽을 수 있는 학습 기록이 되는 것
- 이 저장소를 참고한 학생이 더 나은 자신의 공개용 포트폴리오 저장소를 설계할 수 있게 돕는 것

저장소는 현재 `study/` 안의 네 학습 트랙을 중심으로 읽는 편이 가장 자연스럽습니다.

- `legacy/`: 이전 학습 흔적을 보존하는 읽기 전용 참고 트리
- `study/`: 현재 기준으로 다시 설계한 학습용 작업 트리
- `docs/`: 저장소 전체 운영 기준과 재구성 메모

## 먼저 읽을 곳

1. [`study/README.md`](study/README.md): 전체 학습 트리의 사용법과 문서 규칙
2. [`study/Foundations-CSAPP/README.md`](study/Foundations-CSAPP/README.md): CS:APP 기반 기초 트랙
3. [`study/Systems-Programming/README.md`](study/Systems-Programming/README.md): 시스템 프로그래밍 심화 트랙
4. [`study/Operating-Systems-Internals/README.md`](study/Operating-Systems-Internals/README.md): scheduler, VM, filesystem, synchronization으로 이어지는 운영체제 breadth 트랙
5. [`study/Programming-Languages-Foundations/README.md`](study/Programming-Languages-Foundations/README.md): parser, typing, VM으로 이어지는 PL/컴파일러 기초 트랙
6. 각 프로젝트의 `README.md`: 문제 경계, 구현 경로, 검증 방법

## 트랙 개요

| 트랙 | 핵심 질문 | 시작 문서 |
|---|---|---|
| `Foundations-CSAPP` | 비트 연산, 어셈블리, 공격 모델, 아키텍처, 캐시를 어떻게 코드로 체득할까 | [`study/Foundations-CSAPP/README.md`](study/Foundations-CSAPP/README.md) |
| `Systems-Programming` | 프로세스, 시그널, 메모리 할당, 네트워크 I/O를 어떻게 직접 구현해 볼까 | [`study/Systems-Programming/README.md`](study/Systems-Programming/README.md) |
| `Operating-Systems-Internals` | scheduling, virtual memory, filesystem, synchronization을 작은 실험으로 어떻게 설명할까 | [`study/Operating-Systems-Internals/README.md`](study/Operating-Systems-Internals/README.md) |
| `Programming-Languages-Foundations` | parser, static typing, bytecode/VM을 같은 언어로 어떻게 설명할까 | [`study/Programming-Languages-Foundations/README.md`](study/Programming-Languages-Foundations/README.md) |

## 문서 원칙

- 설명 문장은 한국어를 기본으로 쓰고, 명령어·파일명·도구명·식별자는 영어 원문을 유지합니다.
- 공개 문서는 학습 가이드 역할을 해야 하며, 외부 과제의 정답 덤프처럼 보여서는 안 됩니다.
- `notion/`은 Notion 업로드용 문서이면서 저장소 안에 남겨 두는 현재판입니다.
- 현재 `notion/`은 `00`~`05` 세트로 유지하며, 특히 `05-development-timeline.md`는 새 환경에서 다시 따라 하기 위한 재현 문서로 씁니다.
- 현재 기준의 학습 노트는 `notion/`에 유지합니다. 더 긴 작업 로그가 필요하면 로컬 백업을 따로 둘 수 있지만, 새 프로젝트의 공개 표면에 `notion-archive/`를 필수로 두지는 않습니다.
- 공식 핸드아웃, 바이너리, 쿠키, 복원 툴체인은 계속 로컬 전용 자산으로 취급합니다.

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
- [`study/PUBLISHABILITY_REVIEW.md`](study/PUBLISHABILITY_REVIEW.md)
- [`study/TODO.md`](study/TODO.md)
