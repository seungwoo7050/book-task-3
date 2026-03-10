# 04 지식 인덱스

## 핵심 용어
- **RTT**: 하나의 요청이 왕복하는 데 걸린 시간을 뜻한다.
- **packet loss**: 송신은 했지만 정해진 시간 안에 응답을 받지 못한 경우로 기록한다.
- **timeout**: UDP 애플리케이션이 손실을 감지하는 가장 단순한 장치다.
- **datagram**: 연결 상태 없이 독립적으로 전송되는 UDP 메시지 단위다.

## 다시 볼 파일
- [`../problem/code/udp_pinger_server.py`](../problem/code/udp_pinger_server.py): 제공 서버가 일부 요청을 버리고 응답을 대문자로 바꾸는 동작을 확인할 때 본다.
- [`../python/src/udp_pinger_client.py`](../python/src/udp_pinger_client.py): 송신 루프, timeout 처리, 통계 계산이 모두 모여 있다.
- [`../python/tests/test_udp_pinger.py`](../python/tests/test_udp_pinger.py): 성공 응답, 대문자 응답, 손실 처리의 최소 기준을 보여준다.
- [`../docs/concepts/rtt.md`](../docs/concepts/rtt.md): RTT 측정이 무엇을 의미하고 무엇을 의미하지 않는지 정리해 둔 문서다.

## 자주 쓰는 확인 명령
- `make -C study/Application-Protocols-and-Sockets/udp-pinger/problem test`
- `cd study/Application-Protocols-and-Sockets/udp-pinger/python/tests && python3 -m pytest test_udp_pinger.py -v`

## 참고 자료
- [`../docs/references/README.md`](../docs/references/README.md): 공개 문서를 정리할 때 다시 확인한 근거 모음
