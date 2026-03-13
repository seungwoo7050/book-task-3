# TCP and UDP Packet Analysis blog

이 디렉터리는 `TCP and UDP Packet Analysis`를 `strict source-only` 기준으로 다시 읽는 blog 시리즈다. chronology는 `problem/README.md`, `problem/Makefile`, `analysis/src/tcp-udp-analysis.md`를 중심으로 재구성했고, 필요한 맥락은 `docs/concepts/reproducibility.md`에서만 보강했다.

## source set
- [`../../../03-Packet-Analysis-Top-Down/tcp-udp/README.md`](../../../03-Packet-Analysis-Top-Down/tcp-udp/README.md)
- [`../../../03-Packet-Analysis-Top-Down/tcp-udp/problem/README.md`](../../../03-Packet-Analysis-Top-Down/tcp-udp/problem/README.md)
- [`../../../03-Packet-Analysis-Top-Down/tcp-udp/problem/Makefile`](../../../03-Packet-Analysis-Top-Down/tcp-udp/problem/Makefile)
- [`../../../03-Packet-Analysis-Top-Down/tcp-udp/analysis/src/tcp-udp-analysis.md`](../../../03-Packet-Analysis-Top-Down/tcp-udp/analysis/src/tcp-udp-analysis.md)
- [`../../../03-Packet-Analysis-Top-Down/tcp-udp/docs/concepts/reproducibility.md`](../../../03-Packet-Analysis-Top-Down/tcp-udp/docs/concepts/reproducibility.md)

## 읽는 순서
1. [`00-series-map.md`](00-series-map.md)
2. [`10-development-timeline.md`](10-development-timeline.md)
3. [`../../../03-Packet-Analysis-Top-Down/tcp-udp/README.md`](../../../03-Packet-Analysis-Top-Down/tcp-udp/README.md)

## 검증 진입점
- `make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem test`

## chronology 메모
- 같은 전송 계층이라도 TCP와 UDP를 서로 다른 질문 묶음으로 읽는 방식으로 chronology를 세웠다.
