# web-server 문제지

## 왜 중요한가

이 문서는 Web Server를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 구현 세부와 공개 구현 경로는 상위 프로젝트 README가 연결하는 경로를 따라가면 됩니다.

## 목표

시작 위치의 구현을 완성해 정상 200 응답: 요청한 파일이 있을 때 유효한 HTTP/1.1 200 OK 응답을 돌려줍니다, 정상 404 응답: 없는 파일 요청에 404 Not Found 페이지를 반환합니다, 연결 처리: 요청을 처리한 뒤 연결을 적절히 닫고 서버는 계속 살아 있습니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/01-Application-Protocols-and-Sockets/web-server/problem/code/server_skeleton.py`
- `../study/01-Application-Protocols-and-Sockets/web-server/python/src/web_server.py`
- `../study/01-Application-Protocols-and-Sockets/web-server/problem/script/test_server.sh`
- `../study/01-Application-Protocols-and-Sockets/web-server/python/tests/test_web_server.py`
- `../study/01-Application-Protocols-and-Sockets/web-server/problem/data/hello.html`
- `../study/01-Application-Protocols-and-Sockets/web-server/problem/Makefile`

## starter code / 입력 계약

- ../study/01-Application-Protocols-and-Sockets/web-server/problem/code/server_skeleton.py에서 starter 코드와 입력 경계를 잡는다.

## 핵심 요구사항

- 정상 200 응답: 요청한 파일이 있을 때 유효한 HTTP/1.1 200 OK 응답을 돌려줍니다.
- 정상 404 응답: 없는 파일 요청에 404 Not Found 페이지를 반환합니다.
- 연결 처리: 요청을 처리한 뒤 연결을 적절히 닫고 서버는 계속 살아 있습니다.
- 멀티스레드 처리: 요청마다 별도 스레드로 처리합니다.
- 코드 품질: 읽기 쉽고 일관된 Python 코드로 정리되어 있습니다.

## 제외 범위

- `../study/01-Application-Protocols-and-Sockets/web-server/problem/code/server_skeleton.py` starter skeleton을 정답 구현으로 착각하지 않는다.
- `../study/01-Application-Protocols-and-Sockets/web-server/problem/script/test_server.sh` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.

## 성공 체크리스트

- `../study/01-Application-Protocols-and-Sockets/web-server/problem/code/server_skeleton.py`의 빈 확장 지점을 실제 구현으로 채웠다.
- 핵심 흐름은 `get_content_type`와 `handle_client`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `send_request`와 `TestWebServer`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/01-Application-Protocols-and-Sockets/web-server/problem/script/test_server.sh` 등 fixture/trace 기준으로 결과를 대조했다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/network-atda/study/01-Application-Protocols-and-Sockets/web-server/problem test
```

- `web-server`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`web-server_answer.md`](web-server_answer.md)에서 확인한다.
