# SMTP Client — 개발 타임라인

## Phase 0: 환경 준비

```bash
python3 --version
# 표준 라이브러리: socket, sys
# 테스트: pytest
pip install pytest

# 디버깅 SMTP 서버 선택지 확인
python3 -m smtpd -n -c DebuggingServer localhost:1025   # deprecated 경고 있음
# 또는
pip install aiosmtpd
python3 -m aiosmtpd -n -l localhost:1025
```

이 과제에서는 제공된 `problem/script/mock_smtp_server.py`를 사용하므로 외부 패키지 불필요.

## Phase 1: skeleton 분석

**파일**: `problem/code/smtp_client_skeleton.py`

- TCP 소켓 생성 코드 제공됨
- SMTP 명령 전송 부분이 비어있음
- `recv_reply()`, `send_command()`, `check_reply()` 함수 시그니처 확인

## Phase 2: TCP 연결 및 220 greeting 수신

**작업 파일**: `python/src/smtp_client.py`

1. `socket.socket(AF_INET, SOCK_STREAM)` — TCP 소켓 생성
2. `client_socket.settimeout(10)` — 10초 타임아웃
3. `client_socket.connect((server, port))` — 서버 연결
4. `recv_reply()` — 서버의 220 greeting 수신
5. `check_reply(greeting, "220")` — 응답 코드 검증

**CLI 확인**:
```bash
# 터미널 1: mock SMTP 서버 기동
python3 problem/script/mock_smtp_server.py localhost 1025

# 터미널 2: 연결만 테스트
python3 -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 1025))
print(s.recv(1024).decode())
s.close()
"
# → 220 localhost Mock SMTP Service Ready
```

## Phase 3: recv_reply / send_command 헬퍼

1. `recv_reply(sock)`: `sock.recv(4096).decode()` 후 `S:` 접두어로 출력
2. `send_command(sock, command)`: `f"{command}\r\n"` 전송 후 `recv_reply()` 호출
3. 모든 명령에 CRLF(`\r\n`) 종단 보장

## Phase 4: SMTP 대화 시퀀스 구현

순서대로 구현:

1. **HELO**: `send_command(sock, f"HELO {socket.gethostname()}")` → `250` 확인
2. **MAIL FROM**: `send_command(sock, f"MAIL FROM:<{sender}>")` → `250` 확인
3. **RCPT TO**: `send_command(sock, f"RCPT TO:<{recipient}>")` → `250` 확인
4. **DATA**: `send_command(sock, "DATA")` → `354` 확인

## Phase 5: 메시지 본문 전송

1. 헤더 조립: `From:`, `To:`, `Subject:`
2. 빈 줄로 헤더와 본문 구분 (`\r\n`)
3. 본문 텍스트
4. 종료 시퀀스: `\r\n.\r\n` — 마침표만 있는 줄
5. `sock.sendall(message.encode())` 전송
6. `recv_reply()` → `250` 확인

## Phase 6: QUIT 및 정리

1. `send_command(sock, "QUIT")` → `221` 확인
2. `client_socket.close()` — 소켓 닫기

## Phase 7: check_reply — fail-fast 패턴

```python
def check_reply(reply: str, expected_code: str) -> None:
    if not reply.startswith(expected_code):
        raise RuntimeError(f"Expected {expected_code}, got: {reply.strip()}")
```

- 매 단계마다 호출하여 실패 지점 즉시 표시
- RuntimeError로 전파 → main에서 포착

## Phase 8: CLI 인터페이스

```python
if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python3 smtp_client.py <server> <port> <sender> <recipient>")
        sys.exit(1)
    main(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4])
```

**CLI 실행**:
```bash
python3 python/src/smtp_client.py localhost 1025 alice@example.com bob@example.com
```

## Phase 9: 테스트 작성

**작업 파일**: `python/tests/test_smtp_client.py`

- mock SMTP 서버를 프로세스로 기동
- 솔루션이 정상적으로 SMTP 대화를 완료하는지 검증

## Phase 10: Makefile 통합 검증

```bash
make -C problem test
```

내부 동작:
1. `mock_smtp_server.py`를 백그라운드로 기동 → 로그를 `/tmp/net_smtp_mock.log`에 기록
2. `script/test_smtp.sh`가 솔루션 실행 후 출력 검사
3. `trap`으로 mock 서버 자동 종료

## 최종 파일 구조

```
smtp-client/
├── python/
│   ├── src/smtp_client.py           ← 솔루션 (140줄)
│   └── tests/test_smtp_client.py    ← pytest 테스트
├── problem/
│   ├── Makefile                     ← make test / make run-solution
│   ├── code/smtp_client_skeleton.py ← 제공 skeleton
│   └── script/
│       ├── mock_smtp_server.py      ← 테스트용 mock 서버
│       └── test_smtp.sh             ← bash 검증 스크립트
├── docs/concepts/
└── notion/                          ← 이 문서
```
