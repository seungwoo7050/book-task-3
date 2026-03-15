# HTTP/2 and QUIC Packet Analysis Blog

이 문서 묶음은 `http2-quic` 랩을 "새 프로토콜 두 개 소개"가 아니라 "multiplexing이 application framing에 머무는지, transport까지 내려가는지"라는 비교 질문으로 다시 읽는다. 현재 공개 답안은 raw pcap 전체 대신 `http2-trace.tsv`, `quic-trace.tsv` condensed dataset을 사용해 stream ID, packet type, connection ID, packet number를 비교한다. 따라서 이 lab의 핵심은 protocol encyclopaedia가 아니라, HTTP/2와 QUIC가 같은 동시 요청 문제를 서로 다른 층에서 푼다는 점을 짧은 표로 선명하게 보여 주는 데 있다.

이번 재작성은 기존 blog 본문이 아니라 다음 근거만 사용했다.

- 문제 정의: `study/03-Packet-Analysis-Top-Down/http2-quic/problem/README.md`
- 답안 경계: `README.md`, `analysis/README.md`, `analysis/src/http2-quic-analysis.md`
- 실제 검증: 2026-03-14 재실행한 `make -C network-atda/study/03-Packet-Analysis-Top-Down/http2-quic/problem test`
- 보조 출력: `make -C .../http2-quic/problem compare`

## 읽는 순서

1. [`00-series-map.md`](./00-series-map.md)
2. [`10-development-timeline.md`](./10-development-timeline.md)
3. [`01-evidence-ledger.md`](./01-evidence-ledger.md)
4. [`02-structure.md`](./02-structure.md)

## 이번에 다시 확인한 검증 상태

- 정식 검증 명령: `make -C network-atda/study/03-Packet-Analysis-Top-Down/http2-quic/problem test`
- 결과: `PASS: http2-quic answer file passed content verification`
- 보조 비교 출력에서 재확인한 값:
  - HTTP/2: stream `1` `/feed`, stream `3` `/avatars/42.png`
  - QUIC: packet types `Initial -> Handshake -> 1-RTT`, connection IDs `8394c8f03e515708` / `1f4a7b9c00112233`

## 지금 남기는 한계

- raw full capture가 아니라 condensed TSV라 packet-by-packet byte layout까지는 다루지 않는다.
- QUIC loss recovery, QPACK, 0-RTT는 현재 범위에 넣지 않았다.
- HTTP/2 쪽도 TCP loss가 실제로 일어나는 장면을 보여 주는 trace는 아니다.
