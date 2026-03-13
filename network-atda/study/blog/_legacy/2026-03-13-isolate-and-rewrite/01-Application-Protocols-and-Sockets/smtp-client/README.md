# SMTP Client blog

이 디렉터리는 `SMTP Client`를 `source-first` 방식으로 다시 읽는 blog 시리즈다. chronology는 프로젝트 README, `problem/README.md`, `problem/Makefile`, `python/src/smtp_client.py`, `python/tests/test_smtp_client.py`를 기준으로 재구성했다.

## source set
- [`../../../01-Application-Protocols-and-Sockets/smtp-client/README.md`](../../../01-Application-Protocols-and-Sockets/smtp-client/README.md)
- [`../../../01-Application-Protocols-and-Sockets/smtp-client/problem/README.md`](../../../01-Application-Protocols-and-Sockets/smtp-client/problem/README.md)
- [`../../../01-Application-Protocols-and-Sockets/smtp-client/problem/Makefile`](../../../01-Application-Protocols-and-Sockets/smtp-client/problem/Makefile)
- [`../../../01-Application-Protocols-and-Sockets/smtp-client/python/src/smtp_client.py`](../../../01-Application-Protocols-and-Sockets/smtp-client/python/src/smtp_client.py)
- [`../../../01-Application-Protocols-and-Sockets/smtp-client/python/tests/test_smtp_client.py`](../../../01-Application-Protocols-and-Sockets/smtp-client/python/tests/test_smtp_client.py)

## 읽는 순서
1. [`00-series-map.md`](00-series-map.md)
2. [`10-development-timeline.md`](10-development-timeline.md)
3. [`../../../01-Application-Protocols-and-Sockets/smtp-client/README.md`](../../../01-Application-Protocols-and-Sockets/smtp-client/README.md)

## 검증 진입점
- `make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem test`

## chronology 메모
- 핵심은 명령을 많이 보내는 것이 아니라, 각 단계가 기대한 3자리 응답 코드로 닫히는지 확인하는 흐름이었다.
- 날짜 근거가 약해 `Day / Session` 형식을 사용했다.
