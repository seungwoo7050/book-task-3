# 01. Application Protocols and Sockets blog

이 트랙의 blog 시리즈는 socket 위에서 애플리케이션 규칙을 직접 구현할 때 어떤 판단이 생기는지 프로젝트 단위로 복원한다. chronology는 모두 `source-first` 기준으로 다시 썼고, 공통으로 `problem/Makefile`, `python/src/`, `python/tests/`를 함께 읽는다.

## 프로젝트

| 프로젝트 | blog | 원 프로젝트 |
| :--- | :--- | :--- |
| Web Server | [`README.md`](web-server/README.md) | [`../../01-Application-Protocols-and-Sockets/web-server/README.md`](../../01-Application-Protocols-and-Sockets/web-server/README.md) |
| UDP Pinger | [`README.md`](udp-pinger/README.md) | [`../../01-Application-Protocols-and-Sockets/udp-pinger/README.md`](../../01-Application-Protocols-and-Sockets/udp-pinger/README.md) |
| SMTP Client | [`README.md`](smtp-client/README.md) | [`../../01-Application-Protocols-and-Sockets/smtp-client/README.md`](../../01-Application-Protocols-and-Sockets/smtp-client/README.md) |
| Web Proxy | [`README.md`](web-proxy/README.md) | [`../../01-Application-Protocols-and-Sockets/web-proxy/README.md`](../../01-Application-Protocols-and-Sockets/web-proxy/README.md) |

## 읽는 순서
1. [`Web Server`](web-server/README.md)로 TCP request/response의 최소 구조를 먼저 본다.
2. [`UDP Pinger`](udp-pinger/README.md)로 connectionless transport에서 timeout과 RTT를 읽는다.
3. [`SMTP Client`](smtp-client/README.md)로 텍스트 프로토콜의 단계적 state transition을 본다.
4. [`Web Proxy`](web-proxy/README.md)로 중개자 구조와 cache policy를 묶는다.

## source-first 메모
- 구현형이므로 inline 증거는 주로 `python/src/*.py`의 짧은 분기나 상태 전환 조각을 쓴다.
- CLI는 `make -C ... run-solution`, `make -C ... test`, 보조 `pytest`나 `curl` 흐름을 실제 재현 순서대로 남긴다.
- 정확한 날짜 근거가 부족해 대부분 `Day/Session`을 기본 형식으로 썼다.
- source set만으로 비는 부분은 일반적인 개발자 수준의 추론으로 메운다.
