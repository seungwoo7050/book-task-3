# QUIC Connection ID And Packet Number

QUIC trace를 읽을 때 가장 눈에 띄는 표면은 `packet type`, `packet number`, `connection ID`다.

- `Initial`, `Handshake`, `1-RTT`는 handshake 진행 상태를 드러낸다.
- connection ID는 4-tuple이 바뀌어도 connection identity를 유지하게 해 준다.
- packet number는 byte offset이 아니라 transport packet 자체를 식별한다.
