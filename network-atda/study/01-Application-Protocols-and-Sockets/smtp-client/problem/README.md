# SMTP Client 문제 안내

## 이 문서의 역할

이 문서는 `SMTP Client`를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 구현 세부와 공개 구현 경로는 상위 프로젝트 README가 연결하는 경로를 따라가면 됩니다.

## 문제 목표

`smtplib` 없이 TCP 소켓 위에서 직접 SMTP 대화를 수행해 메일 한 통을 보내는 클라이언트를 구현합니다.

## 구현해야 할 동작

### TCP 연결

- SMTP 서버에 연결합니다.
- 서버가 먼저 보내는 `220` greeting을 읽습니다.

### SMTP 대화 수행

- `HELO`, `MAIL FROM`, `RCPT TO`, `DATA`, 본문 전송, `QUIT` 순서로 명령을 보냅니다.
- 각 단계마다 기대하는 응답 코드(`250`, `354`, `221`)를 확인합니다.

### 메시지 형식

- `DATA` 구간에는 `From`, `To`, `Subject` 헤더와 본문을 포함합니다.
- 본문 끝은 `
.
`으로 마무리합니다.

### 오류 처리

- 예상하지 못한 응답 코드가 오면 오류를 출력하고 안전하게 종료합니다.

### 선택 확장

- 가능하다면 `STARTTLS`, `AUTH LOGIN`을 후속 실험 과제로 다룰 수 있습니다.

## 제공 자료와 실행 환경

- starter code: `code/smtp_client_skeleton.py`
- 로컬 모의 서버: `script/mock_smtp_server.py`
- 검증 스크립트: `script/test_smtp.sh`

## 제약과 해석 기준

- Python 3 표준 라이브러리만 사용합니다.
- `smtplib`은 사용하지 않습니다.
- TLS가 필요하다면 `ssl`, 인증이 필요하다면 `base64` 같은 표준 모듈만 사용합니다.

## 성공 기준

| 항목 | 내용 |
| :--- | :--- |
| 완전한 SMTP 대화 | 필수 SMTP 명령을 올바른 순서로 전송합니다. |
| 응답 코드 검증 | 각 단계에서 응답 코드를 확인하고 다음 단계로 진행합니다. |
| 메시지 전송 | 메일 본문이 정상적으로 전달되거나 로컬 디버그 서버에 기록됩니다. |
| 오류 처리 | 예상치 못한 응답 코드에 적절히 반응합니다. |
| 코드 품질 | 읽기 쉽고 흐름이 분명한 Python 코드입니다. |

## 출력 예시

```text
Connecting to smtp.example.com:587 ...
S: 220 smtp.example.com ESMTP ready
C: HELO localhost
S: 250 Hello localhost
...
C: QUIT
S: 221 Bye
Email sent successfully!
```
