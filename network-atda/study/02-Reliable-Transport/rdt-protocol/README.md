# RDT Protocol

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 rdt3.0/GBN 흐름을 현재 저장소 구조에 맞게 정리한 구현 프로젝트 |
| 정식 검증 | `make -C study/02-Reliable-Transport/rdt-protocol/problem test` |

## 문제가 뭐였나
- 문제 배경: `Computer Networking: A Top-Down Approach`의 rdt3.0/GBN 흐름을 현재 저장소 구조에 맞게 정리한 구현 프로젝트
- 이 단계에서의 역할: 전송 계층 메커니즘을 가장 직접적으로 체험하는 중심 과제로, 이후 `Selective Repeat`를 비교할 때 기준점 역할을 합니다.

## 제공된 자료
- `problem/code/channel.py`: 손실과 손상을 흉내 내는 비신뢰 채널
- `problem/code/packet.py`: 패킷 인코딩/디코딩 helper
- `problem/code/rdt3_skeleton.py`: rdt3.0 skeleton
- `problem/code/gbn_skeleton.py`: GBN skeleton
- `problem/data/test_messages.txt`: 테스트 메시지
- `problem/script/test_rdt.sh`: 정식 검증 스크립트

## 이 레포의 답
- 한 줄 답: `rdt3.0`과 `Go-Back-N`을 같은 채널 모델 위에서 비교하는 신뢰 전송 과제입니다.
- 공개 답안 위치: `python/src/`
- 보조 공개 표면: `python/tests/`
- 보조 공개 표면: `docs/`
- 보조 공개 표면: `study/blog/02-Reliable-Transport/rdt-protocol/`
- 읽는 순서:
  1. `problem/README.md` - 문제 조건, 제공 자료, 성공 기준을 먼저 확인합니다.
  2. `python/README.md` - 현재 공개 답안 범위와 기준 명령을 확인합니다.
  3. `../../blog/02-Reliable-Transport/rdt-protocol/README.md` - 실제 소스 기준의 개발 chronology를 따라갑니다.
  4. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.
  5. `notion/README.md` - 공개 학습 노트이지만 엔트리포인트는 아닙니다.

## 어떻게 검증하나
- 실행: `make -C study/02-Reliable-Transport/rdt-protocol/problem run-solution-rdt3`
- 검증: `make -C study/02-Reliable-Transport/rdt-protocol/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 무엇을 배웠나
- alternating bit와 cumulative ACK의 차이
- timeout 기반 재전송
- sliding window의 기본 구조
- 실제 네트워크 대신 시뮬레이션 채널에서 프로토콜을 검증하는 법

## 현재 한계
- 실제 네트워크가 아니라 시뮬레이션 채널을 사용합니다.
- GBN 성능 로그를 자동 수집하지 않습니다.
- 동시성 대신 단일 이벤트 루프를 사용합니다.
