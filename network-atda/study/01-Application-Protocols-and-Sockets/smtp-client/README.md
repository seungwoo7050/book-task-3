# SMTP Client

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 SMTP 메일 클라이언트 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 |
| 정식 검증 | `make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem test` |

## 문제가 뭐였나
- 문제 배경: `Computer Networking: A Top-Down Approach`의 SMTP 메일 클라이언트 과제를 현재 저장소 구조에 맞게 정리한 프로젝트
- 이 단계에서의 역할: HTTP와 비슷하게 텍스트 명령을 쓰지만 상태 전이가 더 길고 명확해서, 응용 계층 프로토콜의 단계적 흐름을 연습하기 좋습니다.

## 제공된 자료
- `problem/code/smtp_client_skeleton.py`: 시작용 skeleton 코드
- `problem/script/mock_smtp_server.py`: 로컬 모의 SMTP 서버
- `problem/script/test_smtp.sh`: 정식 검증 스크립트

## 이 레포의 답
- 한 줄 답: 텍스트 기반 명령-응답 프로토콜을 TCP 위에서 직접 수행하는 메일 클라이언트 과제입니다.
- 공개 답안 위치: `python/src/`
- 보조 공개 표면: `python/tests/`
- 보조 공개 표면: `docs/`
- 보조 공개 표면: `study/blog/01-Application-Protocols-and-Sockets/smtp-client/`
- 읽는 순서:
  1. `problem/README.md` - 문제 조건, 제공 자료, 성공 기준을 먼저 확인합니다.
  2. `python/README.md` - 현재 공개 답안 범위와 기준 명령을 확인합니다.
  3. `../../blog/01-Application-Protocols-and-Sockets/smtp-client/README.md` - 실제 소스 기준의 개발 chronology를 따라갑니다.
  4. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.
  5. `notion/README.md` - 공개 학습 노트이지만 엔트리포인트는 아닙니다.

## 어떻게 검증하나
- 실행: `make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem run-solution`
- 검증: `make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 무엇을 배웠나
- 3자리 SMTP 응답 코드에 따른 제어 흐름
- `CRLF`와 `DATA` 종료 구분자 처리
- envelope 주소와 헤더 주소의 차이
- 예상하지 못한 응답 코드를 빠르게 중단시키는 fail-fast 구조

## 현재 한계
- `STARTTLS`는 구현하지 않았습니다.
- `AUTH LOGIN`은 구현하지 않았습니다.
- 외부 SMTP 서버 정책과의 차이는 검증하지 않았습니다.
