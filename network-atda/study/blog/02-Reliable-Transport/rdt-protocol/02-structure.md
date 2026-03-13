# RDT Protocol structure guide

## 이 글의 중심 질문

- rdt3.0과 Go-Back-N의 핵심 차이를 같은 채널 모델 위에서 어떻게 드러냈는가?
- 한 줄 답: rdt3.0`과 `Go-Back-N`을 같은 채널 모델 위에서 비교하는 신뢰 전송 과제입니다.

## 권장 흐름

1. 실행 표면과 entrypoint를 먼저 고정하기
2. 패킷 생성 규칙과 전송 루프를 비교 가능한 단위로 붙들기
3. 테스트와 남은 범위를 정리하기

## 꼭 살릴 근거

- `problem/Makefile`의 공개 target과 `make -C study/02-Reliable-Transport/rdt-protocol/problem test`
- `study/02-Reliable-Transport/rdt-protocol/python/src/gbn.py`의 `def gbn_send_receive`
- `study/02-Reliable-Transport/rdt-protocol/python/tests/test_rdt.py`의 `def test_make_and_parse_packet`

## 리라이트 주의점

- `RDT Protocol`를 개념 강의처럼 풀지 말고, 실제 파일과 CLI 순서로 보여 준다.
- 전체 로그를 덤프하지 말고 판단을 바꾼 줄만 남긴다.
- 마지막에는 실제 네트워크가 아니라 시뮬레이션 채널을 사용합니다. 같은 남은 경계를 사람 말로 다시 정리한다.
