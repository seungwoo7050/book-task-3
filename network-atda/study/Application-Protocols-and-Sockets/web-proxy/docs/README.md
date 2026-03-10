# 개념 문서 안내

    이 디렉터리는 `Web Proxy`를 공부하면서 반복해서 다시 볼 만한 개념 문서만 남겨 둔 곳입니다.

    ## 읽는 순서

    1. [`caching.md`](concepts/caching.md)
2. [`http-proxy.md`](concepts/http-proxy.md)
3. [`reproducibility.md`](concepts/reproducibility.md)
4. [`url-parsing.md`](concepts/url-parsing.md)
5. [`references/README.md`](references/README.md)

    ## 이 폴더가 답하려는 질문

    - 절대 URL 파싱과 origin request 재구성
- 프록시의 server/client 이중 역할
- MD5 기반 캐시 키 설계
- `502`, `504` 같은 프록시 전용 오류 응답

    ## 사용 원칙

    - 프로젝트 README와 중복되는 설명은 줄이고, 오래 남길 개념과 판단 근거를 우선합니다.
    - 이전 형식 노트는 `notion-archive/`에, 현재 읽을 작업 기록은 `notion/`에 둡니다.
    - 프로토콜 field 이름 같은 원문 용어는 필요할 때 그대로 유지합니다.
