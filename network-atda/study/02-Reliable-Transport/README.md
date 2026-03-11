# 02. Reliable Transport

손실과 손상이 있는 채널에서 송신자와 수신자가 어떤 상태를 기억해야 하는지 시뮬레이션으로 확인하는 단계입니다.

## 프로젝트 카탈로그

| 프로젝트 | 문제 | 이 레포의 답 | 검증 | 상태 | 왜 이 단계에 있는가 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`RDT Protocol`](rdt-protocol/README.md) | `Computer Networking: A Top-Down Approach`의 rdt3.0/GBN 흐름을 현재 저장소 구조에 맞게 정리한 구현 프로젝트 | `python/src/` | `make -C study/02-Reliable-Transport/rdt-protocol/problem test` | `verified` | 전송 계층 메커니즘을 가장 직접적으로 체험하는 중심 과제로, 이후 `Selective Repeat`를 비교할 때 기준점 역할을 합니다. |
| [`Selective Repeat`](selective-repeat/README.md) | 이 저장소에서 `Go-Back-N` 다음 단계 학습을 위해 직접 보강한 Selective Repeat 프로젝트 | `python/src/` | `make -C study/02-Reliable-Transport/selective-repeat/problem test` | `verified` | 교재 흐름상 당연히 이어져야 할 Selective Repeat를 별도 프로젝트로 분리해, 재전송 정책과 수신 버퍼링의 차이를 코드 수준에서 비교할 수 있게 합니다. |

## 공통 읽기 순서

1. 프로젝트 README에서 문제, 답, 검증 명령을 먼저 확인합니다.
2. `problem/README.md`에서 제공 자료와 성공 기준을 확인합니다.
3. 구현형 과제는 `python/README.md` 또는 `cpp/README.md`, 분석형 과제는 `analysis/README.md`로 내려갑니다.
4. `docs/README.md`는 개념을 다시 확인할 때만 참고하고, `notion/README.md`는 보조 기록으로만 읽습니다.
