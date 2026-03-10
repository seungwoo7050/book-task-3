# 개념 문서 안내

    이 디렉터리는 `DNS Packet Analysis`를 공부하면서 반복해서 다시 볼 만한 개념 문서만 남겨 둔 곳입니다.

    ## 읽는 순서

    1. [`dns-hierarchy.md`](concepts/dns-hierarchy.md)
2. [`dns-protocol.md`](concepts/dns-protocol.md)
3. [`dns-security.md`](concepts/dns-security.md)
4. [`wireshark-dns.md`](concepts/wireshark-dns.md)
5. [`references/README.md`](references/README.md)

    ## 이 폴더가 답하려는 질문

    - DNS header/question/answer 구조
- record type별 역할
- recursive resolution 개념
- TTL 감소와 cache hit 해석

    ## 사용 원칙

    - 프로젝트 README와 중복되는 설명은 줄이고, 오래 남길 개념과 판단 근거를 우선합니다.
    - 답안 본문과 중복되는 설명은 줄이고, 반복 참조할 개념만 유지합니다.
    - 프로토콜 field 이름 같은 원문 용어는 필요할 때 그대로 유지합니다.
