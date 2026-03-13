# Development Timeline

첫 장면은 `http2-trace.tsv`다. frame **18**, **19**에서 stream **1**, **3**이 열린 뒤, frame **20**, **21**에서 `DATA`가 interleave 되는 장면이 HTTP/2 multiplexing의 핵심이다. frame **22**의 `WINDOW_UPDATE`는 connection-level flow control이 따로 있다는 사실까지 보여 준다.

다음 장면은 `quic-trace.tsv`다. frame **31-34**는 `Initial`과 `Handshake`, frame **35-39**는 `1-RTT`다. 여기서 눈여겨볼 것은 packet type뿐 아니라 `connection_id`, 그리고 client packet numbers `0, 1, 2, 3, 4`다. QUIC의 transport surface가 TCP와 다르게 밖으로 드러나는 부분이다.

마지막 비교는 결국 HOL 위치다. HTTP/2는 stream을 나눠도 TCP 위에 있기 때문에 transport-level head-of-line blocking을 그대로 가진다. QUIC은 multiplexing을 transport에 올리고 UDP 위에서 packet number와 connection ID를 직접 관리하므로, 그 결합이 같은 방식으로 남지 않는다.
