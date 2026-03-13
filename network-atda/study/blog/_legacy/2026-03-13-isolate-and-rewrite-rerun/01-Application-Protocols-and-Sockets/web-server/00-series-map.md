    # Series Map — Web Server

    | 항목 | 내용 |
    | :--- | :--- |
    | 대상 프로젝트 | `01-Application-Protocols-and-Sockets/web-server` |
    | 문제 배경 | `Computer Networking: A Top-Down Approach`의 웹 서버 구현 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 |
    | 공개 답안 표면 | `python/src/web_server.py` |
    | 정식 검증 | `make -C study/01-Application-Protocols-and-Sockets/web-server/problem test` |
    | rewrite 방식 | `isolate-and-rewrite` |
    | legacy 보관 위치 | `_legacy/2026-03-13-isolate-and-rewrite/01-Application-Protocols-and-Sockets/web-server` |

    ## 프로젝트 경계
    - 이 프로젝트는 HTTP request line을 filename으로 바꾸고 200/404 응답을 직접 만드는 가장 작은 정적 서버를 독립 문제로 다룬다.
    - `README.md`, `problem/`, `python/`, `docs/`가 한 폴더 아래에 닫혀 있어 다른 lab 없이도 범위 설명과 재검증이 가능하다.
    - canonical entrypoint는 `make -C study/01-Application-Protocols-and-Sockets/web-server/problem test`이며, 이번 재실행에서도 Web Server Test Suite: `GET /hello.html` 200, `GET /nonexistent` 404, 총 3 passed 신호를 확인했다.

    ## 이번 rewrite의 입력 표면
    - `problem/code/server_skeleton.py`: 시작용 skeleton 코드
- `problem/data/hello.html`: 정적 파일 서빙 확인용 샘플 HTML
- `problem/script/test_server.sh`: 정식 검증을 호출하는 스크립트
    - 소스 파일: `python/src/web_server.py`
    - 테스트 파일: `python/tests/test_web_server.py`
    - `docs/concepts/content-types.md` - MIME Types와 Content-Type 헤더
- `docs/concepts/error-handling.md` - 에러 처리 및 보안 고려사항
- `docs/concepts/http.md` - HTTP/1.1 Protocol Reference
- `docs/concepts/reproducibility.md` - 재현 가이드

    ## 이번 rewrite에서 제외한 입력
    - 기존 `study/blog/01-Application-Protocols-and-Sockets/web-server` 초안
    - `notion/`, `notion-archive/` 계열 노트
    - track 단위 회고나 다른 프로젝트 blog

    ## 이번 글에서 꼭 복원할 장면
    - Session 1: 실행 entrypoint와 최소 runtime surface를 먼저 고정했다
- Session 2: 핵심 protocol/algorithm branch를 채웠다
- Session 3: canonical test와 문서로 경계를 닫았다

    ## 이번 프로젝트가 남긴 학습 포인트
    - HTTP 요청 라인의 최소 파싱 규칙
- 정적 파일 서빙과 `Content-Type` 결정
- 404 응답 생성과 연결 종료 시점
- 요청마다 스레드를 분리하는 기본 accept loop 구조
