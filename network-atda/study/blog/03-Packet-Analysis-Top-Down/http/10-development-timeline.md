# HTTP Packet Analysis 개발 타임라인

현재 답안을 다시 읽으면 이 lab의 흐름은 HTTP 기능 목록을 한 번에 훑는 방식이 아니다. 네 개의 trace를 순서대로 열면서, "하나의 object 요청"에서 "조건부 재검증", "긴 body transport", "여러 object fetch ordering"으로 관찰 시야를 넓혀 가는 구조다. 전환점은 네 번이다.

## 1. basic trace에서 HTTP/1.1 request/response의 최소 surface를 먼저 고정한다

출발점은 frame `4`의 `GET /kurose_ross_small/HTTP/index.html HTTP/1.1`과 frame `6`의 `HTTP/1.1 200 OK`다. 여기에 `Accept-Language`, `Last-Modified`, `Content-Length: 36`, `Connection: keep-alive`가 붙으면서, 이 lab는 "HTTP는 텍스트 프로토콜" 수준을 넘어 browser와 server가 어떤 metadata를 주고받는지 보여 주기 시작한다.

즉 첫 단계의 핵심은 request line과 status line만이 아니라, body 길이와 freshness hint가 이미 이 기본 trace에 같이 들어 있다는 점이다.

## 2. conditional trace에서 같은 resource fetch가 `304`로 가벼워지는 장면을 확인한다

두 번째 전환은 `If-Modified-Since`다. 첫 GET에는 조건 헤더가 없고 `200 OK`와 body가 온다. 이후 두 번째 GET에는 `If-Modified-Since: Mon, 17 Feb 2025 06:59:02 GMT`가 붙고, 응답은 `304 Not Modified`로 짧아진다.

이 차이 때문에 conditional GET은 "헤더 하나 더 붙였다"가 아니라, 같은 리소스 요청이 body 없는 validation round-trip으로 바뀌는 메커니즘으로 읽혀야 한다. 현재 답안도 바로 그 점을 중심에 둔다.

## 3. long document trace는 HTTP object 하나가 transport에서는 여러 segment라는 사실을 드러낸다

세 번째 전환은 object 수와 segment 수를 분리해서 보는 것이다. long document trace는 HTTP GET이 1개뿐이지만 server-to-client data segment는 7개다. `Content-Length`는 9000이고, 실제 전송된 TCP data 총합은 header까지 포함해 9066 bytes가 된다.

즉 HTTP level의 "document 하나"와 TCP level의 "segment 여러 개"는 다른 단위라는 사실을 여기서 눈으로 확인하게 된다. 이 장면이 transport analysis lab로 이어지는 연결점이기도 하다.

## 4. embedded objects trace는 직렬 fetch 판정을 referer와 순서로 닫는다

마지막 전환은 여러 object가 있다고 해서 반드시 병렬 fetch인 것은 아니라는 점이다. `filter-embedded` 재실행 결과 요청 순서는 `/index.html -> /img1.png -> /img2.png`였고, 두 image GET 모두 `Referer: /index.html`을 가진다. 더 중요한 건 `/img1.png` 응답 뒤에 `/img2.png` 요청이 나오므로, 현재 trace에서는 직렬 download로 읽는 편이 맞다.

결국 이 lab는 HTTP를 "사람이 읽을 수 있는 프로토콜"로 보는 데서 멈추지 않는다. 같은 프로토콜이라도 cache validation, segmentation, object dependency에 따라 trace 읽기 방식이 달라진다는 점을 단계적으로 보여 준다.

## 지금 남는 한계

이 자료는 의도적으로 `HTTP/1.1` 중심이고 short trace 기반이다. 브라우저별 speculative fetch, connection coalescing, `HTTP/2` multiplexing은 현재 증거 범위 밖이다. 그래서 이 문서는 HTTP 전부를 덮는 설명보다, request/response 패턴을 trace별로 읽는 기준선을 세우는 문서로 남기는 편이 정확하다.
