# 개념 문서 안내

    이 디렉터리는 `IP and ICMP Packet Analysis`를 공부하면서 반복해서 다시 볼 만한 개념 문서만 남겨 둔 곳입니다.

    ## 읽는 순서

    1. [`icmp-protocol.md`](concepts/icmp-protocol.md)
2. [`ipv4-header.md`](concepts/ipv4-header.md)
3. [`ipv4-vs-ipv6.md`](concepts/ipv4-vs-ipv6.md)
4. [`wireshark-ip.md`](concepts/wireshark-ip.md)
5. [`references/README.md`](references/README.md)

    ## 이 폴더가 답하려는 질문

    - IPv4 header field 해석
- fragmentation 3요소(ID/flags/offset)
- TTL과 traceroute 관계
- ICMP type/code 구분

    ## 사용 원칙

    - 프로젝트 README와 중복되는 설명은 줄이고, 오래 남길 개념과 판단 근거를 우선합니다.
    - 답안 본문과 중복되는 설명은 줄이고, 반복 참조할 개념만 유지합니다.
    - 프로토콜 field 이름 같은 원문 용어는 필요할 때 그대로 유지합니다.
