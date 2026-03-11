# HTTP Packet Analysis 문제 안내

## 이 문서의 역할

이 문서는 `HTTP Packet Analysis`를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 답안을 먼저 보기보다 trace 범위와 질문을 먼저 이해하는 데 초점을 둡니다.

## 문제 목표

미리 캡처된 HTTP trace를 Wireshark로 분석해, 메시지 수준에서 HTTP 프로토콜이 어떻게 동작하는지 이해합니다. 기본 GET, conditional GET, 긴 문서 전송, 다중 객체 페이지 로딩을 모두 관찰합니다.

## 제공 trace

| 파일 | 시나리오 | 설명 |
| :--- | :--- | :--- |
| `http-basic.pcapng` | 기본 GET | 짧은 HTML 페이지를 요청하고 `200 OK`를 받는 단일 교환 |
| `http-conditional.pcapng` | Conditional GET | 같은 페이지를 두 번 요청하며 두 번째 요청에 `If-Modified-Since`가 포함됨 |
| `http-long-document.pcapng` | 긴 문서 전송 | 하나의 HTTP 응답이 여러 TCP segment로 나뉘는 예시 |
| `http-embedded-objects.pcapng` | Embedded Objects | 이미지가 포함된 페이지 로딩 예시 |

## 풀어야 할 질문

### 파트 1. 기본 HTTP GET / 응답 (`http-basic.pcapng`)

1. 브라우저와 서버는 각각 어떤 HTTP 버전을 사용하고 있습니까?
2. 브라우저가 서버에 전달한 언어 관련 헤더가 있습니까?
3. 클라이언트와 서버(`gaia.cs.umass.edu`)의 IP 주소는 무엇입니까?
4. 서버가 반환한 HTTP 상태 코드는 무엇입니까?
5. 가져온 HTML 파일의 마지막 수정 시각은 무엇입니까?
6. 응답 본문은 몇 바이트입니까?
7. 응답 패킷의 raw data를 볼 때 `Connection` 헤더가 포함되어 있습니까? 있다면 값은 무엇입니까?

### 파트 2. Conditional GET (`http-conditional.pcapng`)

1. 첫 번째 GET 요청에는 `If-Modified-Since` 또는 `If-None-Match`가 포함되어 있습니까?
2. 첫 번째 응답의 상태 코드와 phrase는 무엇이며, 서버는 파일 내용을 실제로 다시 보냈습니까?
3. 두 번째 GET 요청에는 `If-Modified-Since`가 포함되어 있습니까? 있다면 어떤 값이 따라옵니까?
4. 두 번째 요청에 대한 응답 상태 코드와 phrase는 무엇이며, 파일 본문이 실제로 전송되었는지 설명해 보세요.

### 파트 3. 긴 문서 (`http-long-document.pcapng`)

1. 브라우저는 HTTP GET 요청을 몇 번 보냈고, 하나의 응답을 전달하는 데 몇 개의 TCP segment가 필요했습니까?
2. 응답의 상태 코드와 phrase는 무엇입니까?
3. 서버는 실제 데이터가 담긴 TCP segment를 몇 개 보냈습니까?
4. HTTP 응답의 `Content-Length` 값은 얼마이며, 실제 전송된 데이터 양과 일치합니까?

### 파트 4. Embedded Objects (`http-embedded-objects.pcapng`)

1. 브라우저는 HTTP GET 요청을 총 몇 번 보냈고, 각각 어느 IP 주소로 향했습니까?
2. 브라우저가 이미지를 직렬로 내려받았는지 병렬로 내려받았는지 trace 근거로 설명해 보세요.
3. 기본 HTML 페이지의 상태 코드는 무엇이며, embedded image들의 상태 코드는 무엇입니까?
4. 이미지 요청의 `Referer` 헤더에는 어떤 URL이 들어 있으며, 왜 그 값이 필요한가요?

## 성공 기준

| 항목 | 내용 |
| :--- | :--- |
| 정확성 | 정확한 packet/frame 번호와 field 값을 사용합니다. |
| 완결성 | 모든 질문에 근거를 포함해 답합니다. |
| 이해도 | 프로토콜 메커니즘을 이해한 설명을 제시합니다. |
| 근거성 | Wireshark field와 trace evidence를 직접 인용합니다. |
