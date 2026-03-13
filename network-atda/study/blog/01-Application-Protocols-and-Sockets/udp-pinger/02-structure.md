# UDP Pinger structure guide

## 이 글의 중심 질문

- 연결 없는 UDP에서 손실과 timeout을 클라이언트 쪽 코드로 어떻게 드러냈는가?
- 한 줄 답: UDP의 비연결성과 timeout 기반 손실 처리를 RTT 측정 과제로 묶은 구현입니다.

## 권장 흐름

1. 실행 표면과 entrypoint를 먼저 고정하기
2. 반복 ping, timeout, RTT 통계를 한 루프로 붙들기
3. 테스트와 남은 범위를 정리하기

## 꼭 살릴 근거

- `problem/Makefile`의 공개 target과 `make -C study/01-Application-Protocols-and-Sockets/udp-pinger/problem test`
- `study/01-Application-Protocols-and-Sockets/udp-pinger/python/src/udp_pinger_client.py`의 `for seq in range(1, PING_COUNT + 1):`
- `study/01-Application-Protocols-and-Sockets/udp-pinger/python/tests/test_udp_pinger.py`의 `def test_server_responds_to_ping`

## 리라이트 주의점

- `UDP Pinger`를 개념 강의처럼 풀지 말고, 실제 파일과 CLI 순서로 보여 준다.
- 전체 로그를 덤프하지 말고 판단을 바꾼 줄만 남긴다.
- 마지막에는 패킷 순서 역전은 별도 처리하지 않습니다. 같은 남은 경계를 사람 말로 다시 정리한다.
