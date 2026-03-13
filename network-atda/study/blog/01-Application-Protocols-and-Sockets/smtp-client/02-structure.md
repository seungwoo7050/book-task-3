# SMTP Client structure guide

## 이 글의 중심 질문

- SMTP 대화를 raw socket 위에서 단계별 명령으로 어떻게 끝까지 완주했는가?
- 한 줄 답: 텍스트 기반 명령-응답 프로토콜을 TCP 위에서 직접 수행하는 메일 클라이언트 과제입니다.

## 권장 흐름

1. 실행 표면과 entrypoint를 먼저 고정하기
2. 명령 전송과 응답 확인을 대화 단계에 맞춰 정리하기
3. 테스트와 남은 범위를 정리하기

## 꼭 살릴 근거

- `problem/Makefile`의 공개 target과 `make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem test`
- `study/01-Application-Protocols-and-Sockets/smtp-client/python/src/smtp_client.py`의 `def send_command`
- `study/01-Application-Protocols-and-Sockets/smtp-client/python/tests/test_smtp_client.py`의 `def test_full_smtp_dialogue`

## 리라이트 주의점

- `SMTP Client`를 개념 강의처럼 풀지 말고, 실제 파일과 CLI 순서로 보여 준다.
- 전체 로그를 덤프하지 말고 판단을 바꾼 줄만 남긴다.
- 마지막에는 `STARTTLS`는 구현하지 않았습니다. 같은 남은 경계를 사람 말로 다시 정리한다.
