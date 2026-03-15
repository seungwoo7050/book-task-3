# UDP Pinger Evidence Ledger

## 이번에 읽은 자료

- `problem/README.md`
- `python/src/udp_pinger_client.py`
- `python/tests/test_udp_pinger.py`

## 핵심 코드 근거

- `PING_COUNT = 10`
- `TIMEOUT = 1`
- `send_time`/`recv_time` 차이로 RTT 계산
- `socket.timeout` 예외를 손실로 처리
- `rtt_list` 기반으로 min/avg/max 계산

## 테스트/검증 근거

`make -C network-atda/study/01-Application-Protocols-and-Sockets/udp-pinger/problem test`

재실행 결과:

- 응답/timeout 혼합 시나리오 실제 출력 확인
- 통계 출력 확인
- 테스트 `3 passed`

## 이번에 남긴 해석

- 이 lab의 핵심은 reliable transport가 아니라 loss visibility다.
- 제공 서버가 일부 패킷을 버리기 때문에 "모든 ping 성공"이 아니라 "적어도 일부 응답과 일부 손실을 견디는 출력"이 중요하다.
