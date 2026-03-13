# SMTP Client 시리즈 지도

## 이 프로젝트를 한 줄로

HTTP처럼 텍스트 명령을 쓰지만 상태 전이가 더 길고 엄격한 프로토콜 — SMTP 대화를 raw TCP socket으로 직접 구현하는 과제다. `220` → `250` → `354` → `250` → `221`이라는 응답 코드 시퀀스가 이 프로젝트의 뼈대이고, 한 단계라도 어긋나면 전체 대화가 실패하는 구조를 직접 겪는다.

## 문제 구조
- 제공물: `problem/code/smtp_client_skeleton.py`, `problem/script/mock_smtp_server.py`
- 답안: `python/src/smtp_client.py`, `python/tests/test_smtp_client.py`
- 검증: `make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem test`

## 이 시리즈에서 따라갈 질문
1. SMTP 대화는 왜 한 번에 보내지 않고 단계마다 허가를 기다리는가
2. `check_reply()`라는 단순한 함수가 왜 프로토콜 전체의 안전 장치인가
3. `DATA` 종료 구분자 `"\r\n.\r\n"`의 위치를 놓치면 무엇이 벌어지는가
4. mock 서버 없이 SMTP를 테스트할 수 없는 현실적 이유는 무엇인가

## 글 목록
| 번호 | 파일 | 범위 |
| :--- | :--- | :--- |
| `10` | [`10-development-timeline.md`](10-development-timeline.md) | mock 서버 이해부터 전체 대화 완성까지 |
