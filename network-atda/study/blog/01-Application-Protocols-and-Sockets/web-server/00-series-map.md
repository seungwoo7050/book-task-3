# Web Server 시리즈 지도

## 이 프로젝트를 한 줄로

TCP socket과 `threading`만으로 HTTP/1.1 정적 파일 서버를 밑바닥부터 만드는 과제다. skeleton을 열었을 때 "소켓이면 바로 send 하면 되지 않나?"라는 생각이, 끝날 때 "요청 라인 파싱 → 파일 읽기 → Content-Length → 연결 종료라는 계약이 먼저였다"로 바뀌는 과정을 기록한다.

## 문제 구조
- 제공물: `problem/code/server_skeleton.py`, `problem/data/hello.html`, `problem/script/test_server.sh`
- 답안: `python/src/web_server.py`, `python/tests/test_web_server.py`
- 검증: `make -C study/01-Application-Protocols-and-Sockets/web-server/problem test`
- 단건 확인: `make ... request` → `curl -v http://localhost:6789/hello.html`

## 이 시리즈에서 따라갈 질문
1. socket `bind → listen → accept` 루프와 HTTP 요청 라인의 관계는 무엇인가
2. `/` 요청과 `/hello.html` 요청을 왜 같은 파일로 매핑해야 하는가
3. `404`가 단순 오류가 아니라 응답 계약의 절반인 이유는 무엇인가
4. `Content-Length`와 `Connection: close`가 없으면 브라우저가 왜 멈추는가
5. `curl` 한 번으로 "된다"고 말할 수 없는 이유는 무엇인가

## 글 목록
| 번호 | 파일 | 범위 |
| :--- | :--- | :--- |
| `10` | [`10-development-timeline.md`](10-development-timeline.md) | skeleton 읽기부터 `make test` 통과까지의 전체 타임라인 |
