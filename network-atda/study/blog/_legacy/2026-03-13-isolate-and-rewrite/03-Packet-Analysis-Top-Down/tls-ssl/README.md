# TLS Packet Analysis blog

이 디렉터리는 `TLS Packet Analysis`를 `strict source-only` 기준으로 다시 읽는 blog 시리즈다. chronology는 `problem/README.md`, `problem/Makefile`, `analysis/src/tls-ssl-analysis.md`, `docs/concepts/wireshark-tls.md`를 기반으로 합리적으로 재구성했다.

## source set
- [`../../../03-Packet-Analysis-Top-Down/tls-ssl/README.md`](../../../03-Packet-Analysis-Top-Down/tls-ssl/README.md)
- [`../../../03-Packet-Analysis-Top-Down/tls-ssl/problem/README.md`](../../../03-Packet-Analysis-Top-Down/tls-ssl/problem/README.md)
- [`../../../03-Packet-Analysis-Top-Down/tls-ssl/problem/Makefile`](../../../03-Packet-Analysis-Top-Down/tls-ssl/problem/Makefile)
- [`../../../03-Packet-Analysis-Top-Down/tls-ssl/analysis/src/tls-ssl-analysis.md`](../../../03-Packet-Analysis-Top-Down/tls-ssl/analysis/src/tls-ssl-analysis.md)
- [`../../../03-Packet-Analysis-Top-Down/tls-ssl/docs/concepts/wireshark-tls.md`](../../../03-Packet-Analysis-Top-Down/tls-ssl/docs/concepts/wireshark-tls.md)

## 읽는 순서
1. [`00-series-map.md`](00-series-map.md)
2. [`10-development-timeline.md`](10-development-timeline.md)
3. [`../../../03-Packet-Analysis-Top-Down/tls-ssl/README.md`](../../../03-Packet-Analysis-Top-Down/tls-ssl/README.md)

## 검증 진입점
- `make -C study/03-Packet-Analysis-Top-Down/tls-ssl/problem test`

## chronology 메모
- minimal synthetic trace라는 한계를 인정하는 흐름이 중요해서, "보이는 것"과 "malformed라서 보이지 않는 것"을 분리해 적었다.
