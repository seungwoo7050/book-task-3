# Ethernet and ARP Packet Analysis blog

이 디렉터리는 `Ethernet and ARP Packet Analysis`를 `strict source-only` 기준으로 다시 읽는 blog 시리즈다. chronology는 `problem/README.md`, `problem/Makefile`, `analysis/src/ethernet-arp-analysis.md`, `docs/concepts/wireshark-link.md`를 기반으로 재구성했다.

## source set
- [`../../../03-Packet-Analysis-Top-Down/ethernet-arp/README.md`](../../../03-Packet-Analysis-Top-Down/ethernet-arp/README.md)
- [`../../../03-Packet-Analysis-Top-Down/ethernet-arp/problem/README.md`](../../../03-Packet-Analysis-Top-Down/ethernet-arp/problem/README.md)
- [`../../../03-Packet-Analysis-Top-Down/ethernet-arp/problem/Makefile`](../../../03-Packet-Analysis-Top-Down/ethernet-arp/problem/Makefile)
- [`../../../03-Packet-Analysis-Top-Down/ethernet-arp/analysis/src/ethernet-arp-analysis.md`](../../../03-Packet-Analysis-Top-Down/ethernet-arp/analysis/src/ethernet-arp-analysis.md)
- [`../../../03-Packet-Analysis-Top-Down/ethernet-arp/docs/concepts/wireshark-link.md`](../../../03-Packet-Analysis-Top-Down/ethernet-arp/docs/concepts/wireshark-link.md)

## 읽는 순서
1. [`00-series-map.md`](00-series-map.md)
2. [`10-development-timeline.md`](10-development-timeline.md)
3. [`../../../03-Packet-Analysis-Top-Down/ethernet-arp/README.md`](../../../03-Packet-Analysis-Top-Down/ethernet-arp/README.md)

## 검증 진입점
- `make -C study/03-Packet-Analysis-Top-Down/ethernet-arp/problem test`

## chronology 메모
- trace가 매우 작기 때문에 "없는 HTTP packet을 억지로 찾지 않는다"는 원칙이 chronology의 중심에 있다.
