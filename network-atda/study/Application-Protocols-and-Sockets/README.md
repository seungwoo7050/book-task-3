# Application Protocols and Sockets

응용 계층 프로토콜을 구현하면서 TCP/UDP 소켓의 기본 패턴을 다지는 트랙이다.

## 왜 이 트랙인가

웹 서버에서 시작해 timeout, 텍스트 프로토콜, 중개자 역할까지 단계적으로 확장한다.

## 프로젝트 순서

1. [Web Server](web-server/README.md) - `verified`
   핵심: TCP 소켓과 HTTP/1.1 응답 조합으로 정적 파일 서버를 구현하는 파일럿 과제다.
2. [UDP Pinger](udp-pinger/README.md) - `verified`
   핵심: UDP 비연결성과 timeout 기반 손실 처리를 RTT 측정 과제로 묶은 구현이다.
3. [SMTP Client](smtp-client/README.md) - `verified`
   핵심: 텍스트 기반 명령-응답 프로토콜을 TCP 위에서 직접 수행하는 메일 클라이언트 과제다.
4. [Web Proxy](web-proxy/README.md) - `verified`
   핵심: 클라이언트 요청을 중계하고 파일 기반 캐시로 재사용하는 간단한 HTTP 프록시 구현이다.

## 공통 규칙

- 코드 과제는 `problem/`과 `python/`을 분리한다.
- 패킷 분석 랩은 `problem/`과 `analysis/`를 분리한다.
- 시행착오와 회고는 `notion/`으로 밀어내고, 공개 README는 인덱스 역할만 맡긴다.
