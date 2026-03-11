# Selective Repeat

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | 이 저장소에서 `Go-Back-N` 다음 단계 학습을 위해 직접 보강한 Selective Repeat 프로젝트 |
| 정식 검증 | `make -C study/02-Reliable-Transport/selective-repeat/problem test` |

## 문제가 뭐였나
- 문제 배경: 이 저장소에서 `Go-Back-N` 다음 단계 학습을 위해 직접 보강한 Selective Repeat 프로젝트
- 이 단계에서의 역할: 교재 흐름상 당연히 이어져야 할 Selective Repeat를 별도 프로젝트로 분리해, 재전송 정책과 수신 버퍼링의 차이를 코드 수준에서 비교할 수 있게 합니다.

## 제공된 자료
- `problem/code/channel.py`: `rdt-protocol`과 공유하는 채널 helper
- `problem/code/packet.py`: 공유 packet helper
- `problem/code/selective_repeat_skeleton.py`: Selective Repeat skeleton
- `problem/data/test_messages.txt`: 테스트 메시지
- `problem/script/test_selective_repeat.sh`: 정식 검증 스크립트

## 이 레포의 답
- 한 줄 답: `Go-Back-N`의 한계를 보강하기 위해 추가한 선택 재전송 프로젝트입니다.
- 공개 답안 위치: `python/src/`
- 보조 공개 표면: `python/tests/`
- 보조 공개 표면: `docs/`
- 읽는 순서:
  1. `problem/README.md` - 문제 조건, 제공 자료, 성공 기준을 먼저 확인합니다.
  2. `python/README.md` - 현재 공개 답안 범위와 기준 명령을 확인합니다.
  3. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.
  4. `notion/README.md` - 공개 학습 노트이지만 엔트리포인트는 아닙니다.

## 어떻게 검증하나
- 실행: `make -C study/02-Reliable-Transport/selective-repeat/problem run-solution`
- 검증: `make -C study/02-Reliable-Transport/selective-repeat/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 무엇을 배웠나
- 패킷별 timer 관리
- 수신 버퍼와 in-order delivery
- ACKed 집합과 sender base 업데이트
- GBN과 SR의 효율 차이 비교

## 현재 한계
- 실제 병렬 스레드 모델은 아닙니다.
- sequence wraparound는 구현하지 않았습니다.
- 성능 비교 표는 아직 정리하지 않았습니다.
