    # Series Map — Web Proxy

    | 항목 | 내용 |
    | :--- | :--- |
    | 대상 프로젝트 | `01-Application-Protocols-and-Sockets/web-proxy` |
    | 문제 배경 | `Computer Networking: A Top-Down Approach`의 HTTP 프록시 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 |
    | 공개 답안 표면 | `python/src/web_proxy.py` |
    | 정식 검증 | `make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem test` |
    | rewrite 방식 | `isolate-and-rewrite` |
    | legacy 보관 위치 | `_legacy/2026-03-13-isolate-and-rewrite/01-Application-Protocols-and-Sockets/web-proxy` |

    ## 프로젝트 경계
    - 이 프로젝트는 absolute URL 파싱, origin fetch, 파일 캐시 hit/miss를 한 요청 흐름으로 묶는 HTTP proxy를 독립 문제로 다룬다.
    - `README.md`, `problem/`, `python/`, `docs/`가 한 폴더 아래에 닫혀 있어 다른 lab 없이도 범위 설명과 재검증이 가능하다.
    - canonical entrypoint는 `make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem test`이며, 이번 재실행에서도 Web Proxy Test Suite: 첫 fetch와 두 번째 cache check 모두 PASS, 총 3 passed 신호를 확인했다.

    ## 이번 rewrite의 입력 표면
    - `problem/code/proxy_skeleton.py`: 시작용 skeleton 코드
- `problem/script/test_proxy.sh`: 원 서버를 포함한 정식 검증 스크립트
- `python/tests/test_web_proxy.py`: URL 파싱과 캐시 키 생성을 확인하는 보조 테스트
    - 소스 파일: `python/src/web_proxy.py`
    - 테스트 파일: `python/tests/test_web_proxy.py`
    - `docs/concepts/caching.md` - 웹 캐싱 전략과 구현
- `docs/concepts/http-proxy.md` - HTTP Proxy Reference
- `docs/concepts/reproducibility.md` - 재현 가이드
- `docs/concepts/url-parsing.md` - URL Parsing for HTTP Proxies

    ## 이번 rewrite에서 제외한 입력
    - 기존 `study/blog/01-Application-Protocols-and-Sockets/web-proxy` 초안
    - `notion/`, `notion-archive/` 계열 노트
    - track 단위 회고나 다른 프로젝트 blog

    ## 이번 글에서 꼭 복원할 장면
    - Session 1: 실행 entrypoint와 최소 runtime surface를 먼저 고정했다
- Session 2: 핵심 protocol/algorithm branch를 채웠다
- Session 3: canonical test와 문서로 경계를 닫았다

    ## 이번 프로젝트가 남긴 학습 포인트
    - 절대 URL 파싱과 origin request 재구성
- 프록시의 server/client 이중 역할
- MD5 기반 캐시 키 설계
- `502`, `504` 같은 프록시 전용 오류 응답
