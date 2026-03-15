# Ethernet and ARP Packet Analysis 시리즈 맵

이 lab의 중심 질문은 "IP packet을 보내기 전에 링크 계층에서 어떤 주소 해석이 먼저 일어나는가"다. 현재 trace는 그 질문에 필요한 최소 장면만 보여 준다. frame `1`은 `ff:ff:ff:ff:ff:ff` broadcast로 `192.168.0.1`의 MAC을 묻고, frame `2`는 `66:77:88:99:aa:bb`가 자기 MAC이라고 답하며, frame `3`은 곧바로 그 MAC을 destination으로 쓰는 IPv4 frame이다.

## 이 lab를 읽는 질문

- 왜 ARP request의 Ethernet destination은 broadcast지만 reply는 unicast인가
- ARP payload 안의 IP/MAC 필드와 Ethernet header의 source/destination은 어떻게 대응되는가
- 같은 48-bit MAC 주소라도 ARP phase와 이후 IPv4 data phase에서 역할이 어떻게 바뀌는가

## 이번에 사용한 근거

- `problem/README.md`
- `analysis/src/ethernet-arp-analysis.md`
- `problem/Makefile`
- `problem/script/verify_answers.sh`
- 2026-03-14 재실행한 `filter-arp`, `filter-ethernet`, `filter-broadcast`

## 이번 재실행에서 고정한 사실

- frame `1`의 destination MAC은 `ff:ff:ff:ff:ff:ff`, `arp.opcode=1`, target MAC은 `00:00:00:00:00:00`이다.
- frame `2`의 destination MAC은 `00:11:22:33:44:55`, `arp.opcode=2`, sender MAC은 `66:77:88:99:aa:bb`이다.
- frame `3`의 EtherType은 `0x0800`이고 destination MAC은 frame `2`에서 알려 준 `66:77:88:99:aa:bb`와 일치한다.
- HTTP GET byte offset 질문은 현재 trace에 HTTP frame이 없어 `Not observable`로 남는다.
