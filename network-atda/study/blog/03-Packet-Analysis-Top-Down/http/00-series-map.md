# HTTP Packet Analysis 시리즈 맵

이 lab의 중심 질문은 "HTTP header를 읽을 수 있는가"가 아니라 "서로 다른 trace 시나리오를 비교하면 browser와 server의 상호작용이 어떤 패턴으로 드러나는가"다. 현재 답안은 네 trace를 따로 쪼갠다. basic trace는 `200 OK`와 `Last-Modified`, conditional trace는 `If-Modified-Since`와 `304`, long document trace는 하나의 object가 여러 TCP segment로 쪼개지는 장면, embedded trace는 object 요청 순서가 직렬인지 병렬인지의 판정 근거를 맡는다.

## 이 lab를 읽는 질문

- `HTTP/1.1` keep-alive가 단순 상태줄보다 어디에서 드러나는가
- conditional GET은 같은 resource fetch를 어떻게 body 없는 `304`로 바꾸는가
- "긴 문서"와 "여러 객체"는 transport 위에서 어떤 다른 흔적을 남기는가

## 이번에 사용한 근거

- `problem/README.md`
- `analysis/src/http-analysis.md`
- `problem/Makefile`
- `problem/script/verify_answers.sh`
- 2026-03-14 재실행한 `filter-basic`, `filter-conditional`, `filter-embedded`

## 이번 재실행에서 고정한 사실

- basic trace의 request/response는 둘 다 `HTTP/1.1`이고 response는 `200`, `Content-Length 36`이다.
- conditional trace는 첫 GET 뒤 `200 OK`, 두 번째 GET 뒤 `304 Not Modified`로 갈린다.
- long document trace는 HTTP GET 1개에 대해 server data segment 7개가 필요하다.
- embedded trace는 `/img1.png` 응답이 끝난 뒤 `/img2.png` 요청이 나와 직렬 fetch로 읽힌다.
