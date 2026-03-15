# smtp-client 문제지

## 왜 중요한가

이 문서는 SMTP Client를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 구현 세부와 공개 구현 경로는 상위 프로젝트 README가 연결하는 경로를 따라가면 됩니다.

## 목표

시작 위치의 구현을 완성해 완전한 SMTP 대화: 필수 SMTP 명령을 올바른 순서로 전송합니다, 응답 코드 검증: 각 단계에서 응답 코드를 확인하고 다음 단계로 진행합니다, 메시지 전송: 메일 본문이 정상적으로 전달되거나 로컬 디버그 서버에 기록됩니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/01-Application-Protocols-and-Sockets/smtp-client/problem/code/smtp_client_skeleton.py`
- `../study/01-Application-Protocols-and-Sockets/smtp-client/python/src/smtp_client.py`
- `../study/01-Application-Protocols-and-Sockets/smtp-client/problem/script/mock_smtp_server.py`
- `../study/01-Application-Protocols-and-Sockets/smtp-client/problem/script/test_smtp.sh`
- `../study/01-Application-Protocols-and-Sockets/smtp-client/python/tests/test_smtp_client.py`
- `../study/01-Application-Protocols-and-Sockets/smtp-client/problem/Makefile`

## starter code / 입력 계약

- ../study/01-Application-Protocols-and-Sockets/smtp-client/problem/code/smtp_client_skeleton.py에서 starter 코드와 입력 경계를 잡는다.

## 핵심 요구사항

- 완전한 SMTP 대화: 필수 SMTP 명령을 올바른 순서로 전송합니다.
- 응답 코드 검증: 각 단계에서 응답 코드를 확인하고 다음 단계로 진행합니다.
- 메시지 전송: 메일 본문이 정상적으로 전달되거나 로컬 디버그 서버에 기록됩니다.
- 오류 처리: 예상치 못한 응답 코드에 적절히 반응합니다.
- 코드 품질: 읽기 쉽고 흐름이 분명한 Python 코드입니다.

## 제외 범위

- `../study/01-Application-Protocols-and-Sockets/smtp-client/problem/code/smtp_client_skeleton.py` starter skeleton을 정답 구현으로 착각하지 않는다.
- `../study/01-Application-Protocols-and-Sockets/smtp-client/problem/script/test_smtp.sh` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.

## 성공 체크리스트

- `../study/01-Application-Protocols-and-Sockets/smtp-client/problem/code/smtp_client_skeleton.py`의 빈 확장 지점을 실제 구현으로 채웠다.
- 핵심 흐름은 `recv_reply`와 `send_command`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `TestSMTPClient`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/01-Application-Protocols-and-Sockets/smtp-client/problem/script/test_smtp.sh` 등 fixture/trace 기준으로 결과를 대조했다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/network-atda/study/01-Application-Protocols-and-Sockets/smtp-client/problem test
```

- `smtp-client`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`smtp-client_answer.md`](smtp-client_answer.md)에서 확인한다.
