# Web Proxy

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 HTTP 프록시 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 |
| 정식 검증 | `make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem test` |

## 문제가 뭐였나
- 문제 배경: `Computer Networking: A Top-Down Approach`의 HTTP 프록시 과제를 현재 저장소 구조에 맞게 정리한 프로젝트
- 이 단계에서의 역할: 클라이언트와 원 서버의 역할을 한 프로그램 안에서 동시에 다루게 만들어, 앞선 소켓 과제보다 한 단계 복잡한 중개자 구조를 연습하게 합니다.

## 제공된 자료
- `problem/code/proxy_skeleton.py`: 시작용 skeleton 코드
- `problem/script/test_proxy.sh`: 원 서버를 포함한 정식 검증 스크립트
- `python/tests/test_web_proxy.py`: URL 파싱과 캐시 키 생성을 확인하는 보조 테스트

## 이 레포의 답
- 한 줄 답: 클라이언트 요청을 중계하고 파일 기반 캐시로 재사용하는 간단한 HTTP 프록시 구현입니다.
- 공개 답안 위치: `python/src/`
- 보조 공개 표면: `python/tests/`
- 보조 공개 표면: `docs/`
- 보조 공개 표면: `study/blog/01-Application-Protocols-and-Sockets/web-proxy/`
- 읽는 순서:
  1. `problem/README.md` - 문제 조건, 제공 자료, 성공 기준을 먼저 확인합니다.
  2. `python/README.md` - 현재 공개 답안 범위와 기준 명령을 확인합니다.
  3. `../../blog/01-Application-Protocols-and-Sockets/web-proxy/README.md` - 실제 소스 기준의 개발 chronology를 따라갑니다.
  4. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.
  5. `notion/README.md` - 공개 학습 노트이지만 엔트리포인트는 아닙니다.

## 어떻게 검증하나
- 실행: `make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem run-solution`
- 검증: `make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 무엇을 배웠나
- 절대 URL 파싱과 origin request 재구성
- 프록시의 server/client 이중 역할
- MD5 기반 캐시 키 설계
- `502`, `504` 같은 프록시 전용 오류 응답

## 현재 한계
- `Cache-Control`이나 TTL 기반 만료 정책은 없습니다.
- `HTTPS CONNECT`는 지원하지 않습니다.
- 캐시 디렉터리 동시성 제어는 단순한 수준에 머뭅니다.
