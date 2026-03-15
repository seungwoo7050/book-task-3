# Web Proxy 개발 타임라인

이 lab의 흐름은 기능이 늘어나는 역사보다, 프록시가 어떤 분기점들을 직접 맡는지 따라가는 편이 더 정확하다.

## 1. 먼저 요청 라인을 읽고 절대 URL만 허용한다

현재 구현은 `GET` 외 요청이나 토큰 부족 요청을 바로 `400 Bad Request`로 거절한다. 즉 출발점은 캐시가 아니라 request line parsing이다. 프록시는 브라우저와 달리 절대 URL을 입력으로 받기 때문에, 이 parsing이 origin fetch 전체의 전제가 된다.

## 2. cache hit을 먼저 판단해 중개 비용을 줄인다

`get_cache_path(url)`로 파일 경로를 만들고, 파일이 있으면 origin 연결 없이 곧바로 cached response를 반환한다. 테스트도 첫 fetch와 second fetch를 나눠서 이 동작을 확인한다. 현재 cache는 TTL이나 validation이 없는 단순한 파일 저장이지만, "같은 URL을 다시 받으면 더 이상 origin으로 가지 않는다"는 의미는 분명하다.

## 3. miss면 origin client 역할로 전환한다

cache miss가 나면 proxy는 곧바로 origin client가 된다. `fetch_from_origin()`은 `GET {path} HTTP/1.1`, `Host`, `Connection: close`, `User-Agent`를 넣어 새 요청을 만들고, origin 응답을 끝까지 읽는다. 이 지점이 이 lab의 진짜 전환점이다. 하나의 프로그램이 request receiver와 request emitter를 모두 맡는다.

## 4. 프록시 오류는 별도 HTTP 상태로 드러난다

timeout은 `504`, origin DNS/connection 문제는 `502`로 나뉜다. 즉 이 lab는 단순 중계가 아니라, origin과 client 사이의 실패를 프록시 관점에서 다시 번역한다.

## 5. 현재 검증이 보여 주는 범위

2026-03-14 정식 재실행에서는 세 가지가 pass했다.

- 첫 fetch 성공
- second fetch cache 재사용
- 응답 body 비어 있지 않음

보조 테스트는 URL parsing과 cache key stability를 직접 고정한다. 그래서 이 lab의 핵심은 완전한 HTTP cache가 아니라, 중개자 구조의 첫 책임들을 분명히 드러내는 것이다.
