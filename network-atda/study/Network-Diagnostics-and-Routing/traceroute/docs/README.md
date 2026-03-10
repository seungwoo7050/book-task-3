# 개념 문서 안내

    이 디렉터리는 `Traceroute`를 공부하면서 반복해서 다시 볼 만한 개념 문서만 남겨 둔 곳입니다.

    ## 읽는 순서

    1. [`icmp-protocol.md`](concepts/icmp-protocol.md)
2. [`ipv4-header.md`](concepts/ipv4-header.md)
3. [`raw-sockets.md`](concepts/raw-sockets.md)
4. [`references/README.md`](references/README.md)

    ## 이 폴더가 답하려는 질문

    - TTL과 `ICMP Time Exceeded`의 연결
- embedded UDP port를 이용한 probe 매칭
- live probing과 synthetic integration test 분리
- 목적지 도달을 `Port Unreachable`로 판정하는 규칙

    ## 사용 원칙

    - 프로젝트 README와 중복되는 설명은 줄이고, 오래 남길 개념과 판단 근거를 우선합니다.
    - 이전 형식 노트는 `notion-archive/`에, 현재 읽을 작업 기록은 `notion/`에 둡니다.
    - 프로토콜 field 이름 같은 원문 용어는 필요할 때 그대로 유지합니다.
