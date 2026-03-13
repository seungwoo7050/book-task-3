# Condensed Trace Data

이 프로젝트는 raw pcap 전체 대신 trace에서 뽑아 낸 condensed dataset을 제공한다. 목적은 도구 조작보다 비교 포인트를 선명하게 만드는 것이다.

- `http2-trace.tsv`: frame, transport, ALPN, stream id, frame type, note
- `quic-trace.tsv`: frame, transport, endpoint, packet type, packet number, stream id, connection id, note
