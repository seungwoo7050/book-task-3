# Web Server structure guide

## 이 글의 중심 질문

- TCP 연결 하나를 받아 HTTP 요청, 파일 조회, 404 응답까지 어디서 나눠 구현했는가?
- 한 줄 답: TCP 소켓과 `HTTP/1.1` 응답 조합으로 정적 파일 서버를 구현하는 파일럿 과제입니다.

## 권장 흐름

1. 실행 표면과 entrypoint를 먼저 고정하기
2. 요청 파싱과 200/404 분기를 한 흐름으로 묶기
3. 테스트와 남은 범위를 정리하기

## 꼭 살릴 근거

- `problem/Makefile`의 공개 target과 `make -C study/01-Application-Protocols-and-Sockets/web-server/problem test`
- `study/01-Application-Protocols-and-Sockets/web-server/python/src/web_server.py`의 `def handle_client`
- `study/01-Application-Protocols-and-Sockets/web-server/python/tests/test_web_server.py`의 `def test_200_ok_for_existing_file`

## 리라이트 주의점

- `Web Server`를 개념 강의처럼 풀지 말고, 실제 파일과 CLI 순서로 보여 준다.
- 전체 로그를 덤프하지 말고 판단을 바꾼 줄만 남긴다.
- 마지막에는 path traversal 방어는 아직 구현하지 않았습니다. 같은 남은 경계를 사람 말로 다시 정리한다.
