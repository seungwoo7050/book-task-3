# HTTP Packet Analysis 개발 타임라인

## Day 1 — 네 개의 trace를 한 질문 흐름으로 묶기

### Session 1

- 목표: HTTP를 막연히 "GET과 200 OK"로 읽지 않고, 기본 trace에서 어떤 필드를 가장 먼저 고정해야 하는지 정한다.
- 진행: 가장 작은 `http-basic.pcapng`부터 열었다. 요청 frame과 응답 frame을 한 쌍으로 붙여 두고, HTTP 버전, 상태 코드, `Content-Length`, `Last-Modified`, `Connection`이 어디서 나오나 체크했다.
- 이슈: 처음엔 status line만 보면 답이 끝날 줄 알았다. 그런데 실제 답안은 "서버가 파일을 언제 수정했는가", "브라우저가 어떤 언어를 받겠다고 했는가"까지 물었다. 즉 응답 line만 보는 습관으로는 부족했다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/http/problem filter-basic
4   192.168.0.2      128.119.245.12   GET   /kurose_ross_small/HTTP/index.html        
6   128.119.245.12   192.168.0.2             200   36
```

- 메모: 이 출력만으로도 "요청은 frame 4, 응답은 frame 6"이라는 기본 축이 잡혔다. 이후 세부 질문은 결국 이 두 frame 안으로 다시 돌아왔다.

### Session 2

- 목표: conditional GET이 왜 별도 시나리오인지 분리해서 이해한다.
- 진행: `http-conditional.pcapng`의 첫 GET과 두 번째 GET을 비교했다. 첫 요청에는 조건부 헤더가 없고, 두 번째 요청에만 `If-Modified-Since`가 붙는다. 응답도 `200 OK`에서 `304 Not Modified`로 바뀐다.
- 이슈: 처음에는 `304`를 단순한 상태 코드 암기 문제로 봤다. 실제로는 "본문이 없는 응답"이라는 점이 더 중요했다. 요청 헤더와 응답 본문 부재를 같이 봐야 캐시 검증이라는 이야기가 성립했다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/http/problem filter-conditional
4   GET        
5              200   OK              Mon, 17 Feb 2025 06:59:02 GMT
7   GET                                        GET /kurose_ross_small/HTTP/index.html HTTP/1.1
8              304   Not Modified
```

- 메모: 이 시점부터 HTTP 답안을 frame 단위로 적지 않으면 쉽게 뭉개진다는 걸 알았다. `304`라는 숫자만 적는 대신, "두 번째 GET에 조건부 헤더가 있고 응답 본문은 빠진다"까지 같이 묶어야 했다.

### Session 3

- 목표: 긴 문서 trace에서 `Content-Length`와 TCP segment 수를 연결한다.
- 진행: `filter-long`은 두 단계로 나온다. 먼저 HTTP packet 요약을 보여 주고, 그다음 서버가 보낸 data-bearing TCP segment 개수를 세어 준다. 여기서 `Content-Length: 9000`이 실제 전송 크기와 모순 없는지 다시 계산했다.
- 이슈: 처음엔 `Content-Length`만 적으면 충분하다고 생각했다. 그런데 서버 응답이 여러 TCP segment에 나뉘면, HTTP 메시지 길이와 TCP payload 총합을 분리해서 봐야 했다. 아니면 9000바이트와 9066바이트를 보고 숫자가 어긋난다고 오해하기 쉽다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/http/problem filter-long
=== HTTP packets ===
4   GET /kurose_ross_small/HTTP/long.txt HTTP/1.1
11  HTTP/1.1 200 OK
		Content-Length: 9000

=== Total TCP data segments from server ===
7
```

- 메모: 여기서 처음으로 "HTTP는 메시지 단위, TCP는 segment 단위"라는 층위 차이가 선명해졌다. `9000`은 body 길이이고, 실제 wire 위 바이트는 헤더까지 포함해 더 커질 수 있다는 감각을 얻었다.

### Session 4

- 목표: embedded object trace로 브라우저가 추가 리소스를 어떤 순서로 가져오는지 확인한다.
- 진행: `http.request.method == GET`만 뽑아 세 개의 GET을 순서대로 정리했다. `/index.html` 이후 `/img1.png`, 그다음 `/img2.png`가 요청된다. 두 이미지 요청 모두 `Referer: /index.html`을 갖는다.
- 이슈: 처음에는 현대 브라우저처럼 병렬 다운로드를 기대했다. 하지만 이 synthetic trace에서는 겹치는 outstanding request가 없다. 그래서 "병렬처럼 보일 수도 있다"는 일반론을 억지로 넣으면 오히려 틀린 설명이 된다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/http/problem filter-embedded
4    128.119.245.12   /index.html
7    128.119.245.12   /img1.png    /index.html
10   128.119.245.12   /img2.png    /index.html
```

```bash
$ make -C study/03-Packet-Analysis-Top-Down/http/problem test
bash script/verify_answers.sh
HTTP analysis answers look complete.
```

- 정리:
	- 기본 GET trace는 질문의 기준 frame을 잡는 용도였다.
	- conditional GET trace는 캐시 검증이 "헤더 차이 + 본문 부재"로 드러난다는 걸 보여 줬다.
	- 긴 문서 trace는 HTTP 길이와 TCP segment 개수를 연결하게 만들었다.
	- embedded object trace는 synthetic capture에서는 일반론보다 실제 frame 순서를 우선해야 한다는 교훈을 남겼다.
