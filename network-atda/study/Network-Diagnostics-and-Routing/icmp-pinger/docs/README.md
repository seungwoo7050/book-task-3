# 개념 문서 안내

    이 디렉터리는 `ICMP Pinger`를 공부하면서 반복해서 다시 볼 만한 개념 문서만 남겨 둔 곳입니다.

    ## 읽는 순서

    1. [`checksum.md`](concepts/checksum.md)
2. [`icmp.md`](concepts/icmp.md)
3. [`ping-comparison.md`](concepts/ping-comparison.md)
4. [`raw-sockets.md`](concepts/raw-sockets.md)
5. [`reproducibility.md`](concepts/reproducibility.md)
6. [`references/README.md`](references/README.md)

    ## 이 폴더가 답하려는 질문

    - RFC 1071 인터넷 체크섬
- raw socket 권한 모델
- IP header length(`IHL`) 파싱
- binary packet build/parse 패턴

    ## 사용 원칙

    - 프로젝트 README와 중복되는 설명은 줄이고, 오래 남길 개념과 판단 근거를 우선합니다.
    - 이전 형식 노트는 `notion-archive/`에, 현재 읽을 작업 기록은 `notion/`에 둡니다.
    - 프로토콜 field 이름 같은 원문 용어는 필요할 때 그대로 유지합니다.
