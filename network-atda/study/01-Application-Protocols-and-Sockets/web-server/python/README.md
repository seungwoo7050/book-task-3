# Python 구현 안내

## 이 폴더의 역할
이 디렉터리는 `Web Server`의 공개 구현을 담습니다. `problem/`의 제공 자료와 분리된 사용자 작성 답안을 이 폴더에서 확인합니다.

## 먼저 볼 파일
- `python/src/web_server.py` - 핵심 구현 진입점입니다.
- `python/tests/test_web_server.py` - 검증 의도와 보조 테스트를 확인합니다.

## 기준 명령
- 검증: `make -C study/01-Application-Protocols-and-Sockets/web-server/problem test`

## 현재 범위
TCP 소켓과 `HTTP/1.1` 응답 조합으로 정적 파일 서버를 구현하는 파일럿 과제입니다.

## 남은 약점
- path traversal 방어는 아직 구현하지 않았습니다.
- 스레드 수 제한이나 thread pool은 없습니다.
- GET 외 메서드는 지원하지 않습니다.
