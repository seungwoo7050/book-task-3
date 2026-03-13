# Head-Of-Line Comparison

HTTP/2와 QUIC 모두 여러 stream을 동시에 처리하지만, 병목이 생기는 위치가 다르다.

- HTTP/2: multiplexing은 application framing에 있고, transport는 TCP다.
- QUIC: multiplexing이 transport에 있으므로 TCP-level HOL coupling을 그대로 물려받지 않는다.

이 차이가 이 프로젝트 전체의 중심 질문이다.
