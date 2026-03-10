# SMTP Client

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 SMTP 메일 클라이언트 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 |
| 정식 검증 | `make -C study/Application-Protocols-and-Sockets/smtp-client/problem test` |

## 한 줄 요약

텍스트 기반 명령-응답 프로토콜을 TCP 위에서 직접 수행하는 메일 클라이언트 과제입니다.

## 왜 이 프로젝트가 필요한가

HTTP와 비슷하게 텍스트 명령을 쓰지만 상태 전이가 더 길고 명확해서, 응용 계층 프로토콜의 단계적 흐름을 연습하기 좋습니다.

## 이런 학습자에게 맞습니다

- 명령-응답 프로토콜의 상태 전이를 코드로 다뤄 보고 싶은 학습자
- `HELO`, `MAIL FROM`, `RCPT TO`, `DATA`, `QUIT` 흐름을 소켓 레벨에서 확인하고 싶은 학습자

## 지금 바로 읽는 순서

1. `problem/README.md` - 구현 목표, 제공 자료, 성공 기준을 먼저 확인합니다.
2. `python/README.md` - 공개 구현 범위와 정식 검증 명령을 확인합니다.
3. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.
4. `notion/README.md` - 더 깊은 작업 기록과 회고가 필요할 때 참고합니다.

## 제공 자료

- `problem/code/smtp_client_skeleton.py`: 시작용 skeleton 코드
- `problem/script/mock_smtp_server.py`: 로컬 모의 SMTP 서버
- `problem/script/test_smtp.sh`: 정식 검증 스크립트

## 실행과 검증

- 실행: `make -C study/Application-Protocols-and-Sockets/smtp-client/problem run-solution`
- 검증: `make -C study/Application-Protocols-and-Sockets/smtp-client/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 학습 포인트

- 3자리 SMTP 응답 코드에 따른 제어 흐름
- `CRLF`와 `DATA` 종료 구분자 처리
- envelope 주소와 헤더 주소의 차이
- 예상하지 못한 응답 코드를 빠르게 중단시키는 fail-fast 구조

## 현재 한계

- `STARTTLS`는 구현하지 않았습니다.
- `AUTH LOGIN`은 구현하지 않았습니다.
- 외부 SMTP 서버 정책과의 차이는 검증하지 않았습니다.

## 포트폴리오로 확장하기

- `STARTTLS`, `AUTH`, MIME 본문, 첨부파일 지원을 추가하면 도구형 포트폴리오로 확장하기 좋습니다.
- 로컬 디버깅 서버와 실제 공개 SMTP 서버의 차이를 정리하면 프로토콜 이해도가 잘 드러납니다.
- 응답 코드 표와 실패 사례를 함께 넣으면 README가 훨씬 친절해집니다.
