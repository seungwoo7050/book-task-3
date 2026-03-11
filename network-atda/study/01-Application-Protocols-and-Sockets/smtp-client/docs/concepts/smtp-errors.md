# SMTP 응답 코드와 에러 처리 패턴

## 개요

SMTP 프로토콜은 모든 서버 응답에 3자리 숫자 코드를 사용한다. SMTP 클라이언트는 각 명령 후 응답 코드를 확인하여 대화(dialogue)를 계속할지, 재시도할지, 중단할지 결정한다. 이 문서는 응답 코드 체계와 클라이언트의 에러 처리 패턴을 정리한다.

## 응답 코드 분류 체계

### 첫째 자리 — 결과 카테고리

| 코드 | 의미 | 클라이언트 동작 |
| :--- | :--- | :--- |
| `2xx` | **성공** — 요청 완료 | 다음 단계로 진행 |
| `3xx` | **중간 상태** — 추가 입력 대기 | 데이터 전송 계속 |
| `4xx` | **일시적 실패** — 나중에 재시도 | 잠시 후 재시도 |
| `5xx` | **영구적 실패** — 재시도 무의미 | 에러 보고 후 중단 |

### 대화 단계별 기대 코드

| 단계 | 명령 | 기대 코드 | 의미 |
| :--- | :--- | :---: | :--- |
| 연결 | — (접속) | `220` | 서비스 준비 완료 |
| 인사 | `HELO`/`EHLO` | `250` | 인사 수락 |
| 발신자 | `MAIL FROM:` | `250` | 발신자 수락 |
| 수신자 | `RCPT TO:` | `250` | 수신자 수락 |
| 데이터 시작 | `DATA` | `354` | 메시지 입력 시작 |
| 데이터 종료 | `.`(마침표) | `250` | 메시지 수신 완료 |
| 종료 | `QUIT` | `221` | 세션 종료 확인 |

## Python에서의 에러 처리 구현

### 기본 패턴: 응답 코드 검증 함수

```python
def check_reply(reply: str, expected_code: str) -> None:
    if not reply.startswith(expected_code):
        raise RuntimeError(
            f"Expected {expected_code}, got: {reply.strip()}"
        )
```

이 함수를 각 명령 후에 호출하여 대화의 무결성을 보장한다:

```python
greeting = recv_reply(sock)
check_reply(greeting, "220")     # 연결 실패 시 즉시 중단

reply = send_command(sock, "HELO localhost")
check_reply(reply, "250")        # HELO 거부 시 중단

reply = send_command(sock, f"MAIL FROM:<{sender}>")
check_reply(reply, "250")        # 발신자 거부 시 중단
```

### 소켓 레벨 에러

| 예외 | 원인 | 대처 |
| :--- | :--- | :--- |
| `ConnectionRefusedError` | 서버가 실행 중이지 않음 | 연결 실패 보고 |
| `socket.timeout` | 서버 응답 시간 초과 | 타임아웃 에러 보고 |
| `socket.gaierror` | 호스트명 DNS 해석 실패 | 호스트 확인 요청 |
| `BrokenPipeError` | 서버가 연결을 끊음 | 세션 비정상 종료 처리 |

### 종합 에러 처리

```python
try:
    main(server, port, sender, recipient)
except RuntimeError as e:
    print(f"[ERROR] SMTP dialogue failed: {e}")
    sys.exit(1)
except ConnectionRefusedError:
    print(f"[ERROR] Cannot connect to {server}:{port}")
    sys.exit(1)
except socket.timeout:
    print(f"[ERROR] Connection timed out")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] Unexpected: {e}")
    sys.exit(1)
```

## Dot-Stuffing

이메일 본문에서 줄의 시작이 마침표(`.`)인 경우, SMTP 프로토콜이 이를 데이터 종료 마커로 오인할 수 있다.

**해결**: 줄 시작의 마침표 앞에 추가 마침표를 삽입 (dot-stuffing):

```python
# 원본: ".hidden line"
# 전송: "..hidden line"
lines = body.split("\n")
stuffed = []
for line in lines:
    if line.startswith("."):
        line = "." + line
    stuffed.append(line)
body = "\n".join(stuffed)
```

이 과제에서는 단순한 메시지만 다루므로 dot-stuffing을 생략했지만, 프로덕션 클라이언트에서는 필수이다.

## EHLO vs HELO

| 명령 | 특징 |
| :--- | :--- |
| `HELO` | 기본 SMTP (RFC 821) |
| `EHLO` | 확장 SMTP (RFC 5321) — 서버 확장 기능 목록 반환 |

`EHLO`는 `STARTTLS`, `AUTH`, `PIPELINING` 등 서버 지원 확장을 알려준다. 이 과제에서는 `HELO`만으로 충분하다.

## 참고 자료

- [RFC 5321 — SMTP](https://www.rfc-editor.org/rfc/rfc5321)
- [RFC 5322 — Internet Message Format](https://www.rfc-editor.org/rfc/rfc5322)
- Kurose & Ross, *Computer Networking* — Chapter 2.3 (Electronic Mail)
