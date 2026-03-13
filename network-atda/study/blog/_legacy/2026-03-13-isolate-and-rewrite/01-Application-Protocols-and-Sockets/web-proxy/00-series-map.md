# Web Proxy 시리즈 지도

## 이 프로젝트를 한 줄로

한 프로그램 안에서 클라이언트와 서버 역할을 동시에 하는 중개자를 만드는 과제다. Web Server에서 "요청을 받아 응답한다"만 했다면, 이번에는 "요청을 받아 → 다른 서버에 대신 요청하고 → 받은 응답을 다시 원래 클라이언트에 넘기는" 전체 흐름을 구현한다. 캐시까지 붙이면 proxy의 가치가 분명해진다.

## 문제 구조
- 제공물: `problem/code/proxy_skeleton.py`, `problem/script/test_proxy.sh`
- 답안: `python/src/web_proxy.py`, `python/tests/test_web_proxy.py`
- 검증: `make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem test`

## 이 시리즈에서 따라갈 질문
1. proxy가 받는 요청 라인은 왜 absolute URL인가
2. URL을 `hostname:port/path`로 분해하지 않으면 무엇이 깨지는가
3. cache hit를 origin fetch보다 먼저 검사해야 하는 이유는 무엇인가
4. proxy 고유 오류 코드 `502`와 `504`는 언제 쓰이는가

## 글 목록
| 번호 | 파일 | 범위 |
| :--- | :--- | :--- |
| `10` | [`10-development-timeline.md`](10-development-timeline.md) | URL 파싱부터 cache hit 검증까지 |
