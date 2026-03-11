# curriculum-map

`cs-core/study`는 정답 모음이 아니라 "문제 계약 -> 실행 가능한 답 -> 검증 -> 학습 노트"가 분리된 multi-track 학습 아카이브다.

## 커리큘럼 뼈대

| 순서 | 트랙 | 핵심 질문 | 시작 프로젝트 |
| --- | --- | --- | --- |
| 1 | `Foundations-CSAPP` | 비트 표현, ISA, 캐시, 역공학의 바닥을 어떻게 세울까 | [`datalab`](../Foundations-CSAPP/datalab/README.md) |
| 2 | `Systems-Programming` | 프로세스, 시그널, 메모리, 네트워크를 직접 구현하면 어떤 계약이 보일까 | [`shlab`](../Systems-Programming/shlab/README.md) |
| 3 | `Operating-Systems-Internals` | scheduler, VM, filesystem, synchronization을 작은 실험으로 어떻게 재설명할까 | [`scheduling-simulator`](../Operating-Systems-Internals/scheduling-simulator/README.md) |
| 4 | `Programming-Languages-Foundations` | parser, type checker, VM을 같은 언어 표면으로 어떻게 이어 볼까 | [`parser-interpreter`](../Programming-Languages-Foundations/parser-interpreter/README.md) |

## 권장 읽기 순서

### 필수 코어

1. [`Foundations-CSAPP/datalab`](../Foundations-CSAPP/datalab/README.md)
2. [`Foundations-CSAPP/archlab`](../Foundations-CSAPP/archlab/README.md)
3. [`Systems-Programming/shlab`](../Systems-Programming/shlab/README.md)
4. [`Systems-Programming/malloclab`](../Systems-Programming/malloclab/README.md)
5. [`Operating-Systems-Internals/scheduling-simulator`](../Operating-Systems-Internals/scheduling-simulator/README.md)
6. [`Operating-Systems-Internals/virtual-memory-lab`](../Operating-Systems-Internals/virtual-memory-lab/README.md)
7. [`Programming-Languages-Foundations/parser-interpreter`](../Programming-Languages-Foundations/parser-interpreter/README.md)
8. [`Programming-Languages-Foundations/static-type-checking`](../Programming-Languages-Foundations/static-type-checking/README.md)

### 심화/선택

- 보안/역공학: [`bomblab`](../Foundations-CSAPP/bomblab/README.md) -> [`attacklab`](../Foundations-CSAPP/attacklab/README.md)
- 성능/캐시: [`perflab`](../Foundations-CSAPP/perflab/README.md)
- 네트워크 시스템: [`proxylab`](../Systems-Programming/proxylab/README.md)
- 운영체제 breadth 확장: [`filesystem-mini-lab`](../Operating-Systems-Internals/filesystem-mini-lab/README.md) -> [`synchronization-contention-lab`](../Operating-Systems-Internals/synchronization-contention-lab/README.md)
- PL runtime 확장: [`bytecode-ir`](../Programming-Languages-Foundations/bytecode-ir/README.md)

## 설계 원칙

- 루트에서는 15개 프로젝트를 짧게 훑고, 세부 reasoning은 하위 문서로 내려 보낸다.
- 각 프로젝트는 `문제`, `이 레포의 답`, `검증 시작점`이 README 첫 화면에서 바로 보이도록 유지한다.
- 트랙 간 브리지는 개념 선행 관계로 설명하고, 구현 디렉터리 구조는 현재 레포 관성을 유지한다.
