# IP and ICMP Packet Analysis blog

이 디렉터리는 `IP and ICMP Packet Analysis`를 `strict source-only` 기준으로 다시 읽는 blog 시리즈다. chronology는 `problem/README.md`, `problem/Makefile`, `analysis/src/ip-icmp-analysis.md`, `docs/concepts/wireshark-ip.md`를 기반으로 복원했다.

## source set
- [`../../../03-Packet-Analysis-Top-Down/ip-icmp/README.md`](../../../03-Packet-Analysis-Top-Down/ip-icmp/README.md)
- [`../../../03-Packet-Analysis-Top-Down/ip-icmp/problem/README.md`](../../../03-Packet-Analysis-Top-Down/ip-icmp/problem/README.md)
- [`../../../03-Packet-Analysis-Top-Down/ip-icmp/problem/Makefile`](../../../03-Packet-Analysis-Top-Down/ip-icmp/problem/Makefile)
- [`../../../03-Packet-Analysis-Top-Down/ip-icmp/analysis/src/ip-icmp-analysis.md`](../../../03-Packet-Analysis-Top-Down/ip-icmp/analysis/src/ip-icmp-analysis.md)
- [`../../../03-Packet-Analysis-Top-Down/ip-icmp/docs/concepts/wireshark-ip.md`](../../../03-Packet-Analysis-Top-Down/ip-icmp/docs/concepts/wireshark-ip.md)

## 읽는 순서
1. [`00-series-map.md`](00-series-map.md)
2. [`10-development-timeline.md`](10-development-timeline.md)
3. [`../../../03-Packet-Analysis-Top-Down/ip-icmp/README.md`](../../../03-Packet-Analysis-Top-Down/ip-icmp/README.md)

## 검증 진입점
- `make -C study/03-Packet-Analysis-Top-Down/ip-icmp/problem test`

## chronology 메모
- 이 프로젝트는 `TTL 변화`와 `fragmentation`을 두 덩어리로 나눠 읽는 것이 가장 안정적이었다.
