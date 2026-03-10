# Web Proxy

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 HTTP 프록시 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 |
| 정식 검증 | `make -C study/Application-Protocols-and-Sockets/web-proxy/problem test` |

## 한 줄 요약

클라이언트 요청을 중계하고 파일 기반 캐시로 재사용하는 간단한 HTTP 프록시 구현입니다.

## 왜 이 프로젝트가 필요한가

클라이언트와 원 서버의 역할을 한 프로그램 안에서 동시에 다루게 만들어, 앞선 소켓 과제보다 한 단계 복잡한 중개자 구조를 연습하게 합니다.

## 이런 학습자에게 맞습니다

- 프록시가 절대 URL을 어떻게 해석하고 원 서버 요청으로 바꾸는지 보고 싶은 학습자
- 캐시가 있는 네트워크 애플리케이션의 최소 구조를 직접 구현해 보고 싶은 학습자

## 지금 바로 읽는 순서

1. `problem/README.md` - 구현 목표, 제공 자료, 성공 기준을 먼저 확인합니다.
2. `python/README.md` - 공개 구현 범위와 정식 검증 명령을 확인합니다.
3. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.
4. `notion/README.md` - 더 깊은 작업 기록과 회고가 필요할 때 참고합니다.

## 제공 자료

- `problem/code/proxy_skeleton.py`: 시작용 skeleton 코드
- `problem/script/test_proxy.sh`: 원 서버를 포함한 정식 검증 스크립트
- `python/tests/test_web_proxy.py`: URL 파싱과 캐시 키 생성을 확인하는 보조 테스트

## 실행과 검증

- 실행: `make -C study/Application-Protocols-and-Sockets/web-proxy/problem run-solution`
- 검증: `make -C study/Application-Protocols-and-Sockets/web-proxy/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 학습 포인트

- 절대 URL 파싱과 origin request 재구성
- 프록시의 server/client 이중 역할
- MD5 기반 캐시 키 설계
- `502`, `504` 같은 프록시 전용 오류 응답

## 현재 한계

- `Cache-Control`이나 TTL 기반 만료 정책은 없습니다.
- `HTTPS CONNECT`는 지원하지 않습니다.
- 캐시 디렉터리 동시성 제어는 단순한 수준에 머뭅니다.

## 포트폴리오로 확장하기

- 캐시 만료 정책, `CONNECT`, 로그 요약을 추가하면 작은 과제에서 꽤 설명력 있는 네트워크 도구로 발전합니다.
- origin fetch와 cache hit를 비교한 시연 캡처를 남기면 포트폴리오에서 이해가 빨라집니다.
- 프록시가 어떤 보안·성능 한계를 갖는지 README에 분명히 적어 두면 더 성숙한 문서가 됩니다.
