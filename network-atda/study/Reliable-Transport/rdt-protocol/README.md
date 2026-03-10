# RDT Protocol

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 rdt3.0/GBN 흐름을 현재 저장소 구조에 맞게 정리한 구현 프로젝트 |
| 정식 검증 | `make -C study/Reliable-Transport/rdt-protocol/problem test` |

## 한 줄 요약

`rdt3.0`과 `Go-Back-N`을 같은 채널 모델 위에서 비교하는 신뢰 전송 과제입니다.

## 왜 이 프로젝트가 필요한가

전송 계층 메커니즘을 가장 직접적으로 체험하는 중심 과제로, 이후 `Selective Repeat`를 비교할 때 기준점 역할을 합니다.

## 이런 학습자에게 맞습니다

- 손실과 손상이 있는 채널에서 ACK와 timer가 왜 필요한지 코드로 확인하고 싶은 학습자
- 상태 기계와 슬라이딩 윈도우를 구현 수준에서 이해하고 싶은 학습자

## 지금 바로 읽는 순서

1. `problem/README.md` - 구현 목표, 제공 자료, 성공 기준을 먼저 확인합니다.
2. `python/README.md` - 공개 구현 범위와 정식 검증 명령을 확인합니다.
3. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.
4. `notion/README.md` - 더 깊은 작업 기록과 회고가 필요할 때 참고합니다.

## 제공 자료

- `problem/code/channel.py`: 손실과 손상을 흉내 내는 비신뢰 채널
- `problem/code/packet.py`: 패킷 인코딩/디코딩 helper
- `problem/code/rdt3_skeleton.py`: rdt3.0 skeleton
- `problem/code/gbn_skeleton.py`: GBN skeleton
- `problem/data/test_messages.txt`: 테스트 메시지
- `problem/script/test_rdt.sh`: 정식 검증 스크립트

## 실행과 검증

- 실행: `make -C study/Reliable-Transport/rdt-protocol/problem run-solution-rdt3`
- 검증: `make -C study/Reliable-Transport/rdt-protocol/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 학습 포인트

- alternating bit와 cumulative ACK의 차이
- timeout 기반 재전송
- sliding window의 기본 구조
- 실제 네트워크 대신 시뮬레이션 채널에서 프로토콜을 검증하는 법

## 현재 한계

- 실제 네트워크가 아니라 시뮬레이션 채널을 사용합니다.
- GBN 성능 로그를 자동 수집하지 않습니다.
- 동시성 대신 단일 이벤트 루프를 사용합니다.

## 포트폴리오로 확장하기

- 패킷 흐름을 시퀀스 다이어그램으로 시각화하면 이해도가 크게 올라갑니다.
- 손실/손상 시나리오별 로그를 남기면 테스트 통과 이상의 설명력이 생깁니다.
- Selective Repeat와 성능 또는 재전송 횟수를 비교한 보고서를 덧붙이면 훨씬 강한 포트폴리오가 됩니다.
