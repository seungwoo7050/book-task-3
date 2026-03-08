# Python 구현 안내

이 디렉터리는 `Web Server`의 공개 구현을 담는다.

## 구성

- `src/web_server.py`
- `tests/test_web_server.py`

## 기준 명령

- 실행: `make -C study/Application-Protocols-and-Sockets/web-server/problem run-solution`
- 검증: `make -C study/Application-Protocols-and-Sockets/web-server/problem test`

## 구현 메모

- 상태: `verified`
- 현재 범위: GET 요청과 정적 파일 서빙 범위만 다룬다. keep-alive, path traversal 방어, 고급 라우팅은 후속 주제다.
- 남은 약점: path traversal 방어 미구현
- 남은 약점: 무제한 스레드 생성
- 남은 약점: GET 외 메서드 미지원
