# 04 지식 인덱스

## 핵심 용어
- **request line**: `GET /index.html HTTP/1.1`처럼 메서드, 경로, 버전을 담는 첫 줄이다.
- **`Content-Type`**: 브라우저가 본문을 어떤 형식으로 해석할지 결정하는 헤더다.
- **`SO_REUSEADDR`**: 개발 중 빠른 재시작을 가능하게 해 주는 소켓 옵션이다.
- **thread-per-connection**: 요청 처리 흐름을 이해하기 쉬우나 접속 수가 늘면 비용이 커지는 단순 동시성 모델이다.

## 다시 볼 파일
- [`../problem/code/server_skeleton.py`](../problem/code/server_skeleton.py): 제공된 시작점과 구현해야 할 최소 범위를 다시 확인할 때 본다.
- [`../python/src/web_server.py`](../python/src/web_server.py): 요청 파싱, 응답 생성, MIME 결정이 한 파일에 모여 있어 현재 동작을 이해하기 좋다.
- [`../python/tests/test_web_server.py`](../python/tests/test_web_server.py): 무엇을 기준으로 `verified`라고 부르는지 가장 명확하게 보여준다.
- [`../docs/concepts/http.md`](../docs/concepts/http.md): 요청/응답 형식을 다시 떠올릴 때 가장 먼저 읽는다.

## 자주 쓰는 확인 명령
- `make -C study/Application-Protocols-and-Sockets/web-server/problem test`
- `cd study/Application-Protocols-and-Sockets/web-server/python/tests && python3 -m pytest test_web_server.py -v`

## 참고 자료
- [`../docs/references/README.md`](../docs/references/README.md): 공개 문서를 정리할 때 다시 확인한 근거 모음
