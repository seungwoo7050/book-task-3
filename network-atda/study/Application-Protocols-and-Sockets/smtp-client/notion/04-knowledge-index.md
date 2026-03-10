# 04 지식 인덱스

## 핵심 용어
- **SMTP envelope**: `MAIL FROM`과 `RCPT TO`처럼 실제 전송 경로를 정하는 명령 집합이다.
- **header**: `From:`, `To:`, `Subject:`처럼 수신자에게 보이는 메시지 메타데이터다.
- **`354`**: 이제 본문 데이터를 보내도 된다는 서버 응답 코드다.
- **`CRLF`**: SMTP가 줄 구분자로 요구하는 `
` 시퀀스다.

## 다시 볼 파일
- [`../problem/script/mock_smtp_server.py`](../problem/script/mock_smtp_server.py): 검증용 서버가 어떤 순서와 응답 코드를 기대하는지 확인할 수 있다.
- [`../python/src/smtp_client.py`](../python/src/smtp_client.py): 명령 송신과 응답 검사가 어떤 단계로 묶여 있는지 읽을 때 본다.
- [`../python/tests/test_smtp_client.py`](../python/tests/test_smtp_client.py): greeting, `HELO`, 전체 대화가 어디까지 자동 검증되는지 보여준다.
- [`../docs/concepts/smtp.md`](../docs/concepts/smtp.md): 응답 코드와 명령 순서를 다시 정리할 때 기준 문서로 쓴다.

## 자주 쓰는 확인 명령
- `make -C study/Application-Protocols-and-Sockets/smtp-client/problem test`
- `cd study/Application-Protocols-and-Sockets/smtp-client/python/tests && python3 -m pytest test_smtp_client.py -v`

## 참고 자료
- [`../docs/references/README.md`](../docs/references/README.md): 공개 문서를 정리할 때 다시 확인한 근거 모음
