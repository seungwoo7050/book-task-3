# Web Proxy 시리즈 맵

이 lab의 핵심 질문은 프록시가 무엇을 숨기느냐가 아니라, 무엇을 대신 떠안느냐다. 현재 구현은 client 요청을 읽는 server이고, 동시에 origin으로 새 TCP 연결을 여는 client다. 여기에 파일 기반 cache까지 얹으면서 URL 파싱, origin request 재구성, cache key 생성, proxy-specific error response를 한곳에 묶는다.

## 이 lab를 읽는 질문

- 절대 URL을 origin request로 바꾸는 최소 규칙은 무엇인가
- cache는 어떤 단위로 저장되고 재사용되는가
- 프록시 오류는 origin 오류와 어떻게 다르게 표현되는가

## 이번에 고정한 사실

- `parse_url()`은 `(hostname, port, path)`를 만든다.
- cache key는 URL MD5 hash 기반 파일명이다.
- cache hit면 origin 연결 없이 응답을 그대로 돌려준다.
- timeout은 `504 Gateway Timeout`, origin reachability 실패는 `502 Bad Gateway`로 구분한다.
