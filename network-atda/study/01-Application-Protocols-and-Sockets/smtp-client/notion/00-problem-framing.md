# 00 문제 프레이밍

## 프로젝트 정의
- 프로젝트: `SMTP Client`
- 상태: `verified`
- 기준 검증: `make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem test`
- 문제 배경: 텍스트 기반 애플리케이션 프로토콜이 실제로는 어떤 상태 기계로 동작하는지 배우는 SMTP 클라이언트 프로젝트다.

## 이번 범위
- 서버에 연결해 `220` greeting을 읽고, `HELO`부터 `QUIT`까지 기본 SMTP 대화를 수행한다.
- `MAIL FROM`, `RCPT TO`, `DATA` 순서를 지켜 한 통의 메일을 전송한다.
- 실패 응답 코드를 만나면 즉시 에러로 처리한다.

## 제약과 전제
- 검증은 로컬 mock SMTP 서버 기준으로 진행한다.
- 줄 끝은 `CRLF`를 사용해야 하고, `DATA` 끝은 `
.
`으로 닫아야 한다.
- TLS, 인증, MIME multipart, 멀티라인 응답의 완전 지원은 범위 밖이다.

## 성공 기준
- mock 서버와의 전체 SMTP 대화가 지정된 코드 순서대로 끝난다.
- 잘못된 응답 코드를 만나면 조용히 넘어가지 않고 실패로 처리한다.
- `make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem test`가 통과한다.

## 공개 문서
- [`../README.md`](../README.md)
- [`../problem/README.md`](../problem/README.md)
- [`../python/README.md`](../python/README.md)
- [`../docs/README.md`](../docs/README.md)
- [`../docs/references/README.md`](../docs/references/README.md)

## 이번에 일부러 제외한 것
- 실제 메일 서비스 연동, `STARTTLS`, 인증은 구현하지 않는다.
- 헤더 인코딩과 첨부파일 처리는 다루지 않는다.
