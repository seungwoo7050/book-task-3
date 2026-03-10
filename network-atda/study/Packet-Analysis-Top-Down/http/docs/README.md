# 개념 문서 안내

    이 디렉터리는 `HTTP Packet Analysis`를 공부하면서 반복해서 다시 볼 만한 개념 문서만 남겨 둔 곳입니다.

    ## 읽는 순서

    1. [`conditional-get.md`](concepts/conditional-get.md)
2. [`http-protocol.md`](concepts/http-protocol.md)
3. [`http-versions.md`](concepts/http-versions.md)
4. [`wireshark-http.md`](concepts/wireshark-http.md)
5. [`references/README.md`](references/README.md)

    ## 이 폴더가 답하려는 질문

    - HTTP 상태 코드 해석
- `If-Modified-Since`와 `304 Not Modified`
- 긴 응답이 여러 TCP segment로 나뉘는 모습
- embedded object 요청 체인

    ## 사용 원칙

    - 프로젝트 README와 중복되는 설명은 줄이고, 오래 남길 개념과 판단 근거를 우선합니다.
    - 답안 본문과 중복되는 설명은 줄이고, 반복 참조할 개념만 유지합니다.
    - 프로토콜 field 이름 같은 원문 용어는 필요할 때 그대로 유지합니다.
