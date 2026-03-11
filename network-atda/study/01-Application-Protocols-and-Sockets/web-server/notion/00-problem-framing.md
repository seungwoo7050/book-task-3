# 00 문제 프레이밍

## 프로젝트 정의
- 프로젝트: `Web Server`
- 상태: `verified`
- 기준 검증: `make -C study/01-Application-Protocols-and-Sockets/web-server/problem test`
- 문제 배경: `Computer Networking: A Top-Down Approach`의 웹 서버 구현 과제를 현재 저장소 구조에 맞게 옮긴 프로젝트다.

## 이번 범위
- `GET` 요청 한 줄을 파싱해서 정적 파일을 반환한다.
- `/` 요청을 기본 문서인 `hello.html`로 연결한다.
- 확장자에 따라 `Content-Type`을 정하고, 없는 파일에는 `404 Not Found`를 돌려준다.
- 동시 접속은 스레드 기반으로 처리하되, 검증 범위는 교육용 수준의 최소 구현에 둔다.

## 제약과 전제
- 범위는 `HTTP/1.1`의 아주 작은 부분집합이다. `GET` 외 메서드, keep-alive, 청크 전송은 다루지 않는다.
- 제공 파일과 테스트는 `problem/` 아래에 있고, 실제 구현은 `python/`으로 분리한다.
- 테스트는 상태 코드, 본문, MIME 타입, 순차 요청 처리를 중심으로 확인한다.

## 성공 기준
- `hello.html` 요청에 `200 OK`와 HTML 본문이 내려온다.
- 없는 파일 요청에 `404 Not Found`와 오류 본문이 내려온다.
- `make -C study/01-Application-Protocols-and-Sockets/web-server/problem test`가 통과한다.

## 공개 문서
- [`../README.md`](../README.md)
- [`../problem/README.md`](../problem/README.md)
- [`../python/README.md`](../python/README.md)
- [`../docs/README.md`](../docs/README.md)
- [`../docs/references/README.md`](../docs/references/README.md)

## 이번에 일부러 제외한 것
- 경로 정규화와 path traversal 방어를 제품 수준으로 다듬지는 않았다.
- 접속당 스레드 모델을 `select`/`asyncio` 기반으로 바꾸지는 않았다.
- TLS, 가상 호스트, 디렉터리 listing 같은 웹 서버 기능은 범위 밖이다.
