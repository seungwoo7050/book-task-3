# Traceroute 시리즈 맵

이 lab의 중심 질문은 "ICMP Time Exceeded를 받는다"가 아니라 "어느 probe에 대한 어떤 ICMP reply인지 어떻게 안정적으로 판정하는가"다. 현재 구현은 `build_probe_port()`로 TTL과 probe index를 port space에 매핑하고, `parse_icmp_response()`가 embedded UDP dest port를 다시 읽어 매칭한다. 종료 조건도 destination IP로부터 `ICMP type 3 code 3`이 오느냐로 명확하게 고정한다.

## 이 lab를 읽는 질문

- probe마다 별도 UDP dest port를 만드는 이유는 무엇인가
- ICMP outer header가 아니라 embedded original datagram을 다시 읽어야 하는 이유는 무엇인가
- hop line formatting은 path discovery logic과 어떻게 분리돼 있는가

## 이번에 사용한 근거

- `problem/README.md`
- `python/src/traceroute.py`
- `python/tests/test_traceroute.py`
- `problem/Makefile`
- 2026-03-14 재실행한 unit tests와 live rerun 시도

## 이번 재실행에서 고정한 사실

- `build_probe_port(1,0,3)=33434`, `(2,0,3)=33437`처럼 TTL/probe index가 stable port mapping을 만든다.
- `parse_icmp_response()`는 `(icmp_type, icmp_code, embedded_udp_dest_port)`를 반환한다.
- synthetic integration test는 hop `10.0.0.1 -> 10.0.1.1 -> 203.0.113.9`까지 출력하고 ત્યાં서 종료한다.
- live rerun은 현재 환경에서 5초 내 완료되지 않았다.
