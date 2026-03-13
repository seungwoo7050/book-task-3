# DNS Packet Analysis blog

이 디렉터리는 `DNS Packet Analysis`를 `strict source-only` 기준으로 다시 읽는 blog 시리즈다. chronology는 `problem/README.md`, `problem/Makefile`, `analysis/src/dns-analysis.md`, `docs/concepts/wireshark-dns.md`를 바탕으로 일반적인 개발자 수준의 추론으로 재구성했다.

## source set
- [`../../../03-Packet-Analysis-Top-Down/dns/README.md`](../../../03-Packet-Analysis-Top-Down/dns/README.md)
- [`../../../03-Packet-Analysis-Top-Down/dns/problem/README.md`](../../../03-Packet-Analysis-Top-Down/dns/problem/README.md)
- [`../../../03-Packet-Analysis-Top-Down/dns/problem/Makefile`](../../../03-Packet-Analysis-Top-Down/dns/problem/Makefile)
- [`../../../03-Packet-Analysis-Top-Down/dns/analysis/src/dns-analysis.md`](../../../03-Packet-Analysis-Top-Down/dns/analysis/src/dns-analysis.md)
- [`../../../03-Packet-Analysis-Top-Down/dns/docs/concepts/wireshark-dns.md`](../../../03-Packet-Analysis-Top-Down/dns/docs/concepts/wireshark-dns.md)

## 읽는 순서
1. [`00-series-map.md`](00-series-map.md)
2. [`10-development-timeline.md`](10-development-timeline.md)
3. [`../../../03-Packet-Analysis-Top-Down/dns/README.md`](../../../03-Packet-Analysis-Top-Down/dns/README.md)

## 검증 진입점
- `make -C study/03-Packet-Analysis-Top-Down/dns/problem test`

## chronology 메모
- 이 프로젝트는 `관찰 가능한 것`과 `trace가 짧아서 관찰 불가한 것`을 구분하는 흐름 자체가 핵심이다.
