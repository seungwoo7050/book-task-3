# IP and ICMP Packet Analysis 시리즈 맵

이 lab의 중심 질문은 "IPv4와 ICMP field가 실제 네트워크 동작을 어떤 서사로 엮어 주는가"다. 현재 답안은 두 trace를 역할별로 나눈다. traceroute trace는 TTL 증가, `Time Exceeded`, `Echo Reply`를 통해 path discovery를 보여 주고, fragmentation trace는 `Identification`, `MF`, `Fragment Offset`, `ip.len` 조합으로 datagram reassembly를 보여 준다.

## 이 lab를 읽는 질문

- TTL은 단순 숫자가 아니라 왜 traceroute에서 hop index처럼 읽히는가
- `Time Exceeded`와 `Echo Reply`는 같은 ICMP라도 어떤 다른 역할을 맡는가
- fragmentation에서는 어떤 필드가 같아야 같은 원본 datagram으로 묶을 수 있는가

## 이번에 사용한 근거

- `problem/README.md`
- `analysis/src/ip-icmp-analysis.md`
- `problem/Makefile`
- `problem/script/verify_answers.sh`
- 2026-03-14 재실행한 `filter-icmp`, `filter-fragments`

## 이번 재실행에서 고정한 사실

- Echo Request frames `#1/#3/#5`의 TTL은 `1/2/3`, `ip.id`는 `0x0fa0/0x0fa1/0x0fa2`다.
- `Time Exceeded` frames `#2/#4`는 `icmp type/code = 11/0`이다.
- final destination response frame `#6`은 `Echo Reply 0/0`이다.
- fragmentation trace는 frame `#1/#2/#3`이 모두 `ip.id=0x3039`를 공유하고 `MF`는 `1/1/0`으로 끝난다.
