# ICMP Pinger 시리즈 맵

이 lab의 중심 질문은 "ICMP Echo Request/Reply를 직접 만들고 읽으려면 운영체제에 무엇을 맡기지 않아야 하는가"다. 현재 구현은 `internet_checksum()`, `build_echo_request()`, `parse_echo_reply()`, `ping()` 네 축으로 이 질문에 답한다. header checksum도 직접 만들고, payload timestamp도 직접 넣고, reply에서 IP header length를 읽어 ICMP section을 분리한다.

## 이 lab를 읽는 질문

- RFC 1071 checksum 계산은 코드에서 어디까지 손으로 처리되는가
- Echo Reply parse에서 왜 ICMP header보다 먼저 IP header length를 읽어야 하는가
- deterministic test와 live raw-socket run은 무엇을 다르게 검증하는가

## 이번에 사용한 근거

- `problem/README.md`
- `python/src/icmp_pinger.py`
- `python/tests/test_icmp_pinger.py`
- `problem/Makefile`
- 2026-03-14 재실행한 deterministic test와 live rerun 시도

## 이번 재실행에서 고정한 사실

- checksum 함수는 odd-length data padding과 carry fold를 모두 직접 처리한다.
- Echo Request payload는 `double` timestamp 8 bytes다.
- reply parse는 outer IPv4 header의 `IHL`을 읽어 ICMP header offset을 계산한다.
- unit tests는 checksum invariants, packet layout, fake raw socket 기반 RTT/loss 통계까지 고정한다.
