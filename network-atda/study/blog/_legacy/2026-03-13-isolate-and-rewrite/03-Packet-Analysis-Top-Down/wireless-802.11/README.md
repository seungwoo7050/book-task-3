# 802.11 Wireless Packet Analysis blog

이 디렉터리는 `802.11 Wireless Packet Analysis`를 `strict source-only` 기준으로 다시 읽는 blog 시리즈다. chronology는 `problem/README.md`, `problem/Makefile`, `analysis/src/wireless-analysis.md`, `docs/concepts/wireshark-wireless.md`를 바탕으로 재구성했다.

## source set
- [`../../../03-Packet-Analysis-Top-Down/wireless-802.11/README.md`](../../../03-Packet-Analysis-Top-Down/wireless-802.11/README.md)
- [`../../../03-Packet-Analysis-Top-Down/wireless-802.11/problem/README.md`](../../../03-Packet-Analysis-Top-Down/wireless-802.11/problem/README.md)
- [`../../../03-Packet-Analysis-Top-Down/wireless-802.11/problem/Makefile`](../../../03-Packet-Analysis-Top-Down/wireless-802.11/problem/Makefile)
- [`../../../03-Packet-Analysis-Top-Down/wireless-802.11/analysis/src/wireless-analysis.md`](../../../03-Packet-Analysis-Top-Down/wireless-802.11/analysis/src/wireless-analysis.md)
- [`../../../03-Packet-Analysis-Top-Down/wireless-802.11/docs/concepts/wireshark-wireless.md`](../../../03-Packet-Analysis-Top-Down/wireless-802.11/docs/concepts/wireshark-wireless.md)

## 읽는 순서
1. [`00-series-map.md`](00-series-map.md)
2. [`10-development-timeline.md`](10-development-timeline.md)
3. [`../../../03-Packet-Analysis-Top-Down/wireless-802.11/README.md`](../../../03-Packet-Analysis-Top-Down/wireless-802.11/README.md)

## 검증 진입점
- `make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem test`

## chronology 메모
- 이 프로젝트는 beacon/probe/auth/assoc/data를 단계별 절차로 읽는 편이 일반적인 개발자 관점에서도 가장 자연스럽다.
