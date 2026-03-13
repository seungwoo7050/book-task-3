# Evidence Ledger

- Phase 1: HTTP/2 쪽에서 stream 1/3 interleaving과 `WINDOW_UPDATE`를 먼저 고정한다.
- Phase 2: QUIC 쪽에서 `Initial`, `Handshake`, `1-RTT`, connection ID, packet number를 고정한다.
- Phase 3: 마지막에 HOL 차이를 구조 비교로 닫는다.
