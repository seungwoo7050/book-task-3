# 개념 문서 안내

    이 디렉터리는 `TCP and UDP Packet Analysis`를 공부하면서 반복해서 다시 볼 만한 개념 문서만 남겨 둔 곳입니다.

    ## 읽는 순서

    1. [`reproducibility.md`](concepts/reproducibility.md)
2. [`tcp-flow-congestion.md`](concepts/tcp-flow-congestion.md)
3. [`tcp-protocol.md`](concepts/tcp-protocol.md)
4. [`tcp-retransmission.md`](concepts/tcp-retransmission.md)
5. [`udp-protocol.md`](concepts/udp-protocol.md)
6. [`wireshark-transport.md`](concepts/wireshark-transport.md)
7. [`references/README.md`](references/README.md)

    ## 이 폴더가 답하려는 질문

    - 3-way handshake 해석
- relative seq/ack 읽기
- window field와 retransmission 표시
- UDP의 8-byte header와 무상태성

    ## 사용 원칙

    - 프로젝트 README와 중복되는 설명은 줄이고, 오래 남길 개념과 판단 근거를 우선합니다.
    - 답안 본문과 중복되는 설명은 줄이고, 반복 참조할 개념만 유지합니다.
    - 프로토콜 field 이름 같은 원문 용어는 필요할 때 그대로 유지합니다.
