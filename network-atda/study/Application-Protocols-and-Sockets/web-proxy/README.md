# Web Proxy

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 레거시 원본 | `legacy/Programming-Assignments/web-proxy` |
| 정식 검증 | `make -C study/Application-Protocols-and-Sockets/web-proxy/problem test` |

## 한 줄 요약

클라이언트 요청을 중계하고 파일 기반 캐시로 재사용하는 간단한 HTTP 프록시 구현이다.

## 문제 요약

프록시는 절대 URL이 포함된 GET 요청을 받아 원 서버에 전달하고, 응답을 캐시에 저장한 뒤 같은 URL 요청에는 캐시를 반환한다.

## 이 프로젝트를 여기 둔 이유

응용 계층 소켓 과제 중 가장 중개자 역할이 뚜렷해, 서버와 클라이언트 책임을 한 프로그램에서 동시에 다루게 만든다.

## 제공 자료

- `problem/code/proxy_skeleton.py` skeleton
- `problem/script/test_proxy.sh` 원 서버 포함 통합 검증
- `python/tests/test_web_proxy.py` self-contained parsing tests

## 학습 포인트

- 절대 URL 파싱과 origin request 재구성
- 프록시의 server/client 이중 역할
- MD5 기반 캐시 키 설계
- 502/504 같은 프록시 전용 오류 응답

## 실행과 검증

- 실행: `make -C study/Application-Protocols-and-Sockets/web-proxy/problem run-solution`
- 검증: `make -C study/Application-Protocols-and-Sockets/web-proxy/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 현재 범위와 한계

HTTP GET과 간단한 파일 캐시만 다룬다. HTTPS 터널링이나 만료 정책은 다루지 않는다.

- 현재 한계: TTL/Cache-Control 기반 만료 정책 없음
- 현재 한계: HTTPS CONNECT 미지원
- 현재 한계: cache 디렉터리 동시성 제어 없음

## Public / Private 경계

- `problem/`은 제공 자료와 canonical 검증 래퍼만 둔다.
- `python/` 또는 `analysis/`는 공개 구현과 공개 답안만 둔다.
- `docs/`는 반복해서 참고할 개념 메모만 유지한다.
- `notion/`은 노션 업로드용 작업 노트이며 저장소 공개 구조에 의존하지 않는다.
