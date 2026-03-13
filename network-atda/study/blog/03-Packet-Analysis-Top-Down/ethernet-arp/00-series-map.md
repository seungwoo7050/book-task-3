# Ethernet and ARP Packet Analysis 시리즈 지도

## 이 프로젝트를 한 줄로

단 세 frame짜리 trace로 broadcast, unicast, EtherType, ARP 해석, 그리고 "없는 packet은 없다고 쓰기"를 배우는 기록이다.

## 시작 전에 고정한 자료

- 제공 trace: `problem/data/ethernet-arp.pcapng`
- 실행 진입점: `problem/Makefile`
- 사용자 답안: `study/03-Packet-Analysis-Top-Down/ethernet-arp/analysis/src/ethernet-arp-analysis.md`
- 보조 개념 문서: `docs/concepts/wireshark-link.md`

## 이 시리즈에서 따라갈 질문

1. Ethernet destination MAC만 보고도 broadcast와 unicast를 어디서 가를 수 있는가.
2. ARP request와 reply는 opcode, target MAC, Ethernet destination이 어떻게 달라지는가.
3. ARP reply 직후 다음 IPv4 frame이 resolved MAC을 실제로 쓰는지 어떻게 확인하는가.
4. trace에 HTTP packet이 없을 때, 그 사실 자체를 어떻게 evidence로 남길 것인가.

## 검증 명령

- ARP 전체: `make -C study/03-Packet-Analysis-Top-Down/ethernet-arp/problem filter-arp`
- Ethernet 헤더: `make -C study/03-Packet-Analysis-Top-Down/ethernet-arp/problem filter-ethernet`
- broadcast frame: `make -C study/03-Packet-Analysis-Top-Down/ethernet-arp/problem filter-broadcast`
- 답안 검증: `make -C study/03-Packet-Analysis-Top-Down/ethernet-arp/problem test`

## 글 구성

| 파일 | 역할 |
| :--- | :--- |
| `00-series-map.md` | 매우 짧은 trace를 어떤 순서로 읽어야 하는지 정한다. |
| `10-development-timeline.md` | broadcast request → unicast reply → resolved MAC 사용 확인 순으로 진행한다. |
