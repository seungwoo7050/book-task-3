    # Structure Design — Web Proxy

    ## opening
    - 시작 질문: 이 프로젝트를 실제로 어디서부터 만들기 시작했는가.
    - 바로 보여 줄 증거: `make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem test`와 ``python/src/web_proxy.py::main``.
    - 서술 원칙: 결과 요약보다 Session별 판단 이동을 우선한다.
    - 메모: `make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem test`가 통과하는 상태를 출발점으로 삼되, 실제 글의 첫 장면은 ``python/src/web_proxy.py::main``에서 시작한다.

    ## Session 1 — 실행 entrypoint와 최소 runtime surface를 먼저 고정했다
- 다룰 파일/표면: `python/src/web_proxy.py::main`
- 글에서 먼저 던질 질문: "README보다 먼저 실제 entrypoint가 어떤 입력과 출력 surface를 갖는지 잡아야 한다"
- 꼭 넣을 CLI: `make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem run-solution`
- 꼭 남길 검증 신호: run surface가 정리되면서 이후 판단을 함수 단위로 이어 붙일 수 있게 됐다.
- 핵심 전환 문장: 절대 URL 파싱과 origin request 재구성
## Session 2 — 핵심 protocol/algorithm branch를 채웠다
- 다룰 파일/표면: `python/src/web_proxy.py::handle_client`
- 글에서 먼저 던질 질문: "이 프로젝트의 핵심은 설명문이 아니라 request/reply, timer, cache, parser 같은 작은 branch에 숨어 있다"
- 꼭 넣을 CLI: `make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem run-solution`
- 꼭 남길 검증 신호: 핵심 로직이 눈에 보이는 함수 단위로 정리되면서 test가 기대하는 입출력과 연결됐다.
- 핵심 전환 문장: 프록시의 server/client 이중 역할
## Session 3 — canonical test와 문서로 경계를 닫았다
- 다룰 파일/표면: `python/tests/test_web_proxy.py`, `make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem test`, `docs/concepts/caching.md`
- 글에서 먼저 던질 질문: "좋은 chronology는 마지막에 test result와 남은 한계를 같이 남겨야 과장되지 않는다"
- 꼭 넣을 CLI: `make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem test`
- 꼭 남길 검증 신호: Web Proxy Test Suite: 첫 fetch와 두 번째 cache check 모두 PASS, 총 3 passed
- 핵심 전환 문장: 절대 URL 파싱과 origin request 재구성 and 프록시의 server/client 이중 역할

    ## ending
    - 마지막 단락에서는 현재 한계를 README bullet 그대로 축약해 남긴다.
    - `Cache-Control`이나 TTL 기반 만료 정책은 없습니다.
- `HTTPS CONNECT`는 지원하지 않습니다.
- 캐시 디렉터리 동시성 제어는 단순한 수준에 머뭅니다.
