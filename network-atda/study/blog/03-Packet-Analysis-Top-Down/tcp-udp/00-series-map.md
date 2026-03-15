# TCP and UDP Packet Analysis 시리즈 맵

이 lab의 중심 질문은 "TCP와 UDP는 무엇이 다른가"를 교과서식으로 답하는 것이 아니라, "짧은 trace에서 어느 차이가 실제로 보이는가"다. 현재 답안은 TCP upload trace에서 handshake, seq/ack, window, throughput, RTT를 읽고, UDP DNS trace에서 4-field header와 `length = header + payload`라는 최소 계약을 읽는다.

## 이 lab를 읽는 질문

- TCP handshake와 ACK chain은 connection state를 어떻게 눈에 보이게 만드는가
- relative sequence number가 있으면 data volume과 RTT를 어떻게 역산할 수 있는가
- UDP는 왜 "적은 정보"가 아니라 "의도적으로 적은 상태"로 읽혀야 하는가

## 이번에 사용한 근거

- `problem/README.md`
- `analysis/src/tcp-udp-analysis.md`
- `problem/Makefile`
- `problem/script/verify_answers.sh`
- 2026-03-14 재실행한 `filter-handshake`, `filter-data`, `filter-udp`

## 이번 재실행에서 고정한 사실

- TCP handshake는 frames `1/2/3`에서 상대 sequence/ack 증가 규칙을 명확히 보여 준다.
- client data-bearing segments는 initial `72 bytes` 뒤 `200-byte` chunk가 연속된다.
- retransmission filter는 empty여서 current trace는 clean upload path다.
- UDP trace는 query length `36`, response length `62`만으로도 header 8 bytes와 payload 관계를 확인하게 해 준다.
