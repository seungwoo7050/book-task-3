# HTTP Packet Analysis blog

이 디렉터리는 `HTTP Packet Analysis`를 `strict source-only` 기준으로 다시 읽는 blog 시리즈다. chronology는 `problem/README.md`, `problem/Makefile`, `analysis/src/http-analysis.md`, `docs/concepts/wireshark-http.md`를 바탕으로, 일반적인 개발자라면 밟았을 분석 순서를 추론해 정리했다.

## source set
- [`../../../03-Packet-Analysis-Top-Down/http/README.md`](../../../03-Packet-Analysis-Top-Down/http/README.md)
- [`../../../03-Packet-Analysis-Top-Down/http/problem/README.md`](../../../03-Packet-Analysis-Top-Down/http/problem/README.md)
- [`../../../03-Packet-Analysis-Top-Down/http/problem/Makefile`](../../../03-Packet-Analysis-Top-Down/http/problem/Makefile)
- [`../../../03-Packet-Analysis-Top-Down/http/analysis/README.md`](../../../03-Packet-Analysis-Top-Down/http/analysis/README.md)
- [`../../../03-Packet-Analysis-Top-Down/http/analysis/src/http-analysis.md`](../../../03-Packet-Analysis-Top-Down/http/analysis/src/http-analysis.md)
- [`../../../03-Packet-Analysis-Top-Down/http/docs/concepts/wireshark-http.md`](../../../03-Packet-Analysis-Top-Down/http/docs/concepts/wireshark-http.md)

## 읽는 순서
1. [`00-series-map.md`](00-series-map.md)
2. [`10-development-timeline.md`](10-development-timeline.md)
3. [`../../../03-Packet-Analysis-Top-Down/http/README.md`](../../../03-Packet-Analysis-Top-Down/http/README.md)

## 검증 진입점
- `make -C study/03-Packet-Analysis-Top-Down/http/problem test`

## chronology 메모
- trace 분석 순서는 `Makefile`의 `filter-*` 타깃과 공개 답안의 frame evidence를 기준으로 합리적으로 복원했다.
