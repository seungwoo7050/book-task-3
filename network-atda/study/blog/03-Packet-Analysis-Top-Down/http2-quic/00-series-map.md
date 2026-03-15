# HTTP/2 and QUIC Packet Analysis 시리즈 맵

이 lab의 중심 질문은 "동시 요청 두 개를 처리할 때, multiplexing 책임이 어디에 놓이는가"다. HTTP/2 dataset은 `TCP:443` 위에서 stream `1`과 `3`이 interleave되는 모습을 보여 주고, QUIC dataset은 `UDP:443` 위에서 `Initial`, `Handshake`, `1-RTT`, explicit `connection_id`, monotonic `packet_number`를 드러낸다. 현재 답안은 이 둘의 차이를 "둘 다 병렬 요청을 처리한다" 수준으로 뭉개지 않고, HOL blocking이 transport에 남는지 아닌지까지 밀어 붙인다.

## 이 lab를 읽는 질문

- HTTP/2의 stream interleave는 어디까지 해결책이고, 어디서 TCP 제약을 그대로 끌고 가는가
- QUIC의 connection ID와 packet number는 왜 TCP sequence number와 다른 역할을 하는가
- 같은 `/feed`, `/avatars/42.png` 요청이 protocol 계층에 따라 어떻게 다른 표면을 남기는가

## 이번에 사용한 근거

- `problem/README.md`
- `analysis/src/http2-quic-analysis.md`
- `problem/Makefile`
- `problem/script/verify_answers.sh`
- 2026-03-14 재실행한 `make compare`

## 이번 재실행에서 고정한 사실

- HTTP/2 trace는 `TCP:443`, ALPN `h2`, stream `1/3`, `WINDOW_UPDATE` on stream `0`를 보여 준다.
- QUIC trace는 `UDP:443`, packet types `Initial`, `Handshake`, `1-RTT`, application streams `4` and `8`를 보여 준다.
- HTTP/2에서는 request/response data가 서로 interleave되지만 transport는 여전히 TCP다.
- QUIC에서는 connection ID와 packet number가 transport-level identity와 ordering marker를 따로 드러낸다.
