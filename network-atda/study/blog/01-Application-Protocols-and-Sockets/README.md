# 01. Application Protocols and Sockets blog

TCP/UDP socket 위에서 HTTP, SMTP, ping, proxy를 직접 구현하며 응용 계층의 책임을 코드로 익히는 단계입니다.

## 이 트랙에서 무엇을 따라가면 되나

이 레이어는 프로젝트를 나열하는 데서 멈추지 않고, 왜 이 순서가 자연스러운지까지 같이 보여 주려고 한다. 구현형 프로젝트는 진입점과 테스트를 먼저 보고, 분석형 프로젝트는 trace 질문과 filter target을 먼저 잡는 방식으로 읽으면 흐름이 편하다.

## 권장 읽기 순서

1. [Web Server](web-server/README.md) - TCP 연결 하나를 받아 HTTP 요청, 파일 조회, 404 응답까지 어디서 나눠 구현했는가?
2. [UDP Pinger](udp-pinger/README.md) - 연결 없는 UDP에서 손실과 timeout을 클라이언트 쪽 코드로 어떻게 드러냈는가?
3. [SMTP Client](smtp-client/README.md) - SMTP 대화를 raw socket 위에서 단계별 명령으로 어떻게 끝까지 완주했는가?
4. [Web Proxy](web-proxy/README.md) - 클라이언트 요청, origin fetch, cache 저장을 프록시 안에서 어떻게 이어 붙였는가?

## 공통으로 보는 근거

- 프로젝트 README와 `problem/README.md`
- `problem/Makefile`의 실행/검증 target
- 구현형은 `python/` 또는 `cpp/`, 분석형은 `analysis/src/`
- 테스트 파일과 `docs/concepts/`
