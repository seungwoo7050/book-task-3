# Application Protocols and Sockets

응용 계층 프로토콜을 직접 구현하며 TCP/UDP 소켓 프로그래밍의 기본 패턴을 익히는 트랙입니다.

## 이 트랙이 맡는 역할

정적 웹 서버에서 시작해 UDP timeout 처리, 텍스트 기반 메일 프로토콜, 프록시 캐시까지 넓혀 가며 "소켓 위에서 애플리케이션 규칙을 직접 구현한다"는 감각을 길러 줍니다.

## 추천 선수 지식

- Python 기본 문법과 표준 라이브러리 사용법
- TCP와 UDP의 차이를 아주 기초 수준에서 알고 있으면 좋습니다.
- 명령줄에서 `make`와 `python3`를 실행할 수 있으면 바로 시작할 수 있습니다.

## 권장 프로젝트 순서

1. [Web Server](web-server/README.md) - `verified`
   TCP 연결 수립, HTTP 요청 파싱, 정적 파일 응답의 최소 구현을 다집니다.
2. [UDP Pinger](udp-pinger/README.md) - `verified`
   UDP에서 timeout과 RTT 통계를 애플리케이션이 직접 책임지는 구조를 배웁니다.
3. [SMTP Client](smtp-client/README.md) - `verified`
   명령-응답이 여러 단계로 이어지는 텍스트 프로토콜을 소켓 레벨에서 구현합니다.
4. [Web Proxy](web-proxy/README.md) - `verified`
   클라이언트와 원 서버 사이에서 요청을 중계하고 캐시하는 중개자 역할을 연습합니다.

## 공통 읽기 방법

- `problem/README.md`로 요구사항과 제공 자료를 먼저 확인합니다.
- `python/README.md`에서 구현 범위와 정식 검증 명령을 확인합니다.
- `docs/README.md`로 반복해서 볼 개념 문서를 고릅니다.
- `notion/README.md`는 더 깊은 작업 기록과 회고가 필요할 때만 보조 자료로 읽습니다.

## 포트폴리오로 확장하기

- 요청과 응답이 오가는 실제 로그를 남기고, 어떤 실패를 어떻게 처리했는지 짧게 설명하면 포트폴리오 설득력이 올라갑니다.
- 단순 구현 나열보다 `Web Server -> UDP Pinger -> SMTP Client -> Web Proxy`로 난도가 어떻게 확장되는지 연결해 보여 주는 편이 좋습니다.
- 후속 확장으로 남긴 범위를 숨기지 말고, 왜 범위를 잘랐는지와 다음 단계 아이디어를 함께 적어 두세요.
