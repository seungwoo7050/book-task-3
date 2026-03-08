# SMTP Client

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 레거시 원본 | `legacy/Programming-Assignments/smtp-client` |
| 정식 검증 | `make -C study/Application-Protocols-and-Sockets/smtp-client/problem test` |

## 한 줄 요약

텍스트 기반 명령-응답 프로토콜을 TCP 위에서 직접 수행하는 메일 클라이언트 과제다.

## 문제 요약

HELO, MAIL FROM, RCPT TO, DATA, QUIT 순서의 SMTP 대화를 소켓 레벨에서 수행하고 각 응답 코드를 검증한다.

## 이 프로젝트를 여기 둔 이유

HTTP와 비슷한 텍스트 프로토콜이지만 다단계 상태 전이가 더 명확한 사례로, 응용 계층 프로토콜 해석 훈련에 적합하다.

## 제공 자료

- `problem/code/smtp_client_skeleton.py` skeleton
- `problem/script/mock_smtp_server.py` 로컬 모의 서버
- `problem/script/test_smtp.sh` 자동 검증

## 학습 포인트

- 3자리 SMTP 응답 코드 기반 제어 흐름
- CRLF와 DATA 종료 구분자
- envelope 주소와 헤더 주소의 차이
- 실패 지점을 빠르게 드러내는 fail-fast 구조

## 실행과 검증

- 실행: `make -C study/Application-Protocols-and-Sockets/smtp-client/problem run-solution`
- 검증: `make -C study/Application-Protocols-and-Sockets/smtp-client/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 현재 범위와 한계

인증과 TLS는 문서에서만 다루고, 공개 구현은 평문 SMTP 대화와 로컬 검증에 집중한다.

- 현재 한계: STARTTLS 미구현
- 현재 한계: AUTH LOGIN 미구현
- 현재 한계: 외부 SMTP 서버와의 정책 차이 미검증

## Public / Private 경계

- `problem/`은 제공 자료와 canonical 검증 래퍼만 둔다.
- `python/` 또는 `analysis/`는 공개 구현과 공개 답안만 둔다.
- `docs/`는 반복해서 참고할 개념 메모만 유지한다.
- `notion/`은 노션 업로드용 작업 노트이며 저장소 공개 구조에 의존하지 않는다.
