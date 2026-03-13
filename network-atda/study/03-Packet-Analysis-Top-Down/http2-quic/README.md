# HTTP/2 and QUIC Packet Analysis

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | HTTP/2와 QUIC trace를 나란히 읽으며, multiplexing과 head-of-line tradeoff가 어디서 갈라지는지 비교하는 packet analysis lab |
| 정식 검증 | `make -C study/03-Packet-Analysis-Top-Down/http2-quic/problem test` |

## 문제가 뭐였나

- HTTP/2는 TCP 위에서 어떻게 stream을 multiplexing 하는가
- QUIC은 UDP 위에서 handshake, packet number, connection ID를 어떻게 드러내는가
- 둘의 차이가 "같은 여러 요청을 동시에 보낸다" 수준을 넘어 어디서 구조적으로 갈라지는가

## 제공된 자료

- `problem/data/http2-trace.tsv`: HTTP/2 condensed trace
- `problem/data/quic-trace.tsv`: QUIC condensed trace
- `analysis/src/http2-quic-analysis.md`: 공개 답안
- `docs/concepts/`: framing / connection ID / HOL 비교 메모

## 이 레포의 답

- 한 줄 답: HTTP/2는 TCP 위에서 stream을 interleave하지만 transport HOL은 남기고, QUIC은 UDP 위에서 connection ID와 packet number를 드러내며 transport-level multiplexing으로 그 제약을 줄인다.
- 공개 답안 위치: `analysis/src/`
- 보조 공개 표면: `docs/`
- 보조 공개 표면: `study/blog/03-Packet-Analysis-Top-Down/http2-quic/`

## 어떻게 검증하나

- 검증: `make -C study/03-Packet-Analysis-Top-Down/http2-quic/problem test`
- 공개 답안 위치: `analysis/src/`
- 개념 노트 위치: `docs/concepts/`

## 현재 한계

- raw pcap 전체를 싣기보다 trace-derived condensed dataset을 사용한다.
- loss recovery, QPACK, 0-RTT는 필수 범위에 넣지 않았다.
