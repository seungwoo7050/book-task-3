# 개념 문서 안내

    이 디렉터리는 `TLS Packet Analysis`를 공부하면서 반복해서 다시 볼 만한 개념 문서만 남겨 둔 곳입니다.

    ## 읽는 순서

    1. [`tls-handshake-detail.md`](concepts/tls-handshake-detail.md)
2. [`tls-protocol.md`](concepts/tls-protocol.md)
3. [`tls-versions-comparison.md`](concepts/tls-versions-comparison.md)
4. [`wireshark-tls.md`](concepts/wireshark-tls.md)
5. [`references/README.md`](references/README.md)

    ## 이 폴더가 답하려는 질문

    - ClientHello/ServerHello 순서 해석
- cipher suite 의미
- certificate visibility 한계
- TLS 1.2 vs 1.3 RTT 차이

    ## 사용 원칙

    - 프로젝트 README와 중복되는 설명은 줄이고, 오래 남길 개념과 판단 근거를 우선합니다.
    - 답안 본문과 중복되는 설명은 줄이고, 반복 참조할 개념만 유지합니다.
    - 프로토콜 field 이름 같은 원문 용어는 필요할 때 그대로 유지합니다.
