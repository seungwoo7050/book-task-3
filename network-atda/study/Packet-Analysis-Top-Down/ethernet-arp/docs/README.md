# 개념 문서 안내

    이 디렉터리는 `Ethernet and ARP Packet Analysis`를 공부하면서 반복해서 다시 볼 만한 개념 문서만 남겨 둔 곳입니다.

    ## 읽는 순서

    1. [`arp-protocol.md`](concepts/arp-protocol.md)
2. [`arp-security-switching.md`](concepts/arp-security-switching.md)
3. [`ethernet-frame.md`](concepts/ethernet-frame.md)
4. [`wireshark-link.md`](concepts/wireshark-link.md)
5. [`references/README.md`](references/README.md)

    ## 이 폴더가 답하려는 질문

    - EtherType와 상위 프로토콜 연결
- ARP request broadcast / reply unicast
- 게이트웨이 MAC 해석
- ARP 보안 취약점 개념

    ## 사용 원칙

    - 프로젝트 README와 중복되는 설명은 줄이고, 오래 남길 개념과 판단 근거를 우선합니다.
    - 답안 본문과 중복되는 설명은 줄이고, 반복 참조할 개념만 유지합니다.
    - 프로토콜 field 이름 같은 원문 용어는 필요할 때 그대로 유지합니다.
