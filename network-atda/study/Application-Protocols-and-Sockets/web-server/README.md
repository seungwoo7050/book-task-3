# Web Server

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 레거시 원본 | `legacy/Programming-Assignments/web-server` |
| 정식 검증 | `make -C study/Application-Protocols-and-Sockets/web-server/problem test` |

## 한 줄 요약

TCP 소켓과 HTTP/1.1 응답 조합으로 정적 파일 서버를 구현하는 파일럿 과제다.

## 문제 요약

브라우저나 curl이 보내는 GET 요청을 받아 파일을 읽고, 존재하면 200 OK와 함께 반환하고 없으면 404 응답을 만든다.

## 이 프로젝트를 여기 둔 이유

이 트랙의 시작점으로, 소켓 수명주기와 텍스트 기반 응답 포맷을 가장 단순한 형태로 익히게 한다.

## 제공 자료

- `problem/code/server_skeleton.py` skeleton
- `problem/data/hello.html` 샘플 파일
- `problem/script/test_server.sh` 자동 검증 스크립트

## 학습 포인트

- HTTP 요청 라인의 최소 파싱 규칙
- 정적 파일 서빙과 MIME 타입 결정
- 404 처리와 연결 종료 시점
- accept loop와 per-client thread 분리

## 실행과 검증

- 실행: `make -C study/Application-Protocols-and-Sockets/web-server/problem run-solution`
- 검증: `make -C study/Application-Protocols-and-Sockets/web-server/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 현재 범위와 한계

GET 요청과 정적 파일 서빙 범위만 다룬다. keep-alive, path traversal 방어, 고급 라우팅은 후속 주제다.

- 현재 한계: path traversal 방어 미구현
- 현재 한계: 무제한 스레드 생성
- 현재 한계: GET 외 메서드 미지원

## Public / Private 경계

- `problem/`은 제공 자료와 canonical 검증 래퍼만 둔다.
- `python/` 또는 `analysis/`는 공개 구현과 공개 답안만 둔다.
- `docs/`는 반복해서 참고할 개념 메모만 유지한다.
- `notion/`은 노션 업로드용 작업 노트이며 저장소 공개 구조에 의존하지 않는다.
