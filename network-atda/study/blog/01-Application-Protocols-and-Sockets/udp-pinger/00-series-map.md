# UDP Pinger 시리즈 지도

## 이 프로젝트를 한 줄로

"연결이 없는 소켓"이 실제 코드에서 무엇을 의미하는지를 10번의 ping과 timeout, RTT 통계로 직접 느끼는 과제다. Web Server에서는 `accept()`가 연결을 보장했지만, UDP에서는 응답이 올지 안 올지를 프로그래머가 직접 판단해야 한다.

## 문제 구조
- 제공물: `problem/code/udp_pinger_server.py` (30% 손실 서버), `problem/code/udp_pinger_client_skeleton.py`
- 답안: `python/src/udp_pinger_client.py`, `python/tests/test_udp_pinger.py`
- 검증: `make -C study/01-Application-Protocols-and-Sockets/udp-pinger/problem test`

## 이 시리즈에서 따라갈 질문
1. `SOCK_DGRAM`이 `SOCK_STREAM`과 가장 처음 부딪히는 차이는 무엇인가
2. `settimeout(1)`이 없으면 클라이언트는 어떻게 되는가
3. 손실이 있는 환경에서 통계를 모으려면 루프를 어떻게 설계해야 하는가
4. 테스트가 비결정적인 서버를 상대로 무엇을 보장할 수 있는가

## 글 목록
| 번호 | 파일 | 범위 |
| :--- | :--- | :--- |
| `10` | [`10-development-timeline.md`](10-development-timeline.md) | skeleton 분석부터 RTT 통계 완성까지 |
