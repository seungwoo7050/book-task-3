# Web Server

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 웹 서버 구현 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 |
| 정식 검증 | `make -C study/01-Application-Protocols-and-Sockets/web-server/problem test` |

## 문제가 뭐였나
- 문제 배경: `Computer Networking: A Top-Down Approach`의 웹 서버 구현 과제를 현재 저장소 구조에 맞게 정리한 프로젝트
- 이 단계에서의 역할: 이 트랙의 출발점으로, 연결 수립부터 요청 파싱, 파일 읽기, 응답 생성, 연결 종료까지 서버의 기본 생애주기를 가장 짧은 경로로 경험하게 합니다.

## 제공된 자료
- `problem/code/server_skeleton.py`: 시작용 skeleton 코드
- `problem/data/hello.html`: 정적 파일 서빙 확인용 샘플 HTML
- `problem/script/test_server.sh`: 정식 검증을 호출하는 스크립트

## 이 레포의 답
- 한 줄 답: TCP 소켓과 `HTTP/1.1` 응답 조합으로 정적 파일 서버를 구현하는 파일럿 과제입니다.
- 공개 답안 위치: `python/src/`
- 보조 공개 표면: `python/tests/`
- 보조 공개 표면: `docs/`
- 읽는 순서:
  1. `problem/README.md` - 문제 조건, 제공 자료, 성공 기준을 먼저 확인합니다.
  2. `python/README.md` - 현재 공개 답안 범위와 기준 명령을 확인합니다.
  3. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.
  4. `notion/README.md` - 공개 학습 노트이지만 엔트리포인트는 아닙니다.

## 어떻게 검증하나
- 실행: `make -C study/01-Application-Protocols-and-Sockets/web-server/problem run-solution`
- 검증: `make -C study/01-Application-Protocols-and-Sockets/web-server/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 무엇을 배웠나
- HTTP 요청 라인의 최소 파싱 규칙
- 정적 파일 서빙과 `Content-Type` 결정
- 404 응답 생성과 연결 종료 시점
- 요청마다 스레드를 분리하는 기본 accept loop 구조

## 현재 한계
- path traversal 방어는 아직 구현하지 않았습니다.
- 스레드 수 제한이나 thread pool은 없습니다.
- GET 외 메서드는 지원하지 않습니다.
