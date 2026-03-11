# 01. Application Protocols and Sockets

TCP/UDP socket 위에서 HTTP, SMTP, ping, proxy를 직접 구현하며 응용 계층의 책임을 코드로 익히는 단계입니다.

## 프로젝트 카탈로그

| 프로젝트 | 문제 | 이 레포의 답 | 검증 | 상태 | 왜 이 단계에 있는가 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`Web Server`](web-server/README.md) | `Computer Networking: A Top-Down Approach`의 웹 서버 구현 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 | `python/src/` | `make -C study/01-Application-Protocols-and-Sockets/web-server/problem test` | `verified` | 이 트랙의 출발점으로, 연결 수립부터 요청 파싱, 파일 읽기, 응답 생성, 연결 종료까지 서버의 기본 생애주기를 가장 짧은 경로로 경험하게 합니다. |
| [`UDP Pinger`](udp-pinger/README.md) | `Computer Networking: A Top-Down Approach`의 UDP ping 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 | `python/src/` | `make -C study/01-Application-Protocols-and-Sockets/udp-pinger/problem test` | `verified` | 웹 서버 다음 단계에서 "연결이 없는 전송"이 애플리케이션 코드에 어떤 책임을 남기는지 분명하게 드러냅니다. |
| [`SMTP Client`](smtp-client/README.md) | `Computer Networking: A Top-Down Approach`의 SMTP 메일 클라이언트 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 | `python/src/` | `make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem test` | `verified` | HTTP와 비슷하게 텍스트 명령을 쓰지만 상태 전이가 더 길고 명확해서, 응용 계층 프로토콜의 단계적 흐름을 연습하기 좋습니다. |
| [`Web Proxy`](web-proxy/README.md) | `Computer Networking: A Top-Down Approach`의 HTTP 프록시 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 | `python/src/` | `make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem test` | `verified` | 클라이언트와 원 서버의 역할을 한 프로그램 안에서 동시에 다루게 만들어, 앞선 소켓 과제보다 한 단계 복잡한 중개자 구조를 연습하게 합니다. |

## 공통 읽기 순서

1. 프로젝트 README에서 문제, 답, 검증 명령을 먼저 확인합니다.
2. `problem/README.md`에서 제공 자료와 성공 기준을 확인합니다.
3. 구현형 과제는 `python/README.md` 또는 `cpp/README.md`, 분석형 과제는 `analysis/README.md`로 내려갑니다.
4. `docs/README.md`는 개념을 다시 확인할 때만 참고하고, `notion/README.md`는 보조 기록으로만 읽습니다.
