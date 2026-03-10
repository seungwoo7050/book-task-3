# Web Server

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 웹 서버 구현 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 |
| 정식 검증 | `make -C study/Application-Protocols-and-Sockets/web-server/problem test` |

## 한 줄 요약

TCP 소켓과 `HTTP/1.1` 응답 조합으로 정적 파일 서버를 구현하는 파일럿 과제입니다.

## 왜 이 프로젝트가 필요한가

이 트랙의 출발점으로, 연결 수립부터 요청 파싱, 파일 읽기, 응답 생성, 연결 종료까지 서버의 기본 생애주기를 가장 짧은 경로로 경험하게 합니다.

## 이런 학습자에게 맞습니다

- TCP 서버를 처음 직접 구현해 보고 싶은 학습자
- HTTP 요청 라인을 문자열 수준에서 어떻게 파싱하는지 보고 싶은 학습자

## 지금 바로 읽는 순서

1. `problem/README.md` - 구현 목표, 제공 자료, 성공 기준을 먼저 확인합니다.
2. `python/README.md` - 공개 구현 범위와 정식 검증 명령을 확인합니다.
3. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.
4. `notion/README.md` - 더 깊은 작업 기록과 회고가 필요할 때 참고합니다.

## 제공 자료

- `problem/code/server_skeleton.py`: 시작용 skeleton 코드
- `problem/data/hello.html`: 정적 파일 서빙 확인용 샘플 HTML
- `problem/script/test_server.sh`: 정식 검증을 호출하는 스크립트

## 실행과 검증

- 실행: `make -C study/Application-Protocols-and-Sockets/web-server/problem run-solution`
- 검증: `make -C study/Application-Protocols-and-Sockets/web-server/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 학습 포인트

- HTTP 요청 라인의 최소 파싱 규칙
- 정적 파일 서빙과 `Content-Type` 결정
- 404 응답 생성과 연결 종료 시점
- 요청마다 스레드를 분리하는 기본 accept loop 구조

## 현재 한계

- path traversal 방어는 아직 구현하지 않았습니다.
- 스레드 수 제한이나 thread pool은 없습니다.
- GET 외 메서드는 지원하지 않습니다.

## 포트폴리오로 확장하기

- `path traversal` 방어, thread pool, access log를 추가하면 학습용 서버가 더 설득력 있는 공개 데모로 발전합니다.
- 응답 예시와 실패 예시를 함께 캡처해 두면 "무엇을 구현했고 무엇은 아직 아닌지"를 깔끔하게 설명할 수 있습니다.
- 도커나 간단한 배포 스크립트를 붙이기 전에도, 로컬 재현 명령과 테스트 결과만 정리해 두면 충분히 좋은 출발점이 됩니다.
