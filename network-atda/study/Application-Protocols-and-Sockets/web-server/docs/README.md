# 개념 문서 안내

    이 디렉터리는 `Web Server`를 공부하면서 반복해서 다시 볼 만한 개념 문서만 남겨 둔 곳입니다.

    ## 읽는 순서

    1. [`content-types.md`](concepts/content-types.md)
2. [`error-handling.md`](concepts/error-handling.md)
3. [`http.md`](concepts/http.md)
4. [`reproducibility.md`](concepts/reproducibility.md)
5. [`tcp-sockets.md`](concepts/tcp-sockets.md)
6. [`threading.md`](concepts/threading.md)
7. [`references/README.md`](references/README.md)

    ## 이 폴더가 답하려는 질문

    - HTTP 요청 라인의 최소 파싱 규칙
- 정적 파일 서빙과 `Content-Type` 결정
- 404 응답 생성과 연결 종료 시점
- 요청마다 스레드를 분리하는 기본 accept loop 구조

    ## 사용 원칙

    - 프로젝트 README와 중복되는 설명은 줄이고, 오래 남길 개념과 판단 근거를 우선합니다.
    - 이전 형식 노트는 `notion-archive/`에, 현재 읽을 작업 기록은 `notion/`에 둡니다.
    - 프로토콜 field 이름 같은 원문 용어는 필요할 때 그대로 유지합니다.
