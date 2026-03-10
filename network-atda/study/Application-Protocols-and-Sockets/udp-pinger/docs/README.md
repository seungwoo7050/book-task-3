# 개념 문서 안내

    이 디렉터리는 `UDP Pinger`를 공부하면서 반복해서 다시 볼 만한 개념 문서만 남겨 둔 곳입니다.

    ## 읽는 순서

    1. [`reproducibility.md`](concepts/reproducibility.md)
2. [`rtt.md`](concepts/rtt.md)
3. [`udp-sockets.md`](concepts/udp-sockets.md)
4. [`udp-vs-tcp.md`](concepts/udp-vs-tcp.md)
5. [`references/README.md`](references/README.md)

    ## 이 폴더가 답하려는 질문

    - UDP의 connectionless socket 사용법
- 1초 timeout을 손실 판정으로 바꾸는 방법
- RTT 최소값/평균값/최대값과 손실률 계산
- ICMP ping과 UDP echo 과제의 차이 이해

    ## 사용 원칙

    - 프로젝트 README와 중복되는 설명은 줄이고, 오래 남길 개념과 판단 근거를 우선합니다.
    - 이전 형식 노트는 `notion-archive/`에, 현재 읽을 작업 기록은 `notion/`에 둡니다.
    - 프로토콜 field 이름 같은 원문 용어는 필요할 때 그대로 유지합니다.
