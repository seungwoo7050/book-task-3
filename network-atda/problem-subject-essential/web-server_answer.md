# web-server 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 정상 200 응답: 요청한 파일이 있을 때 유효한 HTTP/1.1 200 OK 응답을 돌려줍니다, 정상 404 응답: 없는 파일 요청에 404 Not Found 페이지를 반환합니다, 연결 처리: 요청을 처리한 뒤 연결을 적절히 닫고 서버는 계속 살아 있습니다를 한 흐름으로 설명하고 검증한다. 핵심은 `get_content_type`와 `handle_client`, `main` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 정상 200 응답: 요청한 파일이 있을 때 유효한 HTTP/1.1 200 OK 응답을 돌려줍니다.
- 정상 404 응답: 없는 파일 요청에 404 Not Found 페이지를 반환합니다.
- 연결 처리: 요청을 처리한 뒤 연결을 적절히 닫고 서버는 계속 살아 있습니다.
- 첫 진입점은 `../study/01-Application-Protocols-and-Sockets/web-server/python/src/web_server.py`이고, 여기서 `get_content_type`와 `handle_client` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/01-Application-Protocols-and-Sockets/web-server/python/src/web_server.py`: `get_content_type`, `handle_client`, `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/01-Application-Protocols-and-Sockets/web-server/problem/code/server_skeleton.py`: `handle_client`, `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/01-Application-Protocols-and-Sockets/web-server/problem/script/test_server.sh`: 검증 절차나 보조 자동화를 담아 결과를 재현하는 스크립트다.
- `../study/01-Application-Protocols-and-Sockets/web-server/python/tests/test_web_server.py`: `send_request`, `TestWebServer`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/01-Application-Protocols-and-Sockets/web-server/problem/data/hello.html`: 핵심 구현을 담는 파일이다.
- `../study/01-Application-Protocols-and-Sockets/web-server/problem/Makefile`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.
- `get_content_type` 구현은 `send_request` 등이 잠근 입력 계약과 상태 전이를 그대로 만족해야 한다.
- 회귀 게이트는 `make -C /Users/woopinbell/work/book-task-3/network-atda/study/01-Application-Protocols-and-Sockets/web-server/problem test`이며, 핵심 상태 전이를 바꿀 때마다 중간 검증으로 다시 실행한다.

## 정답을 재구성하는 절차

1. `../study/01-Application-Protocols-and-Sockets/web-server/problem/code/server_skeleton.py`와 `../study/01-Application-Protocols-and-Sockets/web-server/python/src/web_server.py`를 나란히 열어 먼저 바뀌는 경계를 잡는다.
2. `send_request` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make -C /Users/woopinbell/work/book-task-3/network-atda/study/01-Application-Protocols-and-Sockets/web-server/problem test`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make -C /Users/woopinbell/work/book-task-3/network-atda/study/01-Application-Protocols-and-Sockets/web-server/problem test
```

- `../study/01-Application-Protocols-and-Sockets/web-server/problem/code/server_skeleton.py` starter skeleton의 빈칸을 그대로 정답으로 착각하지 않는다.
- `send_request`와 `TestWebServer`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make -C /Users/woopinbell/work/book-task-3/network-atda/study/01-Application-Protocols-and-Sockets/web-server/problem test`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/01-Application-Protocols-and-Sockets/web-server/python/src/web_server.py`
- `../study/01-Application-Protocols-and-Sockets/web-server/problem/code/server_skeleton.py`
- `../study/01-Application-Protocols-and-Sockets/web-server/problem/script/test_server.sh`
- `../study/01-Application-Protocols-and-Sockets/web-server/python/tests/test_web_server.py`
- `../study/01-Application-Protocols-and-Sockets/web-server/problem/data/hello.html`
- `../study/01-Application-Protocols-and-Sockets/web-server/problem/Makefile`
