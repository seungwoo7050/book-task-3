# Frame Boundary Recovery

TCP는 message 단위가 아니라 byte stream이다. 따라서 sender가 한 번 `Write` 했다고 receiver가 한 번 `Read`로 같은 단위를 받는다는 보장이 없다.

이 프로젝트는 `[4-byte payload length][JSON payload]` 형식을 사용한다. decoder는 내부 buffer에 chunk를 누적하고, header 4바이트를 읽을 수 있을 때만 payload 길이를 계산한다. 전체 frame 길이가 확보되면 그제서야 한 메시지를 꺼낸다.
