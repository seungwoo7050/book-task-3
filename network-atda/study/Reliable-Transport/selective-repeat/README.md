# Selective Repeat

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | 이 저장소에서 `Go-Back-N` 다음 단계 학습을 위해 직접 보강한 Selective Repeat 프로젝트 |
| 정식 검증 | `make -C study/Reliable-Transport/selective-repeat/problem test` |

## 한 줄 요약

`Go-Back-N`의 한계를 보강하기 위해 추가한 선택 재전송 프로젝트입니다.

## 왜 이 프로젝트가 필요한가

교재 흐름상 당연히 이어져야 할 Selective Repeat를 별도 프로젝트로 분리해, 재전송 정책과 수신 버퍼링의 차이를 코드 수준에서 비교할 수 있게 합니다.

## 이런 학습자에게 맞습니다

- GBN과 SR의 차이를 구현으로 직접 비교하고 싶은 학습자
- 개별 timer와 수신 버퍼가 왜 필요한지 체감하고 싶은 학습자

## 지금 바로 읽는 순서

1. `problem/README.md` - 구현 목표, 제공 자료, 성공 기준을 먼저 확인합니다.
2. `python/README.md` - 공개 구현 범위와 정식 검증 명령을 확인합니다.
3. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.
4. `notion/README.md` - 더 깊은 작업 기록과 회고가 필요할 때 참고합니다.

## 제공 자료

- `problem/code/channel.py`: `rdt-protocol`과 공유하는 채널 helper
- `problem/code/packet.py`: 공유 packet helper
- `problem/code/selective_repeat_skeleton.py`: Selective Repeat skeleton
- `problem/data/test_messages.txt`: 테스트 메시지
- `problem/script/test_selective_repeat.sh`: 정식 검증 스크립트

## 실행과 검증

- 실행: `make -C study/Reliable-Transport/selective-repeat/problem run-solution`
- 검증: `make -C study/Reliable-Transport/selective-repeat/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 학습 포인트

- 패킷별 timer 관리
- 수신 버퍼와 in-order delivery
- ACKed 집합과 sender base 업데이트
- GBN과 SR의 효율 차이 비교

## 현재 한계

- 실제 병렬 스레드 모델은 아닙니다.
- sequence wraparound는 구현하지 않았습니다.
- 성능 비교 표는 아직 정리하지 않았습니다.

## 포트폴리오로 확장하기

- 재전송 횟수, 평균 지연, 버퍼 점유를 GBN과 비교하면 프로젝트 완성도가 크게 올라갑니다.
- window 시각화나 ACK 타임라인을 붙이면 설명력이 높아집니다.
- sequence wraparound와 더 큰 window 실험을 후속 과제로 제안하면 자연스러운 확장 포인트가 됩니다.
