    # Structure Design — Web Server

    ## opening
    - 시작 질문: 이 프로젝트를 실제로 어디서부터 만들기 시작했는가.
    - 바로 보여 줄 증거: `make -C study/01-Application-Protocols-and-Sockets/web-server/problem test`와 ``python/src/web_server.py::main``.
    - 서술 원칙: 결과 요약보다 Session별 판단 이동을 우선한다.
    - 메모: `make -C study/01-Application-Protocols-and-Sockets/web-server/problem test`가 통과하는 상태를 출발점으로 삼되, 실제 글의 첫 장면은 ``python/src/web_server.py::main``에서 시작한다.

    ## Session 1 — 실행 entrypoint와 최소 runtime surface를 먼저 고정했다
- 다룰 파일/표면: `python/src/web_server.py::main`
- 글에서 먼저 던질 질문: "README보다 먼저 실제 entrypoint가 어떤 입력과 출력 surface를 갖는지 잡아야 한다"
- 꼭 넣을 CLI: `make -C study/01-Application-Protocols-and-Sockets/web-server/problem run-solution`
- 꼭 남길 검증 신호: run surface가 정리되면서 이후 판단을 함수 단위로 이어 붙일 수 있게 됐다.
- 핵심 전환 문장: HTTP 요청 라인의 최소 파싱 규칙
## Session 2 — 핵심 protocol/algorithm branch를 채웠다
- 다룰 파일/표면: `python/src/web_server.py::handle_client`
- 글에서 먼저 던질 질문: "이 프로젝트의 핵심은 설명문이 아니라 request/reply, timer, cache, parser 같은 작은 branch에 숨어 있다"
- 꼭 넣을 CLI: `make -C study/01-Application-Protocols-and-Sockets/web-server/problem run-solution`
- 꼭 남길 검증 신호: 핵심 로직이 눈에 보이는 함수 단위로 정리되면서 test가 기대하는 입출력과 연결됐다.
- 핵심 전환 문장: 정적 파일 서빙과 `Content-Type` 결정
## Session 3 — canonical test와 문서로 경계를 닫았다
- 다룰 파일/표면: `python/tests/test_web_server.py`, `make -C study/01-Application-Protocols-and-Sockets/web-server/problem test`, `docs/concepts/content-types.md`
- 글에서 먼저 던질 질문: "좋은 chronology는 마지막에 test result와 남은 한계를 같이 남겨야 과장되지 않는다"
- 꼭 넣을 CLI: `make -C study/01-Application-Protocols-and-Sockets/web-server/problem test`
- 꼭 남길 검증 신호: Web Server Test Suite: `GET /hello.html` 200, `GET /nonexistent` 404, 총 3 passed
- 핵심 전환 문장: HTTP 요청 라인의 최소 파싱 규칙과 정적 파일 서빙 및 `Content-Type` 결정

    ## ending
    - 마지막 단락에서는 현재 한계를 README bullet 그대로 축약해 남긴다.
    - path traversal 방어는 아직 구현하지 않았습니다.
- 스레드 수 제한이나 thread pool은 없습니다.
- GET 외 메서드는 지원하지 않습니다.
