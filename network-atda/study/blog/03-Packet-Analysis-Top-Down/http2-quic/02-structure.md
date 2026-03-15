# HTTP/2 and QUIC Packet Analysis 구조 메모

## 문서 구성 의도

- `00-series-map.md`: HTTP/2와 QUIC를 어떤 비교 질문으로 묶을지 먼저 고정한다.
- `10-development-timeline.md`: HTTP/1.1 단일 흐름에서 HTTP/2 stream interleave, 다시 QUIC transport multiplexing으로 넘어가는 관점을 chronology로 정리한다.
- `01-evidence-ledger.md`: condensed trace 출력과 answer markdown를 짧게 묶는다.

## 이번 재작성에서 강조한 점

- HTTP/2와 QUIC를 "둘 다 빠르다" 같은 성능 언어 대신 layering 차이로 설명한다.
- condensed dataset이라는 형식을 약점이 아니라 비교를 선명하게 만드는 선택으로 다룬다.
- loss recovery, QPACK, 0-RTT처럼 현재 trace가 안 다루는 영역은 분명히 선을 긋는다.
