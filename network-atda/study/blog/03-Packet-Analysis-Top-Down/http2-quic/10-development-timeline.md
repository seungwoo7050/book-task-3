# HTTP/2 and QUIC Packet Analysis 개발 타임라인

현재 답안을 다시 읽으면 이 lab의 흐름은 protocol feature 목록을 나열하는 식이 아니다. 오히려 "동시 요청"이라는 같은 문제를 HTTP/2와 QUIC가 서로 다른 층에서 어떻게 푸는지를, condensed trace 한 장씩으로 비교해 가는 구조다. 전환점은 세 번으로 압축된다.

## 1. 먼저 HTTP/2가 TCP 위에서 request serialization을 깨는 장면을 본다

HTTP/2 section의 출발점은 frame `18`, `19`다. `/feed`는 stream `1`, `/avatars/42.png`는 stream `3`에서 `HEADERS`로 열린다. 이어 frames `20`, `21`, `23`, `24`가 두 stream의 DATA를 서로 교차시킨다. 즉 application level에서는 더 이상 "요청 하나 끝나고 다음 요청" 순서를 강제하지 않는다.

하지만 여기서 transport가 바뀌는 것은 아니다. 모든 행의 `transport`는 `TCP:443`이고, `WINDOW_UPDATE`도 stream `0`의 connection-level control frame으로 남는다. 이 절반의 전환이 HTTP/2의 정확한 위치다.

## 2. 다음으로 QUIC는 multiplexing 자체를 UDP transport로 끌어내린다

QUIC section에 들어가면 표면이 바뀐다. `Initial -> Handshake -> 1-RTT` packet type 전이가 먼저 보이고, 그 위에 connection ID `8394c8f03e515708`, `1f4a7b9c00112233`가 반복해서 등장한다. 이후 application data는 stream `4`, `8`로 흐른다.

여기서 중요한 건 HTTP/2처럼 "TCP 위 multiple streams"가 아니라, transport 자체가 packet number와 connection identity를 관리한다는 점이다. 이 차이 때문에 answer markdown는 QUIC를 단순한 "더 빠른 HTTP/2"로 적지 않는다.

## 3. 마지막 결론은 HOL blocking의 위치를 비교하는 데서 닫힌다

현재 trace는 실제 loss event를 보여 주지 않지만, answer markdown는 아키텍처 차이를 끝까지 밀고 간다. HTTP/2는 app-layer serialization을 줄였어도 TCP-level HOL coupling은 남는다. QUIC는 UDP 위에서 stream을 transport 단에서 분리하므로 그 특정 TCP HOL coupling을 피한다.

즉 이 lab의 마지막 전환점은 "둘 다 병렬 처리"라는 표면적 공통점에서, "어느 층에서 병렬성을 구현했는가"라는 더 정확한 질문으로 넘어가는 데 있다. condensed dataset이 짧아도 이 결론만큼은 매우 선명하다.

## 지금 남는 한계

현재 자료는 full capture가 아니라 teaching dataset이다. 그래서 byte-level packet carving, retransmission episode, QPACK, 0-RTT 같은 세부는 다루지 않는다. 대신 stream ID, packet type, connection ID만으로도 protocol layering 차이를 읽을 수 있다는 점을 분명히 남긴다.
