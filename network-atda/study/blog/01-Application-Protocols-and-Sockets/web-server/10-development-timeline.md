# Web Server 개발 타임라인

이 lab의 흐름은 기능 확장보다, 서버가 한 요청을 어디까지 직접 책임지는지 따라가는 편이 더 정확하다.

## 1. accept loop를 먼저 세운다

현재 구현은 `socket`, `bind`, `listen`, `accept`의 가장 짧은 경로를 따른다. 그리고 새 연결마다 daemon thread를 하나 만든다. 즉 출발점은 HTTP parsing보다 "요청 한 건을 처리할 실행 문맥을 어떻게 만든다"에 있다.

## 2. request line에서 파일명만 최소 파싱한다

`GET /hello.html HTTP/1.1` 같은 요청에서 path만 잘라내고 맨 앞 `/`를 제거해 실제 파일명을 만든다. 빈 path면 `hello.html`을 기본값으로 둔다. 이 단순함 덕분에 lab의 초점이 프레임워크 규칙이 아니라 socket->file 흐름에 남는다.

## 3. 파일 읽기 성공/실패가 곧 200/404 분기다

현재 구현은 아주 직접적이다.

- 파일 열기 성공: body를 읽고 `Content-Type`, `Content-Length`와 함께 `200 OK`
- `FileNotFoundError`: 미리 준비한 404 HTML body와 함께 `404 Not Found`

즉 HTTP 상태 코드는 별도 라우터에서 정해지는 게 아니라 파일 시스템 분기에서 곧바로 결정된다.

## 4. MIME 추정과 연결 종료까지 한 요청 안에서 닫는다

`get_content_type()`은 확장자 기반 map을 사용하고, 응답 전송이 끝나면 항상 socket을 닫는다. keep-alive나 method dispatch가 없기 때문에, 한 연결은 사실상 한 번의 파일 응답 생애주기를 가진다.

## 5. 현재 검증이 보여 주는 범위

2026-03-14 정식 재실행에서는 세 가지가 pass했다.

- `/hello.html` 200
- `/nonexistent` 404
- body 안의 HTML 확인

보조 테스트는 같은 서버가 연속 요청 3건도 처리할 수 있는지 확인한다. 따라서 이 lab는 production web server라기보다, 정적 파일 서빙의 가장 작은 end-to-end skeleton으로 읽는 편이 맞다.
