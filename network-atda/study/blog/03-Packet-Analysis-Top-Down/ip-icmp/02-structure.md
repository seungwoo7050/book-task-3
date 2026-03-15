# IP and ICMP Packet Analysis 구조 메모

## 문서 구성 의도

- `00-series-map.md`: traceroute와 fragmentation이 각자 어떤 질문을 맡는지 먼저 분리한다.
- `10-development-timeline.md`: TTL-limited probes에서 fragmentation reassembly로 넘어가는 시야 확장을 chronology로 정리한다.
- `01-evidence-ledger.md`: `tshark` 필터와 answer markdown를 짧게 묶는다.

## 이번 재작성에서 강조한 점

- IPv4 header field를 나열하기보다 traceroute와 fragmentation이라는 concrete scenario에 고정한다.
- `Time Exceeded`, `Echo Reply`, fragment offsets를 각각 다른 역할로 분리한다.
- IPv6, PMTUD, OS별 traceroute variance는 현재 trace 바깥 범위로 남긴다.
