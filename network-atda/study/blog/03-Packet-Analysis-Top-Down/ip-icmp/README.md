# IP and ICMP Packet Analysis Blog

이 문서 묶음은 `ip-icmp` 랩을 "IPv4 header field 소개"보다 "traceroute와 fragmentation이라는 두 장면을 통해 네트워크 계층이 무엇을 직접 드러내는가"라는 질문으로 다시 읽는다. 현재 공개 답안은 `ip-traceroute.pcapng`에서 TTL 증가와 `Time Exceeded`를, `ip-fragmentation.pcapng`에서 같은 `ip.id`를 가진 세 fragment와 reassembly 경계를 해석한다. 따라서 이 lab의 핵심은 필드 목록 암기가 아니라, IP header와 ICMP control message가 실제 네트워크 동작을 설명하는 방식에 있다.

이번 재작성은 기존 blog 본문이 아니라 다음 근거만 사용했다.

- 문제 정의: `study/03-Packet-Analysis-Top-Down/ip-icmp/problem/README.md`
- 답안 경계: `README.md`, `analysis/README.md`, `analysis/src/ip-icmp-analysis.md`
- 실제 검증: 2026-03-14 재실행한 `make -C network-atda/study/03-Packet-Analysis-Top-Down/ip-icmp/problem test`
- 보조 필터: `make -C .../ip-icmp/problem filter-icmp`, `filter-fragments`

## 읽는 순서

1. [`00-series-map.md`](./00-series-map.md)
2. [`10-development-timeline.md`](./10-development-timeline.md)
3. [`01-evidence-ledger.md`](./01-evidence-ledger.md)
4. [`02-structure.md`](./02-structure.md)

## 이번에 다시 확인한 검증 상태

- 정식 검증 명령: `make -C network-atda/study/03-Packet-Analysis-Top-Down/ip-icmp/problem test`
- 결과: `PASS: ip-icmp answer file passed content verification`
- 보조 필터에서 재확인한 값:
  - traceroute probe TTL: `1 -> 2 -> 3`
  - `Time Exceeded` source routers: `10.0.0.1`, `172.16.0.1`
  - fragmentation trace: same `ip.id=0x3039`, offsets `0 / 175 / 350`

## 지금 남기는 한계

- IPv6와 ICMPv6는 현재 범위 밖이다.
- traceroute trace가 짧아 router 2개와 final destination까지만 보인다.
- fragmentation은 synthetic trace라 MTU discovery나 router-side fragmentation 정책 비교까지는 다루지 않는다.
