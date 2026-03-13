# HTTP/2 Framing And Multiplexing

HTTP/2는 하나의 TCP connection 위에서 여러 stream을 동시에 흘린다. 중요한 것은 "여러 요청을 동시에 보낼 수 있다"보다, **frame이 stream 단위로 interleave**된다는 점이다.

- `HEADERS`와 `DATA` frame이 stream 1, 3 사이에서 번갈아 나타날 수 있다.
- flow control은 stream 단위와 connection 단위 둘 다 있다.
- 하지만 transport는 여전히 TCP이므로 loss는 connection 전체의 진행에 영향을 줄 수 있다.
